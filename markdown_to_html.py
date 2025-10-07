import markdown
import sys
import os
import glob
import re

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("Warning: weasyprint not available. Install with: pip install weasyprint")

def translate_github_urls(text):
    """Translate GitHub blob URLs to raw URLs for proper image display"""
    # Pattern to match GitHub blob URLs
    pattern = r'https://github\.com/([^/]+/[^/]+)/blob/([^/]+)/(.+)'
    
    def replace_url(match):
        owner_repo = match.group(1)
        branch = match.group(2)
        path = match.group(3)
        return f'https://github.com/{owner_repo}/raw/refs/heads/{branch}/{path}'
    
    # Replace all occurrences
    return re.sub(pattern, replace_url, text)

def convert_markdown_to_html(input_file, output_file=None):
    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    
    # Translate GitHub URLs before processing
    markdown_text = translate_github_urls(markdown_text)
    
    # Convert markdown to HTML with more extensions for better link/image handling
    html = markdown.markdown(markdown_text, extensions=[
        'fenced_code', 
        'codehilite',
        'tables',
        'toc',
        'attr_list',
        'def_list',
        'footnotes',
        'md_in_html',
        'nl2br'
    ])
    
    # Create a complete HTML document
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{os.path.basename(input_file)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: Consolas, Monaco, 'Andale Mono', monospace;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    # Write to output file or print to console
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        print(f"Successfully converted {input_file} to {output_file}")
    else:
        print(html_doc)

def html_to_pdf(html_file, pdf_file):
    """Convert HTML file to PDF using weasyprint"""
    if not WEASYPRINT_AVAILABLE:
        print("Error: weasyprint is required for PDF generation. Install with: pip install weasyprint")
        return False
    
    try:
        # Read the HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Get the directory of the HTML file for base_url
        html_dir = os.path.dirname(os.path.abspath(html_file))
        
        # Convert to PDF using base_url for proper resource resolution
        # This allows WeasyPrint to resolve relative paths correctly
        html_doc = HTML(string=html_content, base_url=f"file://{html_dir}/")
        html_doc.write_pdf(pdf_file)
        print(f"Successfully converted {html_file} to {pdf_file}")
        return True
    except Exception as e:
        print(f"Error converting to PDF: {str(e)}")
        return False

def convert_directory(input_dir='.', output_dir='html', pdf_output=False):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Find all markdown files in the input directory
    md_files = glob.glob(os.path.join(input_dir, '*.md'))
    
    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return
    
    # Convert each markdown file
    for md_file in md_files:
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        # Create output filename
        html_file = os.path.join(output_dir, f"{base_name}.html")
        
        try:
            convert_markdown_to_html(md_file, html_file)
            
            # Convert to PDF if requested
            if pdf_output:
                pdf_file = os.path.join(output_dir, f"{base_name}.pdf")
                html_to_pdf(html_file, pdf_file)
                
        except Exception as e:
            print(f"Error converting {md_file}: {str(e)}")

def convert_to_single_html(input_dir='.', output_file='combined_documentation.html', pdf_output=False):
    # Find all markdown files in the input directory
    md_files = glob.glob(os.path.join(input_dir, '*.md'))
    
    if not md_files:
        print(f"No markdown files found in {input_dir}")
        return
    
    # Sort files for consistent ordering
    md_files.sort()
    
    # Create the HTML document structure
    html_parts = []
    toc_items = []
    
    for i, md_file in enumerate(md_files):
        try:
            # Read the markdown file
            with open(md_file, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            
            # Translate GitHub URLs before processing
            markdown_text = translate_github_urls(markdown_text)
            
            # Convert markdown to HTML with more extensions for better link/image handling
            html_content = markdown.markdown(markdown_text, extensions=[
                'fenced_code', 
                'codehilite',
                'tables',
                'toc',
                'attr_list',
                'def_list',
                'footnotes',
                'md_in_html',
                'nl2br'
            ])
            
            # Create section with anchor
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            section_id = f"section-{i}"
            toc_items.append(f'<li><a href="#{section_id}">{base_name}</a></li>')
            
            html_parts.append(f'''
            <section id="{section_id}">
                <h1>{base_name}</h1>
                <hr>
                {html_content}
            </section>
            ''')
            
        except Exception as e:
            print(f"Error processing {md_file}: {str(e)}")
    
    # Create complete HTML document
    toc_html = '\n'.join(toc_items)
    content_html = '\n'.join(html_parts)
    
    # Use print-friendly CSS for PDF output
    if pdf_output:
        css_styles = """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            font-size: 12pt;
        }
        .toc {
            page-break-after: always;
            margin-bottom: 30px;
        }
        .toc h2 {
            margin-top: 0;
            color: #495057;
            font-size: 18pt;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin: 8px 0;
            font-size: 11pt;
        }
        .toc a {
            text-decoration: none;
            color: #007bff;
        }
        section {
            page-break-before: always;
            margin-bottom: 20px;
        }
        section:first-of-type {
            page-break-before: avoid;
        }
        section h1 {
            color: #495057;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
            font-size: 16pt;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 10pt;
        }
        code {
            font-family: Consolas, Monaco, 'Andale Mono', monospace;
        }
        hr {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 20px 0;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        @page {
            margin: 1in;
        }
        """
    else:
        css_styles = """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .toc {
            position: fixed;
            top: 20px;
            left: 20px;
            width: 250px;
            max-height: 80vh;
            overflow-y: auto;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }
        .toc h2 {
            margin-top: 0;
            color: #495057;
        }
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        .toc li {
            margin: 5px 0;
        }
        .toc a {
            text-decoration: none;
            color: #007bff;
            display: block;
            padding: 5px 10px;
            border-radius: 3px;
            transition: background-color 0.2s;
        }
        .toc a:hover {
            background-color: #e9ecef;
        }
        .content {
            margin-left: 290px;
        }
        section {
            margin-bottom: 40px;
            padding: 20px;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            background: white;
        }
        section h1 {
            color: #495057;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        code {
            font-family: Consolas, Monaco, 'Andale Mono', monospace;
        }
        hr {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 20px 0;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        """
    
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Combined Documentation</title>
    <style>
        {css_styles}
    </style>
</head>
<body>
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
            {toc_html}
        </ul>
    </div>
    <div class="content">
        {content_html}
    </div>
</body>
</html>"""
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_doc)
    print(f"Successfully converted {len(md_files)} markdown files to {output_file}")
    
    # Convert to PDF if requested
    if pdf_output:
        pdf_file = os.path.splitext(output_file)[0] + '.pdf'
        html_to_pdf(output_file, pdf_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Check for flags first
        pdf_output = '--pdf' in sys.argv
        single_output = '--single' in sys.argv
        
        # Remove flags from arguments list for processing
        args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
        
        if single_output:
            # Convert to single HTML file
            input_dir = args[0] if len(args) > 0 else '.'
            output_file = args[1] if len(args) > 1 else 'combined_documentation.html'
            convert_to_single_html(input_dir, output_file, pdf_output)
        elif pdf_output:
            # Convert with PDF output (separate files)
            input_dir = args[0] if len(args) > 0 else '.'
            output_dir = args[1] if len(args) > 1 else 'html'
            convert_directory(input_dir, output_dir, pdf_output=True)
        else:
            # If directory is specified as argument (original behavior)
            input_dir = sys.argv[1]
            output_dir = sys.argv[2] if len(sys.argv) > 2 else 'html'
            convert_directory(input_dir, output_dir)
    else:
        # Default to current directory
        print("Usage:")
        print("  python markdown_to_html.py [directory] [output_directory]  # Convert each MD to separate HTML")
        print("  python markdown_to_html.py --single [directory] [output_file]  # Convert all MD to single HTML")
        print("  python markdown_to_html.py --pdf [directory] [output_directory]  # Convert each MD to HTML + PDF")
        print("  python markdown_to_html.py --single --pdf [directory] [output_file]  # Convert all MD to single HTML + PDF")
        print("\nDefault: Convert each markdown file to separate HTML files in 'html' directory")
        print("\nNote: PDF generation requires weasyprint. Install with: pip install weasyprint")
        convert_directory() 