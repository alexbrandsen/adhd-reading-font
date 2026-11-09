#!/usr/bin/env python3
"""
ADHD Reading Font Tool

This tool applies bold formatting to the first 40-50% of each word to improve
readability for people with ADHD. It follows these rules:

1. For words with 4+ letters: bold ceil(word_length * fixation_ratio) characters
2. For 2-3 letter words: bold just 1 letter
3. For 1-letter words: leave unbolded (or optionally bold completely)

The default fixation ratio is 0.5 (50%), but can be adjusted between 0.4 and 0.5.

Usage:
    python adhd_font_tool.py --text "Your text here" [--ratio 0.45] [--format html|markdown|ansi]
    python adhd_font_tool.py --file input.txt --output output.html
"""

import re
import math
import argparse
from typing import Tuple, List


def calculate_bold_length(word: str, fixation_ratio: float = 0.5) -> int:
    """
    Calculate how many characters should be bolded at the start of a word.
    
    Args:
        word: The word to process
        fixation_ratio: The ratio of the word to bold (0.4 to 0.5)
    
    Returns:
        Number of characters to bold
    """
    length = len(word)
    
    # Handle empty strings
    if length == 0:
        return 0
    
    # 1-letter words: leave unbolded (return 0)
    if length == 1:
        return 0
    
    # 2-3 letter words: bold just 1 letter
    if 2 <= length <= 3:
        return 1
    
    # 4+ letter words: use percentage-based calculation
    bold_count = math.ceil(length * fixation_ratio)
    
    # Ensure at least 1 character is bolded for words >= 2
    return max(1, bold_count)


def process_word(word: str, fixation_ratio: float = 0.5) -> Tuple[str, str]:
    """
    Split a word into bold and regular parts.
    
    Args:
        word: The word to process
        fixation_ratio: The ratio of the word to bold
    
    Returns:
        Tuple of (bold_part, regular_part)
    """
    bold_length = calculate_bold_length(word, fixation_ratio)
    
    if bold_length >= len(word):
        return word, ""
    elif bold_length == 0:
        return "", word
    else:
        return word[:bold_length], word[bold_length:]


def format_text_html(text: str, fixation_ratio: float = 0.5) -> str:
    """
    Format text with HTML bold tags.
    
    Args:
        text: The text to format
        fixation_ratio: The ratio of each word to bold
    
    Returns:
        HTML formatted text
    """
    # Split into words while preserving whitespace and punctuation
    # We want to identify word boundaries but keep punctuation attached
    words = re.findall(r"(\w+|\W+)", text)
    
    result = []
    for word in words:
        # Only process if it's a word (contains alphanumeric characters)
        if re.search(r'\w', word):
            bold_part, regular_part = process_word(word, fixation_ratio)
            if bold_part:
                result.append(f"<b>{bold_part}</b>")
            if regular_part:
                result.append(regular_part)
        else:
            # It's whitespace or punctuation, keep as-is
            result.append(word)
    
    return "".join(result)


def format_text_markdown(text: str, fixation_ratio: float = 0.5) -> str:
    """
    Format text with Markdown bold syntax.
    
    Args:
        text: The text to format
        fixation_ratio: The ratio of each word to bold
    
    Returns:
        Markdown formatted text
    """
    words = re.findall(r"(\w+|\W+)", text)
    
    result = []
    for word in words:
        if re.search(r'\w', word):
            bold_part, regular_part = process_word(word, fixation_ratio)
            if bold_part:
                result.append(f"**{bold_part}**")
            if regular_part:
                result.append(regular_part)
        else:
            result.append(word)
    
    return "".join(result)


def format_text_ansi(text: str, fixation_ratio: float = 0.5) -> str:
    """
    Format text with ANSI escape codes for bold.
    
    Args:
        text: The text to format
        fixation_ratio: The ratio of each word to bold
    
    Returns:
        ANSI formatted text
    """
    words = re.findall(r"(\w+|\W+)", text)
    
    result = []
    for word in words:
        if re.search(r'\w', word):
            bold_part, regular_part = process_word(word, fixation_ratio)
            if bold_part:
                result.append(f"\033[1m{bold_part}\033[0m")
            if regular_part:
                result.append(regular_part)
        else:
            result.append(word)
    
    return "".join(result)


