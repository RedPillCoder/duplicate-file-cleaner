# Duplicate File Cleaner

This tool helps you identify and remove duplicate files in your Downloads folder, keeping only the most recently modified version of each file.

## Table of Contents
1. [Features](#features)
2. [How it Works](#how-it-works)
3. [Usage](#usage)
   - [Option 1: Run the Python Script](#option-1-run-the-python-script)
   - [Option 2: Use the Executable](#option-2-use-the-executable)
4. [Functions](#functions)
5. [Important Notes](#important-notes)
6. [Requirements](#requirements)
7. [Contributing](#contributing)

## Features
- Scans the user's Downloads folder for duplicate files
- Uses MD5 hash to identify identical files
- Keeps the most recently modified version of each duplicate file
- Provides an option to delete older duplicates

## How it Works
1. The script walks through the Downloads folder and its subfolders.
2. It generates an MD5 hash for each file encountered.
3. Files with identical MD5 hashes are grouped together.
4. For each group of duplicates, the most recently modified file is kept, while others are marked for potential deletion.
5. The user is presented with a list of duplicate files and asked for confirmation before deletion.

## Usage

### Option 1: Run the Python Script
1. Ensure you have Python installed on your system.
2. Clone this repository or download the script.
3. Run the script using Python:
   ```
   python delete_duplicates.py
   ```

### Option 2: Use the Executable
1. Download the `delete_duplicates.exe` file from the releases section.
2. Double-click the executable to run it.

For both options:
4. The tool will scan your Downloads folder and display any duplicates found.
5. If duplicates are found, you'll be prompted to confirm deletion of the older copies.

## Functions
- `generate_md5(file_path)`: Generates an MD5 hash for a given file.
- `find_duplicates(folder_path)`: Identifies duplicate files in the specified folder.
- `delete_files(files)`: Deletes the specified list of files.
- `main()`: Orchestrates the scanning and deletion process.

## Important Notes
- This tool will only delete files after user confirmation.
- The tool keeps the most recently modified version of each duplicate file.
- Use this tool with caution, as deleted files cannot be recovered.

## Requirements
For running the Python script:
- Python 3.x
- Standard Python libraries: os, hashlib, time

For running the executable:
- No additional requirements. Just download and run.

## Contributing
Feel free to fork this repository and submit pull requests for any improvements or bug fixes.
