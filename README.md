# ADHD Reading Font Tool

This tool applies bold formatting to the first 40-50% of each word to improve readability for people with ADHD. It uses the Aileron font family and follows specific rules for different word lengths.

## Features

- **Percentage-based bolding**: Bolds approximately 40-50% of each word using a ceiling function
- **Smart word handling**: Special rules for short words (1-3 letters)
- **Multiple output formats**: HTML, Markdown, ANSI, and RTF
- **Aileron font support**: Designed to work with the Aileron font family

## Rules

The algorithm follows these rules:

1. **1-letter words** (like "I" or "a"): Left unbolded
2. **2-3 letter words** (like "it" or "the"): Bold just 1 letter
3. **4+ letter words**: Use percentage-based calculation: `ceil(word_length * fixation_ratio)`

### Examples at 50% ratio:
- "Reading" (7 letters): 7 × 0.5 = 3.5 → ceil(3.5) = 4 → **Read**ing
- "Bold" (4 letters): 4 × 0.5 = 2 → ceil(2) = 2 → **Bo**ld
- "the" (3 letters): 1 letter bold → **t**he
- "a" (1 letter): unbolded → a

## Installation

```bash
# Clone the repository
git clone https://github.com/alexbrandsen/adhd-reading-font.git
cd adhd-reading-font

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Process text directly
python adhd_font_tool.py --text "Reading is essential" --ratio 0.45

# Process a file
python adhd_font_tool.py --file input.txt --output output.html --ratio 0.45

# Run demonstration
python adhd_font_tool.py --demo

# Available formats: html, markdown, ansi, rtf
python adhd_font_tool.py --text "Hello world" --format markdown --ratio 0.5
```

### Python API

```python
from adhd_font_tool import process_text, calculate_bold_length

# Process text
text = "Reading is an essential skill"
formatted = process_text(text, fixation_ratio=0.45, output_format='html')
print(formatted)

# Calculate bold length for a word
bold_len = calculate_bold_length("Reading", 0.5)  # Returns 4
```

## Output Formats

### HTML
Converts text with `<b>` tags:
```html
<b>Read</b>ing <b>is</b> <b>an</b> <b>essen</b>tial <b>skil</b>l
```

### Markdown
Converts text with `**` syntax:
```markdown
**Read**ing **is** **an** **essen**tial **skil**l
```

### ANSI
Uses ANSI escape codes for terminal output:
```
\[1mRead\[0m ing \[1mis\[0m ...
```

### RTF
Creates RTF format with Aileron font references:
```rtf
{\rtf1\ansi\deff0{\fonttbl{\f0 Aileron-Regular;}{\f1 Aileron-Bold;}}\f0\fs24 {\b\f1 Read}\b0\f0 ing {\b\f1 is}\b0\f0 ...}
```

## Using with Aileron Font

To use this tool with the Aileron font in your applications:

### HTML/CSS Example

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        @font-face {
            font-family: 'Aileron';
            src: url('aileron/Aileron-Regular.otf') format('opentype');
            font-weight: normal;
        }
        @font-face {
            font-family: 'Aileron';
            src: url('aileron/Aileron-Bold.otf') format('opentype');
            font-weight: bold;
        }
        body {
            font-family: 'Aileron', sans-serif;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <p><b>Read</b>ing <b>is</b> <b>an</b> <b>essen</b>tial <b>skil</b>l</p>
</body>
</html>
```

### CSS with Custom Bold Ratio

You can also use CSS to style the bold parts:

```css
.adhd-text b {
    font-family: 'Aileron-Bold', sans-serif;
    font-weight: bold;
}
.adhd-text {
    font-family: 'Aileron-Regular', sans-serif;
}
```

## Fixation Ratio

The fixation ratio determines what percentage of each word should be bolded:

- **0.4** (40%): More subtle, bolds fewer characters
- **0.45** (45%): Balanced approach
- **0.5** (50%): More pronounced, bolds approximately half of each word

Experiment with different ratios to find what works best for your needs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

The Aileron font files are distributed under their own license (included in this repository).

## Examples

### Input:
```
Reading is an essential skill for everyone.
```

### Output at 50% ratio (HTML):
```html
<b>Read</b>ing <b>is</b> <b>an</b> <b>essen</b>tial <b>skil</b>l <b>for</b> <b>every</b>one.
```

### Output at 40% ratio (Markdown):
```markdown
**Rea**ding **is** **a** **esse**ntial **ski**ll **for** **ever**yone.
```

## Technical Details

The algorithm uses Python's `math.ceil()` function to round up to the nearest whole number, ensuring that we always bold at least the calculated percentage of each word.

For words with 4+ letters:
```python
bold_count = math.ceil(word_length * fixation_ratio)
```

This ensures consistent and predictable results across all word lengths.
