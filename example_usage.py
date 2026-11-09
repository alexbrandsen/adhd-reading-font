#!/usr/bin/env python3
"""
Example usage of the ADHD Reading Font Tool

This script demonstrates how to use the tool to format text for better readability.
"""

from adhd_font_tool import process_text

# Sample text
sample_text = """
Reading is an essential skill for everyone. The ability to read well opens 
doors to knowledge and understanding. People with ADHD often find it 
challenging to maintain focus while reading long texts.

This tool applies bold formatting to the first 40-50% of each word, which 
can help improve focus and reading comprehension for individuals with ADHD.
"""

print("=" * 70)
print("ADHD Reading Font Tool - Example Usage")
print("=" * 70)
print()

# Show the original text
print("ORIGINAL TEXT:")
print("-" * 70)
print(sample_text)
print()

# Show formatted text with different ratios
for ratio in [0.4, 0.45, 0.5]:
    print(f"FORMATTED TEXT (Ratio: {ratio}, Bold: {int(ratio*100)}%):")
    print("-" * 70)
    
    # HTML format (for web use)
    html_output = process_text(sample_text.strip(), ratio, 'html')
    print("HTML Output:")
    print(html_output)
    print()
    
    # Markdown format (for documents)
    md_output = process_text(sample_text.strip(), ratio, 'markdown')
    print("Markdown Output:")
    print(md_output)
    print()
    print()

# Example of processing a file
print("PROCESSING A FILE:")
print("-" * 70)
print("To process a file, use:")
print("  python adhd_font_tool.py --file input.txt --output output.html --ratio 0.45")
print()

# Example of using in a web application
print("WEB APPLICATION EXAMPLE:")
print("-" * 70)
print("""
# In your Flask/Django application:
from adhd_font_tool import process_text

@app.route('/format-text')
def format_text_endpoint():
    text = request.args.get('text', '')
    ratio = float(request.args.get('ratio', 0.45))
    formatted = process_text(text, ratio, 'html')
    return render_template('result.html', text=formatted)

# In your HTML template:
# <div class="adhd-text">
#     {{ text | safe }}
# </div>

# In your CSS:
# .adhd-text b {
#     font-family: 'Aileron-Bold', sans-serif;
#     font-weight: bold;
# }
# .adhd-text {
#     font-family: 'Aileron-Regular', sans-serif;
# }
""")

print("=" * 70)
print("For more information, see README.md")
print("=" * 70)
