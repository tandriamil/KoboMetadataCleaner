#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to clean the .kobo-images directory, use with caution.

It removes elements located into '.kobo-images' directory on two conditions:
- It is a file containing a pattern of useless file (see doc).
- It is an empty directory.

Documentation:
- https://pingouin-grincheux.net/WordPress/2016/05/31/kobo-trucs-et-astuces
"""

# Imports
import os
import sys
from itertools import product
from os import path

if len(sys.argv) != 2:
    print('Usage: clean_kobo_images.py [Kobo root directory]')

# Global variables
KOBO_DIR = sys.argv[1]
KOBO_IMAGES_DIR = path.join(KOBO_DIR, '.kobo-images')
PATTERN_RM_FILES = ['N3_SOCIAL_CURRENTREAD.parsed', 'N3_LIBRARY_SHELF.parsed',
                    'N3_FULL.parsed']  # See doc


count_rm_pattern, count_rm_empty = 0, 0

# Remove every file containing the pattern of unused files
for file, pattern in product(os.listdir(KOBO_IMAGES_DIR), PATTERN_RM_FILES):
    if pattern in file:
        os.remove(file)
        count_rm_pattern += 1


# Remove every empty directory (a lot of them)
for directory, folders, files in os.walk(KOBO_IMAGES_DIR):
    if not folders and not files:
        os.rmdir(directory)
        count_rm_empty += 1

print('%d files removed by the pattern' % count_rm_pattern)
print('%d empty directories removed' % count_rm_empty)
