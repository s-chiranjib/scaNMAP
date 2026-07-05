import threading
import uuid
import json
import os
from flask import Flask, jsonify, render_template, request
import nmap
import sqlite3
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "local_only_secret_key_change_me" # Enables cookies/sessions
DB_FILE = "zenmap_local.db"

def init_db():
    """Creates tables if they don't exist yet."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                target TEXT NOT NULL,
                arguments TEXT NOT NULL,
                status TEXT NOT NULL,
                results TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        conn.commit()

init_db()

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

def execute_nmap_scan(scan_id, username, target, arguments):
    """Background worker that runs Nmap and parses results into SQLite."""
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
                for port in nm[host][proto].keys():
                    port_info = nm[host][proto][port]
                    host_data["protocols"][proto].append({
                        "port": port, "state": port_info["state"],
                        "name": port_info["name"], "product": port_info.get("product", ""),
                        "version": port_info.get("version", "")
                    })
            scan_results.append(host_data)

        # Save Success to DB
        with sqlite3.connect(DB_FILE) as conn:
            conn.cursor().execute(
                "INSERT OR REPLACE INTO scans VALUES (?, ?, ?, ?, ?, ?)",
                (scan_id, username, target, arguments, "completed", json.dumps(scan_results))
            )
        scans[scan_id] = {"status": "completed", "results": scan_results}

    except Exception as e:
        # Save Failure to DB
        with sqlite3.connect(DB_FILE) as conn:
            conn.cursor().execute(
                "INSERT OR REPLACE INTO scans VALUES (?, ?, ?, ?, ?, ?)",
                (scan_id, username, target, arguments, "failed", json.dumps({"error": str(e)}))
            )
        scans[scan_id] = {"status": "failed", "error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/scan", methods=["POST"])
def start_scan():
    username = session.get("username")
    if not username:
        return jsonify({"error": "You must be logged in to scan."}), 401

    data = request.json or {}
    target = data.get("target", "127.0.0.1")
    scan_type = data.get("type", "stealth")

    scan_profiles = {
        "stealth": "-sS -sV -O -T4",
        "intense": "-T4 -A -v",
        "ping_sweep": "-sn",
        "vuln": "-sV --script vuln"
    }
    arguments = scan_profiles.get(scan_type, "-sS")

    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "results": []}

    # Pass 'username' into the background execution thread
    thread = threading.Thread(target=execute_nmap_scan, args=(scan_id, username, target, arguments))
    thread.start()

    return jsonify({"scan_id": scan_id, "status": "running"})

@app.route("/api/scan/<scan_id>", methods=["GET"])
def get_scan_status(scan_id):
    scan = scans.get(scan_id)
    if not scan:
        return jsonify({"error": "Scan ID not found"}), 404
    return jsonify(scan)

@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.json or {}
    username, password, action = data.get("username"), data.get("password"), data.get("action")
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        if action == "register":
            try:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                               (username, generate_password_hash(password)))
                conn.commit()
                session["username"] = username
                return jsonify({"username": username})
            except sqlite3.IntegrityError:
                return jsonify({"error": "User already exists"}), 400
        else: # login
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row and check_password_hash(row[0], password):
                session["username"] = username
                return jsonify({"username": username})
            return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"status": "logged_out"})

@app.route("/api/user", methods=["GET"])
def check_user():
    return jsonify({"username": session.get("username")})

@app.route("/api/history", methods=["GET"])
def get_history():
    username = session.get("username")
    if not username: return jsonify([]), 401
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, arguments, status, results FROM scans WHERE username = ? ORDER BY rowid DESC", (username,))
        return jsonify([{"scan_id": r[0], "target": r[1], "arguments": r[2], "status": r[3], "results": json.loads(r[4])} for r in cursor.fetchall()])

if __name__ == "__main__":
    # Run locally on port 5000
    app.run(host="127.0.0.1", port=5000, debug=True)