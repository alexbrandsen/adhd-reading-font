#!/usr/bin/env python3
"""
Unit tests for the ADHD Reading Font Tool
"""

import unittest
from adhd_font_tool import (
    calculate_bold_length,
    process_word,
    process_text,
    format_text_html,
    format_text_markdown,
)


class TestCalculateBoldLength(unittest.TestCase):
    """Test the calculate_bold_length function"""
    
    def test_empty_string(self):
        self.assertEqual(calculate_bold_length("", 0.5), 0)
    
    def test_single_letter(self):
        """1-letter words should return 0 (unbolded)"""
        self.assertEqual(calculate_bold_length("a", 0.5), 0)
        self.assertEqual(calculate_bold_length("I", 0.5), 0)
    
    def test_two_letter_words(self):
        """2-letter words should bold 1 letter"""
        self.assertEqual(calculate_bold_length("it", 0.5), 1)
        self.assertEqual(calculate_bold_length("is", 0.5), 1)
        self.assertEqual(calculate_bold_length("at", 0.5), 1)
    
    def test_three_letter_words(self):
        """3-letter words should bold 1 letter"""
        self.assertEqual(calculate_bold_length("the", 0.5), 1)
        self.assertEqual(calculate_bold_length("and", 0.5), 1)
        self.assertEqual(calculate_bold_length("for", 0.5), 1)
    
    def test_four_letter_words_at_50_percent(self):
        """4-letter words at 50% should bold 2 letters"""
        self.assertEqual(calculate_bold_length("Bold", 0.5), 2)
        self.assertEqual(calculate_bold_length("text", 0.5), 2)
        self.assertEqual(calculate_bold_length("word", 0.5), 2)
    
    def test_seven_letter_words_at_50_percent(self):
        """7-letter words at 50% should bold 4 letters (ceil(3.5) = 4)"""
        self.assertEqual(calculate_bold_length("Reading", 0.5), 4)
        self.assertEqual(calculate_bold_length("example", 0.5), 4)
    
    def test_at_40_percent(self):
        """Test with 40% fixation ratio"""
        # 7 letters: ceil(7 * 0.4) = ceil(2.8) = 3
        self.assertEqual(calculate_bold_length("Reading", 0.4), 3)
        # 9 letters: ceil(9 * 0.4) = ceil(3.6) = 4
        self.assertEqual(calculate_bold_length("essential", 0.4), 4)
        # 4 letters: ceil(4 * 0.4) = ceil(1.6) = 2
        self.assertEqual(calculate_bold_length("text", 0.4), 2)
    
    def test_at_45_percent(self):
        """Test with 45% fixation ratio"""
        # 7 letters: ceil(7 * 0.45) = ceil(3.15) = 4
        self.assertEqual(calculate_bold_length("Reading", 0.45), 4)
        # 9 letters: ceil(9 * 0.45) = ceil(4.05) = 5
        self.assertEqual(calculate_bold_length("essential", 0.45), 5)
        # 4 letters: ceil(4 * 0.45) = ceil(1.8) = 2
        self.assertEqual(calculate_bold_length("text", 0.45), 2)


class TestProcessWord(unittest.TestCase):
    """Test the process_word function"""
    
    def test_single_letter(self):
        bold, regular = process_word("a", 0.5)
        self.assertEqual(bold, "")
        self.assertEqual(regular, "a")
    
    def test_two_letter(self):
        bold, regular = process_word("it", 0.5)
        self.assertEqual(bold, "i")
        self.assertEqual(regular, "t")
    
    def test_three_letter(self):
        bold, regular = process_word("the", 0.5)
        self.assertEqual(bold, "t")
        self.assertEqual(regular, "he")
    
    def test_four_letter(self):
        bold, regular = process_word("Bold", 0.5)
        self.assertEqual(bold, "Bo")
        self.assertEqual(regular, "ld")
    
    def test_seven_letter(self):
        bold, regular = process_word("Reading", 0.5)
        self.assertEqual(bold, "Read")
        self.assertEqual(regular, "ing")


class TestFormatTextHTML(unittest.TestCase):
    """Test HTML formatting"""
    
    def test_simple_sentence(self):
        result = format_text_html("Reading is essential", 0.5)
        self.assertEqual(result, "<b>Read</b>ing <b>i</b>s <b>essen</b>tial")
    
    def test_with_punctuation(self):
        result = format_text_html("Hello, world!", 0.5)
        self.assertEqual(result, "<b>Hel</b>lo, <b>wor</b>ld!")
    
    def test_multiple_spaces(self):
        result = format_text_html("Hello   world", 0.5)
        self.assertEqual(result, "<b>Hel</b>lo   <b>wor</b>ld")


class TestFormatTextMarkdown(unittest.TestCase):
    """Test Markdown formatting"""
    
    def test_simple_sentence(self):
        result = format_text_markdown("Reading is essential", 0.5)
        self.assertEqual(result, "**Read**ing **i**s **essen**tial")
    
    def test_with_punctuation(self):
        result = format_text_markdown("Hello, world!", 0.5)
        self.assertEqual(result, "**Hel**lo, **wor**ld!")


class TestProcessText(unittest.TestCase):
    """Test the main process_text function"""
    
    def test_html_format(self):
        result = process_text("test", 0.5, "html")
        self.assertEqual(result, "<b>te</b>st")
    
    def test_markdown_format(self):
        result = process_text("test", 0.5, "markdown")
        self.assertEqual(result, "**te**st")
    
    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            process_text("test", 0.5, "invalid")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_empty_text(self):
        result = process_text("", 0.5, "html")
        self.assertEqual(result, "")
    
    def test_only_whitespace(self):
        result = process_text("   ", 0.5, "html")
        self.assertEqual(result, "   ")
    
    def test_only_punctuation(self):
        result = process_text("!!!", 0.5, "html")
        self.assertEqual(result, "!!!")
    
    def test_mixed_case(self):
        result = format_text_html("Reading TEXT", 0.5)
        self.assertEqual(result, "<b>Read</b>ing <b>TE</b>XT")
    
    def test_numbers(self):
        result = format_text_html("test 123 4567", 0.5)
        self.assertEqual(result, "<b>te</b>st <b>1</b>23 <b>45</b>67")


if __name__ == '__main__':
    unittest.main()
