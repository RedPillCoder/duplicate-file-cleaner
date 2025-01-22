# Duplicate File Cleaner

This tool helps you identify and remove duplicate files in your Downloads folder, keeping only the most recently modified version of each file.

## Table of Contents

- [Features](#features)
- [How it Works](#how-it-works)
- [Usage](#usage)
  - [Option 1: Run the Python Script](#option-1-run-the-python-script)
  - [Option 2: Use the Executable](#option-2-use-the-executable)
- [Functions](#functions)
- [Important Notes](#important-notes)
- [Requirements](#requirements)
- [Contributing](#contributing)

## Features

- Scans the user's Downloads folder for duplicate files.
- Uses SHA-1 hash to identify identical files.
- Keeps the most recently modified version of each duplicate file.
- Provides options to delete older duplicates, move them to the trash, or back them up to a specified folder.
- Logs actions taken for auditing and debugging purposes.

## How it Works

1. The script walks through the Downloads folder and its subfolders.
2. It generates an SHA-1 hash for each file encountered.
3. Files with identical SHA-1 hashes are grouped together.
4. For each group of duplicates, the most recently modified file is kept, while others are marked for potential deletion.
5. The user is presented with a list of duplicate files and asked for confirmation before deletion, moving to trash, or backing up.

## Usage

### Option 1: Run the Python Script

1. Ensure you have Python installed on your system.
2. Clone this repository or download the script.
3. Run the script using Python:

   ```bash
   python delete_duplicates.py
   ```

### Option 2: Use the Executable

1. Download the `delete_duplicates.exe` file from the releases section.
2. Double-click the executable to run it.

For both options:

- The tool will scan your Downloads folder and display any duplicates found.
- If duplicates are found, you'll be prompted to confirm the action (delete, move to trash, or back up) for the older copies.

## Functions

- `generate_sha1(file_path)`: Generates an SHA-1 hash for a given file.
- `find_duplicates(folder_path)`: Identifies duplicate files in the specified folder.
- `delete_files(files, move_to_trash=False, backup_folder=None)`: Deletes or moves the specified list of files based on user input.
- `main()`: Orchestrates the scanning and deletion process.

## Important Notes

- This tool will only delete files after user confirmation.
- The tool keeps the most recently modified version of each duplicate file.
- Use this tool with caution, as deleted files cannot be recovered.
- The tool logs all actions taken, which can be found in `deleted_files.log`.

## Requirements

For running the Python script:

- Python 3.x
- Standard Python libraries: `os`, `hashlib`, `logging`, `send2trash`

For running the executable:

- No additional requirements. Just download and run.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or bug fixes.
