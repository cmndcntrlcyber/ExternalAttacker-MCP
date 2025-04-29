from fastmcp import FastMCP
import subprocess
import requests
import os
mcp = FastMCP("docs")

def run_command(command: list):
    """Run command via the Flask app's /api/run endpoint"""
    try:
        tool = command[0]
        args = " ".join(command[1:])
        
        response = requests.post(
            "http://localhost:6991/api/run",
            json={"tool": tool, "args": args},
            timeout=300
        )
        
        # Handle HTTP errors
        if response.status_code != 200:
            return {
                'stdout': '',
                'stderr': f'HTTP Error: {response.status_code}',
                'returncode': 1
            }
        
        # Parse JSON response
        result = response.json()
        
        # Ensure response has the expected structure
        if 'error' in result and 'stdout' not in result:
            return {
                'stdout': '',
                'stderr': result['error'],
                'returncode': 1
            }
            
        return result
    except requests.exceptions.RequestException as e:
        return {
            'stdout': '',
            'stderr': f'Request error: {str(e)}',
            'returncode': 1
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Error: {str(e)}',
            'returncode': 1
        }

@mcp.tool()
async def scan_subdomains(target: str, domain_file: bool, threads: int = 4):
    """
    Scan target domain(s) for subdomains using subfinder binary
    
    Args:
        target: Domain or file containing domains to scan
        domain_file: Whether target is a file containing domains
        threads: Number of concurrent threads to use
    """
    command = [
        "subfinder",
        "-list" if domain_file else "-domain", target,
        "-json",
        "-all", 
        "-silent",
        "-active",
        "-t", str(threads)
    ]
    return run_command(command)

@mcp.tool()
async def scan_ports(target: str, file: bool, ports: str = "1-65535", top_ports: bool = False, threads: int = 20):
    """
    Scan a target domain for open ports using naabu binary
    
    Args:
        target: Domain or IP to scan
        file: Whether to scan a file containing domains
        ports: Port range to scan (e.g. "80,443" or "1-1000") or number of top ports
        top_ports: Whether to scan top N ports or use port range
        threads: Number of concurrent threads (default: 20)
    """
    command = [
        "naabu",
        "-silent",
        "-nc", 
        "-c", str(threads),
        "-r", "8.8.8.8",
        "-skip-host-discovery",
        "-scan-all-ips",
        "-json"
    ]

    if file:
        command.extend(["-list", str(target)])
    else:
        command.extend(["-host", str(target)])

    if top_ports:
        command.extend(["-top-ports", str(ports)])
    else:
        command.extend(["-port", str(ports)])

    return run_command(command)

@mcp.tool()
async def analyze_http_services(target: str, file: bool, threads: int = 20):
    """
    Scan a target domain for HTTP/HTTPS services using httpx binary
    
    Args:
        target: Domain or file containing domains to scan
        file: Whether target is a file containing domains
        threads: Number of concurrent threads to use
    """
    command = [
        "httpx",
        "-silent",
        "-nc", 
        "-threads", str(threads),
        "-json",
        "-title",
        "-status-code",
        "-content-length",
        "-server",
        "-tech-detect"
    ]

    if file:
        command.extend(["-list", str(target)])
    else:
        command.extend(["-target", str(target)])

    return run_command(command)

@mcp.tool()
async def detect_cdn(target: str, resolver: str = "8.8.8.8"):
    """
    Check if a target domain is using a CDN using cdncheck binary
    
    Args:
        target: Domain to check for CDN usage
        resolver: DNS resolver to use
    """
    command = [
        "cdncheck",
        "-input", str(target),
        "-resolver", resolver,
        "-nc",
        "-duc",
        "-silent",
        "-resp",
        "-jsonl"
    ]

    return run_command(command)

@mcp.tool()
async def analyze_tls_config(target: str, file: bool, port: int = 443, resolver: str = "8.8.8.8", threads: int = 300):
    """
    Scan a target domain for TLS/SSL configuration using tlsx binary
    
    Args:
        target: Domain or file containing domains to scan
        file: Whether target is a file containing domains
        port: Port to scan for TLS
        resolver: DNS resolver to use
        threads: Number of concurrent threads to use
    """
    command = [
        "tlsx",
        "-silent",
        "-resolvers", str(resolver),
        "-nc",
        "-c", str(threads),
        "-p", str(port),
        "-json",
        "-so",
        "-tls-version",
        "-cipher",
        "-wildcard-cert",
        "-probe-status",
        "-version-enum",
        "-cipher-enum",
        "-cipher-type", "all",
        "-serial"
    ]
    if file:
        command.extend(["-l", str(target)])
    else:
        command.extend(["-u", str(target)])
    
    return run_command(command)

