from flask import Flask, render_template, request, send_file
from scanner import scaNmapScanner
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Module 1: Accept IP Address or Hostname
        target = request.form.get('target')
        
        if not target:
            return render_template('index.html', error="Please enter a valid IP or Hostname.")
        
        # Initialize and run the scanner
        scanner = scaNmapScanner(target)
        success = scanner.run_scan()
        
        if success:
            # Generate the report automatically upon a successful scan
            report_file = scanner.generate_txt_report()
            return render_template('index.html', 
                                   target=target, 
                                   results=scanner.results, 
                                   report_file=report_file)
        else:
            return render_template('index.html', error="Scan failed. Please check the target or ensure Nmap is installed.")

    # Render the default page on a GET request
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app in debug mode for development
    app.run(debug=True)