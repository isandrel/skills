import markdown
import sys
import os

def convert_md_to_html(md_text, template_path):
    # Convert Markdown to HTML
    html_content = markdown.markdown(md_text, extensions=['extra', 'codehilite'])
    
    # Read template
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Inject content
    final_html = template.replace('{{content}}', html_content)
    return final_html

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <markdown_file> [template_file]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    template_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), '../references/email_template.html')
    
    with open(md_file, 'r') as f:
        md_text = f.read()
    
    html_output = convert_md_to_html(md_text, template_file)
    print(html_output)
