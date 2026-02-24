"""
Generates a visual HTML report for plagiarism analysis.
Makes the demo look polished and professional.
"""

from code_analyzer import PlagiarismDetector
import datetime

def read_file(filename):
    """Read code file safely"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"# Error reading file: {e}"

def escape_html(text):
    """Basic HTML escaping for code display"""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))

def generate_html_report(result, code1, code2):
    """Creates a beautiful HTML report"""
    
    # determine color based on similarity score
    score = result['scores']['overall'] * 100
    if score >= 85:
        color = "#ef4444"  # red
        bg_color = "#fef2f2"
    elif score >= 65:
        color = "#f59e0b"  # orange
        bg_color = "#fffbeb"
    elif score >= 40:
        color = "#eab308"  # yellow
        bg_color = "#fefce8"
    else:
        color = "#10b981"  # green
        bg_color = "#f0fdf4"
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CodeClone Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f8fafc;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 16px;
        }}
        
        .verdict-box {{
            background: {bg_color};
            border-left: 5px solid {color};
            padding: 30px;
            margin: 30px;
            border-radius: 8px;
        }}
        
        .verdict-box h2 {{
            color: {color};
            font-size: 24px;
            margin-bottom: 15px;
        }}
        
        .score-main {{
            font-size: 48px;
            font-weight: 700;
            color: {color};
            margin: 10px 0;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8fafc;
        }}
        
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .metric-label {{
            color: #64748b;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-value {{
            font-size: 28px;
            font-weight: 600;
            color: #1e293b;
        }}
        
        .metric-bar {{
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .metric-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 3px;
            transition: width 0.3s ease;
        }}
        
        .code-comparison {{
            padding: 30px;
        }}
        
        .code-section {{
            margin-bottom: 30px;
        }}
        
        .code-section h3 {{
            color: #1e293b;
            margin-bottom: 15px;
            font-size: 18px;
            display: flex;
            align-items: center;
        }}
        
        .code-section h3::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 20px;
            background: #667eea;
            margin-right: 10px;
            border-radius: 2px;
        }}
        
        pre {{
            background: #1e293b;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
            background: white;
        }}
        
        .stat-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px;
            background: #f8fafc;
            border-radius: 6px;
        }}
        
        .stat-label {{
            color: #64748b;
            font-weight: 500;
        }}
        
        .stat-value {{
            color: #1e293b;
            font-weight: 600;
        }}
        
        .footer {{
            background: #f8fafc;
            padding: 20px;
            text-align: center;
            color: #64748b;
            font-size: 14px;
        }}
        
        .timestamp {{
            margin-top: 10px;
            font-size: 13px;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 CodeClone Analysis Report</h1>
            <p>Advanced Code Plagiarism Detection System</p>
        </div>
        
        <div class="verdict-box">
            <h2>Analysis Result</h2>
            <div class="score-main">{score:.1f}%</div>
            <p style="font-size: 18px; margin-top: 10px;">{result['verdict']}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Function Structure</div>
                <div class="metric-value">{result['scores']['function_similarity']*100:.1f}%</div>
                <div class="metric-bar">
                    <div class="metric-bar-fill" style="width: {result['scores']['function_similarity']*100}%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Control Flow Logic</div>
                <div class="metric-value">{result['scores']['control_flow_similarity']*100:.1f}%</div>
                <div class="metric-bar">
                    <div class="metric-bar-fill" style="width: {result['scores']['control_flow_similarity']*100}%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Operation Patterns</div>
                <div class="metric-value">{result['scores']['operation_similarity']*100:.1f}%</div>
                <div class="metric-bar">
                    <div class="metric-bar-fill" style="width: {result['scores']['operation_similarity']*100}%"></div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Exact Structure Match</div>
                <div class="metric-value">{result['scores']['structure_match']*100:.1f}%</div>
                <div class="metric-bar">
                    <div class="metric-bar-fill" style="width: {result['scores']['structure_match']*100}%"></div>
                </div>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-label">{result['file1']} - Functions</span>
                <span class="stat-value">{result['details']['file1_functions']}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">{result['file2']} - Functions</span>
                <span class="stat-value">{result['details']['file2_functions']}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">{result['file1']} - Control Structures</span>
                <span class="stat-value">{result['details']['file1_control_structures']}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">{result['file2']} - Control Structures</span>
                <span class="stat-value">{result['details']['file2_control_structures']}</span>
            </div>
        </div>
        
        <div class="code-comparison">
            <div class="code-section">
                <h3>File 1: {result['file1']}</h3>
                <pre><code>{escape_html(code1)}</code></pre>
            </div>
            
            <div class="code-section">
                <h3>File 2: {result['file2']}</h3>
                <pre><code>{escape_html(code2)}</code></pre>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>CodeClone</strong> - Intelligent Code Plagiarism Detection</p>
            <p class="timestamp">Generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Generate HTML reports for all test cases"""
    
    print("Generating HTML reports...\n")
    
    detector = PlagiarismDetector()
    
    # Test 1: Plagiarized code
    code1 = read_file('original.py')
    code2 = read_file('plagiarized.py')
    
    result1 = detector.analyze_pair(code1, code2, 'original.py', 'plagiarized.py')
    
    html1 = generate_html_report(result1, code1, code2)
    with open('report_plagiarized.html', 'w', encoding='utf-8') as f:
        f.write(html1)
    print("✓ Created report_plagiarized.html")
    
    # Test 2: Different code
    code3 = read_file('different.py')
    
    result2 = detector.analyze_pair(code1, code3, 'original.py', 'different.py')
    
    html2 = generate_html_report(result2, code1, code3)
    with open('report_different.html', 'w', encoding='utf-8') as f:
        f.write(html2)
    print("✓ Created report_different.html")
    
    print("\n" + "="*60)
    print("HTML reports generated successfully!")
    print("Open these files in your browser to see visual reports:")
    print("  • report_plagiarized.html (should show ~90% similarity)")
    print("  • report_different.html (should show ~27% similarity)")
    print("="*60)

if __name__ == "__main__":
    main()