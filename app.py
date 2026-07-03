import threading
import uuid
import json
import os
from flask import Flask, jsonify, render_template, request
import nmap

app = Flask(__name__)

HISTORY_FILE = "scan_history.json"
# In-memory dictionary for active scans
scans = {}

def save_to_history(scan_data):
    """Appends completed scan data to a local JSON file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            pass
    
    history.append(scan_data)
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def execute_nmap_scan(scan_id, target, arguments):
    """Background worker that runs Nmap and parses results."""
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments=arguments)

        scan_results = []
        for host in nm.all_hosts():
            host_data = {
                "ip": host,
                "hostname": nm[host].hostname(),
                "state": nm[host].state(),
                "mac": nm[host].get('addresses', {}).get('mac', 'Unknown'),
                "os": nm[host].get('osmatch', [{'name': 'Unknown'}])[0]['name'] if nm[host].get('osmatch') else 'Unknown',
                "protocols": {},
            }

            for proto in nm[host].all_protocols():
                host_data["protocols"][proto] = []
                ports = nm[host][proto].keys()
                for port in ports:
                    port_info = nm[host][proto][port]
                    host_data["protocols"][proto].append({
                        "port": port,
                        "state": port_info["state"],
                        "name": port_info["name"],
                        "product": port_info.get("product", ""),
                        "version": port_info.get("version", "")
                    })
            scan_results.append(host_data)

        final_data = {
            "scan_id": scan_id, 
            "target": target, 
            "arguments": arguments, 
            "status": "completed", 
            "results": scan_results
        }
        
        scans[scan_id] = final_data
        save_to_history(final_data)

    except Exception as e:
        scans[scan_id] = {"status": "failed", "error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/scan", methods=["POST"])
def start_scan():
    data = request.json or {}
    target = data.get("target", "127.0.0.1")
    scan_type = data.get("type", "stealth")

    # Local-focused profiles (requires root/admin for OS and SYN scans)
    scan_profiles = {
        "stealth": "-sS -sV -O -T4",      # SYN stealth, versioning, OS detection
        "intense": "-T4 -A -v",           # Aggressive overall scan
        "ping_sweep": "-sn",              # Just find what IPs are online locally
        "vuln": "-sV --script vuln"       # Check versions against known CVEs
    }
    arguments = scan_profiles.get(scan_type, "-sS")

    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "results": []}

    thread = threading.Thread(target=execute_nmap_scan, args=(scan_id, target, arguments))
    thread.start()

    return jsonify({"scan_id": scan_id, "status": "running"})

@app.route("/api/scan/<scan_id>", methods=["GET"])
def get_scan_status(scan_id):
    scan = scans.get(scan_id)
    if not scan:
        return jsonify({"error": "Scan ID not found"}), 404
    return jsonify(scan)

if __name__ == "__main__":
    # Run locally on port 5000
    app.run(host="127.0.0.1", port=5000, debug=True)