
# scaNMAP
### Local Web-Based Zenmap Clone

**scaNMAP** is a locally hosted, web-based graphical interface for the Nmap Security Scanner. It simplifies network reconnaissance by allowing users to scan authorized targets, inspect open ports, view scan results, and maintain scan history through a browser-based interface.

**Developed by:** Chiranjib Swain

## 📖 Project Overview

Traditional Nmap scanning is performed through command-line instructions. scaNMAP provides a graphical web interface that makes network scanning easier for beginners, students, and cybersecurity enthusiasts.

The application is designed for local execution and supports user authentication, predefined scan profiles, background scanning, and persistent scan history.

By combining Python, Flask, Nmap, JavaScript, and SQLite, scaNMAP brings essential network reconnaissance functions into a single interface.

## 🎯 Objectives

- Simplify network scanning through a web-based graphical interface.
- Identify active hosts and examine open ports.
- Inspect detected services and available scan information.
- Provide predefined Nmap scanning profiles.
- Maintain historical scan records.
- Support user authentication and session management.
- Help beginners understand network reconnaissance and security auditing.

## ✨ Key Features

- **User Authentication:** Registration and login with password hashing.
- **Network Scanning:** Scan authorized IP addresses and hostnames using Nmap.
- **Scan Profiles:** Preconfigured Stealth, Intense, Ping Sweep, and Vulnerability Script scans.
- **Background Execution:** Run scans asynchronously to keep the interface responsive.
- **Scan Results:** Display parsed scanning results through the web interface.
- **Scan History:** Store and revisit previous scan records.
- **Local Execution:** Designed to run on the user's own computer.
- **Database Integration:** Store user information and scan history using SQLite.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| Flask | Web server and API endpoints |
| Nmap | Network scanning engine |
| python-nmap | Python interface for Nmap |
| HTML5 | Webpage structure |
| CSS3 | Interface styling |
| JavaScript (ES6) | Frontend interactions |
| SQLite3 | Local database |
| Werkzeug | Password hashing utilities |

## 🏗️ System Architecture

scaNMAP follows a local client-server architecture in which the browser communicates with a Python Flask backend.

```text
                 USER
                   |
                   v
              WEB BROWSER
                   |
                   v
                FRONTEND
           HTML + CSS + JavaScript
                   |
                   v
              FLASK BACKEND
                   |
          +--------+--------+
          |                 |
          v                 v
   AUTHENTICATION      SCAN MANAGER
                            |
                            v
                       NMAP ENGINE
                            |
                            v
                       SCAN RESULTS
                            |
                            v
                      SQLITE DATABASE
                            |
                            v
                    SCAN HISTORY
```

### Architecture Components

- **Frontend:** Provides the interface for authentication, scan configuration, and results.
- **Backend:** Processes requests, manages sessions, and coordinates scanning operations.
- **Scanner Engine:** Executes Nmap through the python-nmap wrapper.
- **Database:** Stores user information and historical scan records.

## 💻 System Requirements

- Python 3.7 or higher.
- Nmap installed on the system.
- pip package manager.
- A modern web browser.
- Windows, Linux, or macOS.

A currently supported Python version is recommended where compatible with the project dependencies.

## 🚀 Installation and Setup

### Step 1: Install Nmap

Download Nmap from the official website:

https://nmap.org/download.html

Verify the installation:

