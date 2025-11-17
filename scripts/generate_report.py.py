#!/usr/bin/env python3
"""
Generate HTML report from TrueClient execution results
"""
import json
import os
from datetime import datetime

def generate_html_report():
    """Generate HTML report from execution results"""
    
    # Find the latest results file
    results_files = [f for f in os.listdir('results') if f.startswith('trueclient_results')]
    if not results_files:
        print("No results files found")
        return
    
    latest_file = sorted(results_files)[-1]
    results_path = os.path.join('results', latest_file)
    
    with open(results_path, 'r') as f:
        results = json.load(f)
    
    # Generate HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TrueClient Execution Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: #f4f4f4; padding: 20px; border-radius: 5px; }}
            .transaction {{ margin: 10px 0; padding: 10px; border-left: 4px solid #4CAF50; background: #f9f9f9; }}
            .transaction.failed {{ border-left-color: #f44336; }}
            .step {{ margin: 5px 0; padding: 5px; font-size: 14px; }}
            .success {{ color: #4CAF50; }}
            .error {{ color: #f44336; }}
            .info {{ color: #2196F3; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>TrueClient Script Execution Report</h1>
            <p><strong>Script:</strong> PetStore Login/Logout</p>
            <p><strong>Start Time:</strong> {results['start_time']}</p>
            <p><strong>End Time:</strong> {results.get('end_time', 'N/A')}</p>
            <p><strong>Status:</strong> {results['status']}</p>
        </div>
        
        <h2>Transaction Summary</h2>
    """
    
    for transaction, details in results['transactions'].items():
        status_class = "" if details['status'] == 'pass' else "failed"
        html_content += f"""
        <div class="transaction {status_class}">
            <h3>{transaction}</h3>
            <p><strong>Status:</strong> {details['status']}</p>
            <p><strong>Duration:</strong> {details['duration_seconds']} seconds</p>
        </div>
        """
    
    html_content += """
        <h2>Step Details</h2>
    """
    
    for step in results['steps']:
        status_class = step['status']
        html_content += f"""
        <div class="step {status_class}">
            <strong>{step['step']}</strong> - {step['status']} at {step['timestamp']}
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    # Save HTML report
    report_path = f"results/execution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    print(f"📊 HTML report generated: {report_path}")

if __name__ == "__main__":
    generate_html_report()