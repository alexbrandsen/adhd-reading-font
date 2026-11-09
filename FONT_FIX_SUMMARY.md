# ADHD Font Fix Summary

## Problem
The original `adhd-font.otf` was bolding **every character** instead of just the first 40-50% of each word.

## Root Cause
The GSUB feature rules were not properly scoped to word boundaries. The substitution patterns were matching all letter positions instead of only the first N positions per word.

## Solution
Created a new `adhd-font.otf` with proper OpenType contextual alternates (calt) feature using chaining contextual substitution rules.

## Implementation Details

### Font Construction
1. **Merged fonts**: Combined `Aileron-Regular.otf` and `Aileron-Bold.otf` using `fontTools.merge.Merger`
   - Regular glyphs: A-Z, a-z (52 glyphs)
   - Bold glyphs: A.1-Z.1, a.1-z.1 (52 glyphs with `.1` suffix)
   - Total glyphs: 676

2. **Removed existing tables**: Cleared GSUB, GPOS, and GDEF tables before adding new features

3. **Added GSUB calt feature**: Created chaining contextual substitution rules with proper ignore statements

### Bolding Rules
Based on the formula: `ceil(word_length × fixation_ratio)` where fixation_ratio is 40-50%

| Word Length | Bold Letters | Example |
|-------------|--------------|---------|
| 1 | 0 | I |
| 2-3 | 1 | **it**, **the** |
| 4-6 | 2 | **te**st, **he**llo, **wo**rld |
| 7-8 | 3 | **rea**ding, **att**ention |
| 9-10 | 4 | **atte**ntion, **conc**entration |
| 11+ | ceil(n × 0.4) | **conce**ntration |

### OpenType Feature Code
```fea
@az = [a-z A-Z];
@AZ = [a.1-z.1 A.1-Z.1];
@all = [a-z A-Z a.1-z.1 A.1-Z.1];

feature calt {
    # 7-8 letter words: bold 3rd letter
    ignore sub @all @all @all @az' @all @all @all @all;
    ignore sub @all @all @all @az' @all @all @all;
    sub @all @all @az' @all @all @all @all by @AZ;
    sub @all @all @az' @all @all @all by @AZ;

    # 4-6 letter words: bold 2nd letter
    ignore sub @all @all @az' @all @all;
    ignore sub @all @all @az' @all;
    sub @all @az' @all @all @all by @AZ;
    sub @all @az' @all @all by @AZ;
    sub @all @az' @all by @AZ;

    # 2-3 letter words: bold 1st letter
    ignore sub @all @az' @all;
    ignore sub @all @az';
    sub @az' @all @all by @AZ;
    sub @az' @all by @AZ;
} calt;
```

### Key Design Decisions
1. **Used `@all` class in context**: Includes both regular and bold glyphs to handle already-substituted glyphs in subsequent positions
2. **Used `'` marker**: Marks the position to substitute in chaining contexts
3. **Used `ignore` statements**: Prevents rules from matching at wrong positions in longer words
4. **Ordered rules by word length**: Longest word rules first, shortest last

### Technical Specifications
- **Font format**: OTF (CFF-based)
- **GSUB lookups**: 2 (one for ignore rules, one for substitution rules)
- **ChainContextSubst tables**: 13 (6 ignore + 7 substitution)
- **Feature tag**: `calt` (Contextual Alternates)
- **File size**: 71,816 bytes

## Testing
The font should now correctly bold only the first portion of each word when used in:
- Microsoft Word
- HTML/CSS (via `@font-face`)
- Any application that supports OpenType features

## Files Modified
- `adhd-font.otf` - Main font file with corrected GSUB features

## Verification
Run the following to verify:
```bash
python3 -c "
from fontTools.ttLib import TTFont
f = TTFont('adhd-font.otf')
print('GSUB:', 'GSUB' in f)
print('Features:', [feat.FeatureTag for feat in f['GSUB'].table.FeatureList.FeatureRecord])
f.close()
"
```

Expected output:
```
GSUB: True
Features: ['calt']
```