@mcp.tool()
async def enumerate_assets(mode: str, target: str = None, wordlist: str = None, threads: int = 10, 
                  extensions: str = None, status_codes: str = None, output: str = None,
                  resolver: str = None, append_domain: bool = True, methods: str = None,
                  project: str = None, region: str = None, server: str = None):
    """
    Unified asset enumeration using gobuster binary
    
    Args:
        mode: Gobuster mode (dir/dns/vhost/fuzz/gcs/s3/tftp)
        target: Target URL/domain/server (required for dir/dns/vhost/fuzz/tftp)
        wordlist: Path to wordlist
        threads: Number of concurrent threads
        extensions: File extensions for dir mode
        status_codes: Status codes for dir mode
        output: Output file path
        resolver: DNS resolver for dns mode
        append_domain: Append domain in vhost mode
        methods: HTTP methods for fuzz mode
        project: Project ID for gcs mode
        region: AWS region for s3 mode
        server: Server address for tftp mode
    """
    if not wordlist:
        raise ValueError("wordlist is required")
        
    command = ["gobuster", mode, "-t", str(threads), "-q"]
    
    # Add mode-specific arguments
    if mode == "dir":
        if not target:
            raise ValueError("target is required for dir mode")
        command.extend(["-u", target+"/FUZZ", "-w", wordlist])
        if extensions:
            command.extend(["-x", extensions])
        if status_codes:
            command.extend(["-s", status_codes])
            
    elif mode == "dns":
        if not target:
            raise ValueError("target is required for dns mode")
        command.extend(["-d", target, "-w", wordlist])
        if resolver:
            command.extend(["-r", resolver])
            
    elif mode == "vhost":
        if not target:
            raise ValueError("target is required for vhost mode")
        command.extend(["-u", target, "-w", wordlist])
        if not append_domain:
            command.append("--append-domain=false")
            
    elif mode == "fuzz":
        if not target:
            raise ValueError("target is required for fuzz mode")
        command.extend(["-u", target, "-w", wordlist])
        if methods:
            command.extend(["-m", methods])
            
    elif mode == "gcs":
        command.extend(["-w", wordlist])
        if project:
            command.extend(["--project", project])
            
    elif mode == "s3":
        command.extend(["-w", wordlist])
        if region:
            command.extend(["--region", region])
            
    elif mode == "tftp":
        if not server:
            raise ValueError("server is required for tftp mode")
        command.extend(["-w", wordlist, "--server", server])
    
    if output:
        command.extend(["-o", output])
        
    return run_command(command)

@mcp.tool()
async def fuzz_endpoints(target: str, threads: int = 40,
                         wordlist: str = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/directory-list-2.3-medium.txt"):
    """
    Fuzz a target domain for hidden endpoints using ffuf binary
    
    Args:
        target: Target domain to fuzz
        threads: Number of concurrent threads to use
        wordlist: Path to wordlist to use
    """
    if "://" in wordlist:
        r = requests.get(wordlist)
        path = os.path.join(os.getcwd(), wordlist.split("/")[-1])
        with open(path, "w") as f:
            f.write(r.text)
        wordlist = path
    else:
        if not os.path.exists(wordlist):
            raise FileNotFoundError(f"File {wordlist} not found")
    command = [
        "ffuf",
        "-s",
        "-w", wordlist,
        "-u", target+"/FUZZ",
        "-t", str(threads)
    ]
    return run_command(command)

@mcp.tool()
async def resolve_dns(target: str, file: bool, threads: int = 100, resolver: str = "8.8.8.8",
                    wordlist: str = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt"):
    """
    Run DNS enumeration using dnsx binary
    
    Args:
        target: Domain or file containing domains to scan
        file: Whether target is a file containing domains
        threads: Number of concurrent threads to use
        resolver: DNS resolver to use
        wordlist: Path to wordlist for subdomain enumeration
    """
    if "://" in wordlist:
        r = requests.get(wordlist)
        path = os.path.join(os.getcwd(), wordlist.split("/")[-1])
        with open(path, "w") as f:
            f.write(r.text)
        wordlist = path
    else:
        if not os.path.exists(wordlist):
            raise FileNotFoundError(f"File {wordlist} not found")
    command = [
        "dnsx",
        "-silent",
        "-t", str(threads),
        "-json",
        "-r", str(resolver),
        "-all"
    ]
    if file:
        command.extend(["-l", str(target)])
    else:
        command.extend(["-d", str(target)])


if __name__ == "__main__":
    mcp.run(transport="stdio")