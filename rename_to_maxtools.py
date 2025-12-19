# -*- coding: utf-8 -*-
"""Script to rename MaxTools to MaxTools in all files"""
import os
import re

def replace_in_file(filepath):
    """Replace MaxTools references with MaxTools in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            print(f"Cannot read: {filepath}")
            return False

    original = content

    # Replacements
    content = content.replace('MaxTools', 'MaxTools')
    content = content.replace('Max Tools', 'Max Tools')
    content = content.replace('max_tools', 'max_tools')
    content = content.replace('Max Zermatten', 'Max Zermatten')
    content = content.replace('max@bussigny.ch', 'max@bussigny.ch')
    content = content.replace('Max Zermatten', 'Max Zermatten')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    extensions = ['.py', '.txt', '.md', '.ts', '.pro', '.qrc', '.xml']

    count = 0
    for root, dirs, files in os.walk(base_dir):
        # Skip __pycache__ and .git
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                if replace_in_file(filepath):
                    count += 1

    print(f"\nTotal files updated: {count}")

if __name__ == '__main__':
    main()
