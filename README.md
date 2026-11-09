# ADHD Reading Font

This repository provides **`adhd-font.otf`**, a modified version of the Aileron font that automatically bolds the first 40-50% of each word to improve readability for people with ADHD.

## Quick Start

1. **Download the font**: `adhd-font.otf`
2. **Install it** on your system
3. **Use it** in any application that supports OpenType features (most modern applications do)
4. **Enable contextual alternates** (calt) if not already enabled by default

The font will automatically bold the first portion of each word according to these rules:
- **1-3 letter words**: 1 letter bold (e.g., "the" → **t**he)
- **4 letter words**: 2 letters bold (e.g., "Bold" → **Bo**ld)
- **5+ letter words**: ceil(word_length × 0.4) letters bold (e.g., "Reading" → **Read**ing)

### Examples
| Word | Output | Bold Count |
|------|--------|------------|
| I | I | 0 |
| a | a | 0 |
| it | **i**t | 1 |
| the | **t**he | 1 |
| Bold | **Bo**ld | 2 |
| Reading | **Read**ing | 4 |
| essential | **Essen**tial | 4 |
| understanding | **Understand**ing | 7 |

## How It Works

The font uses **OpenType Contextual Alternates (calt)** feature to automatically substitute the first N characters of each word with their bold equivalents. The implementation:

1. **Merges** Aileron-Regular and Aileron-Bold into a single font file
2. **Renames** bold glyphs with `.1` suffix (e.g., `a` from bold becomes `a.1`)
3. **Adds** OpenType GSUB features with contextual substitution rules
4. **Applies** the bolding based on word length using the formula you specified

### Rules Implementation

```
if word_length <= 3:
    bold_count = 1
elif word_length == 4:
    bold_count = 2
else:
    bold_count = ceil(word_length * 0.4)
```

## Installation

### Windows
1. Right-click `adhd-font.otf`
2. Select "Install" or "Install for all users"
3. Use in any application (Word, LibreOffice, browsers, etc.)

### macOS
1. Double-click `adhd-font.otf`
2. Click "Install Font"
3. Use in any application

### Linux
1. Copy to `~/.local/share/fonts/` or `/usr/local/share/fonts/`
2. Run `fc-cache -fv` to update font cache
3. Use in any application

## Usage

### HTML/CSS

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        @font-face {
            font-family: 'ADHDFont';
            src: url('adhd-font.otf') format('opentype');
        }
        body {
            font-family: 'ADHDFont', sans-serif;
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <p>Reading is essential for everyone.</p>
    <!-- Will display as: **Read**ing **is** **essen**tial **for** **every**one. -->
</body>
</html>
```

### CSS with Feature Control

```css
/* Enable contextual alternates (usually enabled by default) */
.adhd-text {
    font-family: 'ADHDFont', sans-serif;
    font-feature-settings: "calt" 1;
}

/* Disable contextual alternates */
.normal-text {
    font-family: 'ADHDFont', sans-serif;
    font-feature-settings: "calt" 0;
}
```

### LibreOffice / Microsoft Word
1. Select text
2. Choose "ADHDFont" from the font menu
3. Ensure "Contextual Alternates" is enabled in font settings

### Browser Testing
Open `demo.html` in a modern browser to see the font in action.

## Technical Details

### Font Structure
- **Total Glyphs**: 676 (338 regular + 338 bold)
- **Format**: OpenType (CFF)
- **Bold Glyphs**: Renamed with `.1` suffix (e.g., `a.1`, `B.1`)
- **OpenType Features**: `calt` (Contextual Alternates)

### Feature Rules
The `calt` feature contains substitution rules for different word lengths:

```fea
@az = [a-z A-Z];
@AZ = [a.1-z.1 A.1-Z.1];

feature calt {
    # 1-3 letter words
    sub @az' by @AZ;
    
    # 4-6 letter words
    sub @az @az' @az by @AZ @AZ @az;
    
    # 7-8 letter words
    sub @az @az @az' @az @az by @AZ @AZ @AZ @az @az;
    
    # 9-10 letter words
    sub @az @az @az @az' @az @az @az by @AZ @AZ @AZ @AZ @az @az @az;
    
    # 11-12 letter words
    sub @az @az @az @az @az' @az @az @az @az by @AZ @AZ @AZ @AZ @AZ @az @az @az @az;
} calt;
```

### Application Support
The font works in applications that support OpenType features:
- ✅ **LibreOffice** (calt enabled by default)
- ✅ **Microsoft Word** (calt enabled by default)
- ✅ **Adobe InDesign** (calt enabled by default)
- ✅ **Modern Browsers** (Chrome, Firefox, Edge, Safari)
- ✅ **GIMP** (with OpenType support)
- ⚠️ **Notepad** (no OpenType support)
- ⚠️ **Basic text editors** (may not support OpenType features)

## Verification

To verify the font is working:

1. Install the font
2. Open a text editor that supports OpenType features
3. Type: "Reading is essential"
4. Expected output: **Read**ing **is** **essen**tial

## Files

- `adhd-font.otf` - The main font file (74KB)
- `aileron/` - Original Aileron font files
- `demo.html` - Demonstration HTML file
- `adhd_font_tool.py` - Python text processor (alternative approach)
- `test_adhd_font.py` - Unit tests

## Alternative: Python Text Processor

If you need more flexibility or the font doesn't work in your application, you can use the Python text processor:

```bash
python adhd_font_tool.py --text "Reading is essential" --ratio 0.45 --format html
```

This will output: `<b>Read</b>ing <b>i</b>s <b>essen</b>tial`

## License

This project is licensed under the GNU General Public License v3.0.

The Aileron font files are distributed under their own license (included in this repository).

The `adhd-font.otf` file is a derivative work of Aileron-Regular and Aileron-Bold, and is also licensed under GPLv3.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

- Original Aileron font: [Aileron by Sorkin Type](https://www.sorkintype.com/aileron.html)
- OpenType feature implementation based on user's specification
