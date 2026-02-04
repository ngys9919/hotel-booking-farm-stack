import markdown
import sys

def convert_md_to_html(md_file, html_file, title):
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Authentication Test Plan</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 2px solid #ecf0f1; padding-bottom: 8px; }}
        h3 {{ color: #7f8c8d; margin-top: 20px; }}
        code {{
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            color: inherit;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #bdc3c7;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #ecf0f1;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin-left: 0;
            color: #7f8c8d;
            font-style: italic;
        }}
        .nav {{
            background: #2c3e50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .nav a {{
            color: #3498db;
            text-decoration: none;
            margin-right: 20px;
        }}
        .nav a:hover {{
            color: #5dade2;
        }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="index.html">← Home</a>
        <a href="test-plan.html">Test Plan</a>
        <a href="security-vulnerabilities.html">Security</a>
        <a href="test-execution-report.html">Report</a>
        <a href="https://github.com/ngys9919/hotel-booking-farm-stack" target="_blank">GitHub →</a>
    </div>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""
    
    with open(html_file, 'w') as f:
        f.write(full_html)

convert_md_to_html('test-plan.md', 'test-plan.html', 'Test Plan')
convert_md_to_html('security-vulnerabilities.md', 'security-vulnerabilities.html', 'Security Vulnerabilities')
convert_md_to_html('test-execution-report.md', 'test-execution-report.html', 'Test Execution Report')
print("Conversion complete!")