```bash
nmap --version
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/JohnJoseph2007/scaNMAP.git
cd scaNMAP
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Alternatively, on Linux or macOS:

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

If the repository contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the documented dependencies:

```bash
pip install Flask python-nmap werkzeug
```

**Note:** Installing `python-nmap` does not install the Nmap executable itself. Nmap must be installed separately.

### Step 5: Run the Application

If `app.py` is the application entry point, run:

```bash
python app.py
```

Follow the repository's instructions if a different entry point is used.

Some scanning operations require additional privileges. Configure these permissions carefully rather than running the entire web server as an administrator.

### Step 6: Open the Application

Open the following address in your browser:

http://127.0.0.1:5000/

The application should be available if the server is running on that address and port.

## 🔄 Application Workflow

1. Open the application in a web browser.
2. Register a new account or log in.
3. Enter an authorized target IP address or hostname.
4. Select the desired scan profile.
5. Start the scan.
6. The backend initiates the scanning operation.
7. The frontend checks the scan status.
8. View the results after the scan completes.
9. Review previous scans through the history section.

## 🔍 Available Scan Profiles

| Scan Profile | Description |
|---|---|
| Stealth Scan | Uses a TCP SYN scanning technique when supported. |
| Intense Scan | Collects detailed host and service information. |
| Ping Sweep | Checks for responsive hosts in a specified network range. |
| Vulnerability Scripts | Runs selected Nmap scripts to investigate particular security issues. |

The available options and required privileges depend on the implementation, operating system, and network configuration.

## 🗄️ Database Design

The project documentation describes a local SQLite database named `zenmap_local.db`.

### Users Table

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Auto-incrementing user identifier |
| `username` | TEXT | Unique username |
| `password_hash` | TEXT | Hashed password |

### Scans Table

| Column | Type | Description |
|---|---|---|
| `id` | TEXT | Unique scan identifier |
| `username` | TEXT | Associated username |
| `target` | TEXT | Scanned IP address or hostname |
| `arguments` | TEXT | Nmap options used |
| `status` | TEXT | Running, completed, or failed |
| `results` | TEXT | Scan output stored as JSON text |

## 🔌 API Endpoints

The documented API endpoints allow the frontend to communicate with the backend.

### Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth` | Register or log in |
| POST | `/api/logout` | End the current session |
| GET | `/api/user` | Retrieve current user information |

### Scanning and History

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/scan` | Start a new scan |
| GET | `/api/scan/<scan_id>` | Check scan status or retrieve results |
| GET | `/api/history` | Retrieve the logged-in user's scan history |

These endpoints describe the documented interface. Actual request formats and behavior depend on the source code.

## 📊 Result Analysis

scaNMAP is designed to help users:

- Identify responsive hosts.
- Examine open ports where scan results permit.
- Discover services running on target systems.
- Review scan results through a graphical interface.
- Track the status of scanning operations.
- Access previously stored scan records.
- Organize and revisit historical scan information.

Results depend on target availability, firewall configurations, network restrictions, and selected scanning options.

An open port does not necessarily indicate a security vulnerability. Further investigation may be required.

## ✅ Advantages

- Beginner-friendly graphical interface.
- Reduces the need to memorize Nmap commands.
- Organizes scan results in one place.
- Provides predefined scanning profiles.
- Supports persistent scan history.
- Combines web development, Python programming, and network security concepts.
- Useful for learning network reconnaissance and cybersecurity fundamentals.

## ⚠️ Limitations

- Designed primarily for local execution.
- Some scanning techniques require additional privileges.
- Network restrictions can limit scan accuracy.
- Vulnerability scripts may produce false positives.
- Background threads alone do not guarantee reliable scan management after a server restart.
- Application security depends on proper authentication, session management, input validation, and access controls.

## 🔐 Security and Ethical Use

scaNMAP is intended for educational purposes, authorized network reconnaissance, and security auditing.

- Scan only systems you own or have explicit permission to test.
- Do not expose the development server to untrusted networks.
- Avoid unnecessary administrator or root privileges.
- Validate scan inputs and prevent unauthorized command execution.
- Protect user sessions and restrict access to scan records.
- Review scan scripts before running them against production systems.

## 🔮 Future Enhancements

Potential improvements include:

- Live scan progress indicators.
- Exportable scan reports in PDF or CSV format.
- Improved host and port visualization.
- Additional configurable scan profiles.
- Better error handling and logging.
- Stronger authentication and access controls.
- Automated report generation.
- A production-ready deployment configuration.

## 📝 Conclusion

scaNMAP aims to make Nmap network scanning more accessible through a local web-based graphical interface.

By combining Flask, Python, Nmap, JavaScript, and SQLite, the project brings network scanning, result visualization, user authentication, and historical records into one application.

It serves as a practical learning project for understanding web application development, network reconnaissance, and cybersecurity fundamentals.

---

## 👨‍💻 Author

**Chiranjib Swain**

Cybersecurity Enthusiast | Student Developer

I worked on scaNMAP as a cybersecurity learning project focused on simplifying network scanning through a local web-based graphical interface.

### Skills & Technologies

- Python and Flask
- Nmap and Network Scanning
- HTML, CSS, and JavaScript
- SQLite Database
- Cybersecurity and Ethical Hacking

---

## ⚖️ Disclaimer

This project is intended for educational purposes and authorized security testing only. Users are responsible for ensuring that their scanning activities comply with applicable laws and permissions.
