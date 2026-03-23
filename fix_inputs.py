#!/usr/bin/env python3
"""
Fix incorrectly placed HTML input elements that should be ___ instead.
These inputs were injected inside JavaScript strings and speaking scaffolds.
"""

import os
import re
import sys

INPUT_PATTERN = r'<input type="text" style="width: 120px; padding: 4px 8px; font-size: 1em; border: 2px solid #667eea; border-radius: 6px; color: #764ba2; font-weight: 600; text-align: center;" placeholder="[^"]*">'
UNDERSCORE = "___"

# Game files where ALL content is in JS data and should be reverted entirely
GAME_FILE_PREFIXES = [
    'gr_', 'bl_', 'ielts-spelling-gym', 'vocab-', 'collocation-'
]

def is_game_file(filename):
    """Check if file is a game file that should have blanket replacement."""
    return any(filename.startswith(prefix) for prefix in GAME_FILE_PREFIXES)

def extract_script_ranges(content):
    """Extract all <script> tag ranges as (start, end) tuples."""
    ranges = []
    for match in re.finditer(r'<script[^>]*>(.*?)</script>', content, re.DOTALL):
        ranges.append((match.start(1), match.end(1)))
    return ranges

def extract_scaffold_ranges(content):
    """Extract all speaking scaffold element ranges."""
    ranges = []

    # Looking for divs/p with scaffold-related classes
    scaffold_patterns = [
        (r'<div[^>]*class="[^"]*(?:chip|scaffold|prompt|template|speaking|sentence-starter|instruction)[^"]*"[^>]*>', r'</div>'),
        (r'<p[^>]*class="[^"]*(?:scaffold|prompt|sentence-starter|speaking)[^"]*"[^>]*>', r'</p>'),
    ]

    for open_pattern, close_pattern in scaffold_patterns:
        open_positions = []
        for match in re.finditer(open_pattern, content):
            open_positions.append(match.end())

        close_positions = []
        for match in re.finditer(close_pattern, content):
            close_positions.append(match.start())

        # Match opens with closes (simple nesting assumption)
        for open_pos in open_positions:
            for close_pos in close_positions:
                if close_pos > open_pos:
                    ranges.append((open_pos, close_pos))
                    break

    return ranges

def is_position_in_ranges(pos, ranges):
    """Check if a position falls within any of the given ranges."""
    for start, end in ranges:
        if start <= pos < end:
            return True
    return False

def fix_content(content, filename):
    """Fix input elements in content. Return modified content."""

    # For game files: simple blanket replacement
    if is_game_file(filename):
        return re.sub(INPUT_PATTERN, UNDERSCORE, content)

    # For regular files: context-aware replacement
    script_ranges = extract_script_ranges(content)
    scaffold_ranges = extract_scaffold_ranges(content)

    # Find all input elements and track which ones to replace
    replacements = []  # List of (start, end) tuples to replace
    for match in re.finditer(INPUT_PATTERN, content):
        match_start = match.start()

        # Replace if inside script tag
        if is_position_in_ranges(match_start, script_ranges):
            replacements.append((match.start(), match.end()))
            continue

        # Replace if inside scaffold
        if is_position_in_ranges(match_start, scaffold_ranges):
            replacements.append((match.start(), match.end()))
            continue

    # Apply replacements in reverse order to maintain positions
    for start, end in sorted(replacements, reverse=True):
        content = content[:start] + UNDERSCORE + content[end:]

    return content

def fix_file(filepath):
    """Fix a single HTML file. Return count of fixes made."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

    filename = os.path.basename(filepath)
    modified_content = fix_content(original_content, filename)

    if modified_content != original_content:
        fixes = len(re.findall(INPUT_PATTERN, original_content)) - len(
            re.findall(INPUT_PATTERN, modified_content)
        )
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"Fixed {fixes} inputs in {filename}")
            return fixes
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return 0

    return 0

def main():
    sitedir = '/sessions/great-gracious-mendel/mnt/malcolmtheteacher/Documents/01_Work/gitsite'

    if not os.path.isdir(sitedir):
        print(f"Directory not found: {sitedir}")
        sys.exit(1)

    total_fixes = 0
    html_files = []

    # Collect all HTML files (excluding ww_quiz_* as instructed)
    for filename in os.listdir(sitedir):
        if filename.endswith('.html') and not filename.startswith('ww_quiz_'):
            html_files.append(os.path.join(sitedir, filename))

    print(f"Found {len(html_files)} HTML files to check")

    # Process all files
    for filepath in sorted(html_files):
        fixes = fix_file(filepath)
        total_fixes += fixes

    print(f"\nTotal fixes made: {total_fixes}")

if __name__ == '__main__':
    main()
