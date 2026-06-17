#!/usr/bin/env python3
"""
Markdown to HTML Converter
Converts markdown files or stdin to HTML
"""

import sys
import os
import argparse
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Error: python-markdown not installed. Run: pip install markdown")
    sys.exit(1)

def convert_markdown_to_html(markdown_text, extensions=None):
    """Convert markdown text to HTML"""
    if extensions is None:
        extensions = [
            'extra',           # Tables, footnotes, etc.
            'codehilite',      # Code highlighting
            'toc',            # Table of contents
            'tables',         # Tables
            'fenced_code',    # Fenced code blocks
            'smarty'          # Smart quotes/punctuation
        ]
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text, extensions=extensions)
    
    return html

def create_full_html(content, title="Markdown Document", css_style=None):
    """Wrap HTML content in a complete HTML document"""
    
    default_css = """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        pre {
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow-x: auto;
        }
        code {
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 2px 4px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        blockquote {
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 16px;
            color: #666;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
    """
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css_style if css_style else default_css}
</head>
<body>
{content}
</body>
</html>"""
    
    return html_template

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML')
    parser.add_argument('input', nargs='?', help='Input markdown file (default: stdin)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: stdout)')
    parser.add_argument('-t', '--title', default='Markdown Document', help='HTML title')
    parser.add_argument('-c', '--css', help='External CSS file to include')
    parser.add_argument('-f', '--full', action='store_true', default=True, 
                       help='Generate complete HTML document (default: True)')
    parser.add_argument('-r', '--raw', action='store_true', 
                       help='Output raw HTML fragment only')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    else:
        markdown_text = sys.stdin.read()
    
    if not markdown_text:
        print("Error: No input provided", file=sys.stderr)
        sys.exit(1)
    
    # Convert to HTML
    try:
        html_content = convert_markdown_to_html(markdown_text)
    except Exception as e:
        print(f"Error converting markdown: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Wrap in full HTML if requested
    if not args.raw and args.full:
        css_content = None
        if args.css:
            with open(args.css, 'r') as f:
                css_content = f"<style>{f.read()}</style>"
        
        output_html = create_full_html(html_content, args.title, css_content)
    else:
        output_html = html_content
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_html)
        print(f"Converted to {args.output}", file=sys.stderr)
    else:
        print(output_html)

if __name__ == "__main__":
    main()