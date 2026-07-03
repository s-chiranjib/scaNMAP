import nmap

# Initialize the PortScanner
nm = nmap.PortScanner()

# Define the target and port range to scan
target = '172.16.16.138'
ports = '22-80'

# Run the nmap scan (using 'sV' for version detection as an example argument)
print(f"Scanning {target}...")
nm.scan(target, arguments='-sV')

# Loop through all the hosts found in the scan
for host in nm.all_hosts():
    print(f'----------------------------------------------------')
    print(f'Host : {host} ({nm[host].hostname()})')
    print(f'State : {nm[host].state()}')

    # Loop through the protocols (e.g., tcp, udp)
    for proto in nm[host].all_protocols():
        print(f'----------')
        print(f'Protocol : {proto}')
        
        # Get all ports for this protocol
        lport = nm[host][proto].keys()
        sorted_ports = sorted(lport)
        
        for port in sorted_ports:
            state = nm[host][proto][port]['state']
            name = nm[host][proto][port]['name']
            print(f'port : {port}\tstate : {state}\tservice : {name}')
