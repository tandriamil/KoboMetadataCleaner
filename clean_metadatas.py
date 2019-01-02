#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to clean the 'Digital Editions' directory, use with caution.

It will check, for Annotations and Manifest directories, if the file concerned
by a given metadata file is present or not. If not present, the metadata file
is removed.

Note:
- We use sortedcontainers for better performances.
"""

# Imports
import os
import sys
from os import path
from sortedcontainers import SortedSet

if len(sys.argv) != 2:
    print('Usage: clean_metadatas.py [Kobo root directory]')

# Global variables
KOBO_DIR = sys.argv[1]
ANNOT_DIR = path.join(KOBO_DIR, 'Digital Editions', 'Annotations')
MANIFEST_DIR = path.join(KOBO_DIR, 'Digital Editions', 'Manifest')


def base_dir_length(base_dir_path):
    """Return the length of a base directory path, including the last '/'."""
    if not base_dir_path.endswith('/'):
        return len(base_dir_path) + 1
    return len(base_dir_path)


def remove_xml_extension(metadata_file):
    """Return the name of a metadata file without the .xml extension."""
    return path.splitext(metadata_file)[0]


len_kobo_dir = base_dir_length(KOBO_DIR)
len_annot_dir = base_dir_length(ANNOT_DIR)
len_manif_dir = base_dir_length(MANIFEST_DIR)

# Counters and storages
documents = SortedSet()
count_temp_removed = 0
count_annot_removed, count_annot_emptied = 0, 0
count_manif_removed, count_manif_emptied = 0, 0

# Get the documents located into the root directory
for directory, _, files in os.walk(KOBO_DIR):
    if directory in (ANNOT_DIR, MANIFEST_DIR):
        continue  # Pass metadata directories

    if '.kobo' in directory or '.adobe' in directory:
        continue  # Pass metadata directories

    for filename in files:
        document_path = path.join(directory, filename)

        # Remove temporary files by the way
        if filename.startswith('.'):
            os.remove(document_path)
            count_temp_removed += 1
            continue

        document_file = document_path[len_kobo_dir:]
        documents.add(document_file)

print('Parsed document files, removed %d temporary files by the way.'
      % count_temp_removed)


# --- Annotations

# For every file into Annotations metadata directory
for directory, _, files in os.walk(ANNOT_DIR):
    for filename in files:
        metadata_file = path.join(directory, filename)
        metadata_name = remove_xml_extension(metadata_file[len_annot_dir:])
        if metadata_name not in documents:
            os.remove(metadata_file)
            count_annot_removed += 1

# Remove every empty directory (a lot of them)
for directory, folders, files in os.walk(ANNOT_DIR):
    if not folders and not files:
        os.rmdir(directory)
        count_annot_emptied += 1

print('Removed %d annotations metadata files, and %d empty directories'
      % (count_annot_removed, count_annot_emptied))


# --- Manifest

# For every file into Manifest metadata directory
for directory, _, files in os.walk(MANIFEST_DIR):
    for filename in files:
        metadata_file = path.join(directory, filename)
        metadata_name = remove_xml_extension(metadata_file[len_manif_dir:])
        if metadata_name not in documents:
            os.remove(metadata_file)
            count_manif_removed += 1

# Remove every empty directory (a lot of them)
for directory, folders, files in os.walk(MANIFEST_DIR):
    if not folders and not files:
        os.rmdir(directory)
        count_manif_emptied += 1

print('Removed %d manifest metadata files, and %d empty directories'
      % (count_manif_removed, count_manif_emptied))
