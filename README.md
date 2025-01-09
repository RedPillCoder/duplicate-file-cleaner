# Duplicate File Cleaner for Windows Downloads

This repository contains a safe batch script for Windows that automatically checks your Downloads folder for duplicate files and removes the older versions, keeping only the most recent copies.

## Features

- Scans the current user's Downloads folder for duplicate files
- Compares files based on content, not just file names
- Deletes older duplicates, preserving the most recent version
- Works with all file types (e.g., .docx, .txt, .pdf, etc.)
- Safe operation with built-in checks and confirmations

## Usage

1. Download the `clean_duplicates.bat` file from this repository
2. Double-click the file to run it
3. Follow the on-screen prompts to confirm the operation
4. The script will automatically scan your Downloads folder and remove older duplicates

## Warning

Always ensure you have backups of important files before running any script that deletes files. While this script is designed to be safe, unforeseen circumstances can occur.

## How It Works

The script uses PowerShell commands within a batch file to:

1. Locate the current user's Downloads folder
2. Generate hash values for all files in the folder
3. Compare hash values to identify duplicates
4. For each set of duplicates, keep the newest file and delete the older ones

## Requirements

- Windows
- PowerShell 3.0 or later (pre-installed on Windows 8 and above)

## Customization

You can modify the script to target different folders or adjust its behavior. Open the `clean_duplicates.bat` file in a text editor to make changes.

## Contributing

Contributions to improve the script or add features are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
