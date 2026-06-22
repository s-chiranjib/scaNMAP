import nmap
import datetime
import os

class NetGuardianScanner:
    def __init__(self, target):
        self.target = target
        # Initialize the Nmap PortScanner
        self.nm = nmap.PortScanner()
        # Module 2: Target specific common ports defined in the requirements
        self.target_ports = '21,22,23,25,53,80,110,143,443,3306,3389'
        self.results = []

    def assess_risk(self, port, service_name):
        """
        Module 5: Risk Assessment with simple recommendations.
        Analyzes the port and assigns a risk level and mitigation strategy.
        """
        port = int(port)
        if port in [21, 23]: # FTP and Telnet
            return "High", "Cleartext protocol detected. Highly vulnerable to sniffing. Disable and use secure alternatives like SFTP or SSH."
        elif port in [25, 110, 143]: # Email ports without guaranteed SSL
            return "Medium", "Ensure these mail protocols are configured to enforce TLS/SSL encryption."
        elif port == 80: # HTTP
            return "Medium", "Unencrypted web traffic. Enforce HTTPS (Port 443) to secure data in transit."
        elif port in [3306, 3389]: # Database and RDP
            return "High", "Database or Remote Desktop exposed to the network. Restrict access using Firewalls or a VPN."
        else:
            return "Low", "Standard secure or essential service. Ensure the software version is up-to-date to prevent zero-day exploits."

    def run_scan(self):
        """
        Modules 3 & 4: Service Detection and Enumeration.
        Uses the -sV flag in Nmap to probe open ports to determine service/version info.
        """
        try:
            # -sV: Probe open ports to determine service/version info
            self.nm.scan(self.target, self.target_ports, arguments='-sV')
            
            # Parse the Nmap output
            for host in self.nm.all_hosts():
                for proto in self.nm[host].all_protocols():
                    ports = self.nm[host][proto].keys()
                    for port in sorted(ports):
                        state = self.nm[host][proto][port]['state']
                        
                        # Only process open ports for enumeration
                        if state == 'open':
                            service = self.nm[host][proto][port]['name']
                            version = self.nm[host][proto][port]['version']
                            # If Nmap can't find a version, provide a placeholder
                            if not version:
                                version = "Version hidden/Unknown"
                                
                            risk_level, recommendation = self.assess_risk(port, service)
                            
                            self.results.append({
                                'port': port,
                                'state': state,
                                'service': service,
                                'version': version,
                                'risk': risk_level,
                                'recommendation': recommendation
                            })
            return True
        except Exception as e:
            print(f"An error occurred during scanning: {e}")
            return False

    def generate_txt_report(self):
        """
        Module 6: Report Generation in TXT format.
        Creates a time-stamped text file detailing the vulnerabilities found.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"NetGuardian_Report_{self.target}_{timestamp}.txt"
        
        with open(filename, 'w') as file:
            file.write("="*50 + "\n")
            file.write(f"NETGUARDIAN VULNERABILITY REPORT\n")
            file.write(f"Target: {self.target}\n")
            file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("="*50 + "\n\n")
            
            if not self.results:
                file.write("No open ports found or target unreachable.\n")
            else:
                for item in self.results:
                    file.write(f"Port: {item['port']}/tcp ({item['state']})\n")
                    file.write(f"Service: {item['service']} (Version: {item['version']})\n")
                    file.write(f"Risk Level: {item['risk']}\n")
                    file.write(f"Recommendation: {item['recommendation']}\n")
                    file.write("-" * 50 + "\n")
                    
        return filename