def format_text_rtf(text: str, fixation_ratio: float = 0.5) -> str:
    """
    Format text with RTF bold syntax.
    
    Args:
        text: The text to format
        fixation_ratio: The ratio of each word to bold
    
    Returns:
        RTF formatted text
    """
    words = re.findall(r"(\w+|\W+)", text)
    
    result = [r"{\rtf1\ansi\deff0"]
    result.append(r"{\fonttbl{\f0 Aileron-Regular;}{\f1 Aileron-Bold;}}")
    result.append(r"\f0\fs24")  # Default to regular font
    
    for word in words:
        if re.search(r'\w', word):
            bold_part, regular_part = process_word(word, fixation_ratio)
            if bold_part:
                result.append(r"{\b\f1 " + bold_part + r"}")
            if regular_part:
                result.append(r"\b0\f0 " + regular_part)
        else:
            result.append(word)
    
    result.append("}")
    return "".join(result)


def process_text(text: str, fixation_ratio: float = 0.5, output_format: str = "html") -> str:
    """
    Process text and format it according to the specified output format.
    
    Args:
        text: The text to process
        fixation_ratio: The ratio of each word to bold (0.4 to 0.5)
        output_format: One of 'html', 'markdown', 'ansi', 'rtf'
    
    Returns:
        Formatted text
    """
    formatters = {
        'html': format_text_html,
        'markdown': format_text_markdown,
        'ansi': format_text_ansi,
        'rtf': format_text_rtf,
    }
    
    if output_format not in formatters:
        raise ValueError(f"Unsupported format: {output_format}. Choose from: {list(formatters.keys())}")
    
    return formatters[output_format](text, fixation_ratio)


def demonstrate():
    """Demonstrate the tool with example text."""
    example_text = """
Reading is an essential skill for everyone. The ability to read well 
opens doors to knowledge and understanding. People with ADHD often 
find it challenging to maintain focus while reading long texts.
    """
    
    print("=" * 70)
    print("ADHD Reading Font Tool - Demonstration")
    print("=" * 70)
    print()
    
    # Show with different ratios
    for ratio in [0.4, 0.45, 0.5]:
        print(f"Fixation Ratio: {ratio} (bolding {int(ratio*100)}% of each word)")
        print("-" * 70)
        
        # HTML format
        html_output = process_text(example_text.strip(), ratio, 'html')
        print("HTML output:")
        print(html_output)
        print()
        
        # Markdown format
        md_output = process_text(example_text.strip(), ratio, 'markdown')
        print("Markdown output:")
        print(md_output)
        print()
        
        # Show specific word examples
        test_words = ["Reading", "the", "a", "ability", "I", "it", "understanding"]
        print("Word-by-word examples:")
        for word in test_words:
            bold_len = calculate_bold_length(word, ratio)
            bold_part, regular_part = process_word(word, ratio)
            print(f"  {word:15} -> <b>{bold_part}</b>{regular_part} (bold length: {bold_len})")
        print()
        print()


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='ADHD Reading Font Tool - Apply bold formatting to the first 40-50% of each word',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python adhd_font_tool.py --text "Reading is essential" --ratio 0.45
  python adhd_font_tool.py --file input.txt --output output.html
  python adhd_font_tool.py --demo
        """
    )
    
    parser.add_argument('--text', type=str, help='Text to process directly')
    parser.add_argument('--file', type=str, help='Input file to process')
    parser.add_argument('--output', type=str, help='Output file (if not specified, prints to stdout)')
    parser.add_argument('--ratio', type=float, default=0.5, 
                        help='Fixation ratio (0.4 to 0.5, default: 0.5)')
    parser.add_argument('--format', type=str, default='html', 
                        choices=['html', 'markdown', 'ansi', 'rtf'],
                        help='Output format (default: html)')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    
    args = parser.parse_args()
    
    # Validate ratio
    if args.ratio < 0.4 or args.ratio > 0.5:
        print("Error: Fixation ratio must be between 0.4 and 0.5")
        return 1
    
    # Run demo if requested
    if args.demo:
        demonstrate()
        return 0
    
    # Get text from either --text or --file
    text = None
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            return 1
    else:
        print("Error: Please specify --text or --file")
        parser.print_help()
        return 1
    
    # Process the text
    formatted_text = process_text(text, args.ratio, args.format)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        print(f"Output written to {args.output}")
    else:
        print(formatted_text)
    
    return 0


if __name__ == '__main__':
    exit(main())
