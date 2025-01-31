import os
import hashlib
import logging
from logging.handlers import RotatingFileHandler
from typing import List, Tuple, Optional
from send2trash import send2trash
import time

# Set up logging with a rotating file handler
log_file = 'deleted_files.log'
handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)  # 5 MB per log file, keep 5 backups
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p'  # 12-hour format with AM/PM
)

def generate_sha1(file_path: str) -> str:
    """Generate SHA-1 hash for a file."""
    hash_sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def find_duplicates(folder_path: str, file_types: Optional[List[str]] = None) -> List[Tuple[str, float]]:
    """Find duplicate files in the specified folder, optionally filtering by file type."""
    files_by_hash = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file_types and not any(file.lower().endswith(ext) for ext in file_types):
                continue  # Skip files that do not match the specified types
            
            file_path = os.path.join(root, file)
            file_hash = generate_sha1(file_path)
            last_modified = os.path.getmtime(file_path)
            files_by_hash.setdefault(file_hash, []).append((file_path, last_modified))

    # Identify duplicates
    duplicates = [item for sublist in files_by_hash.values() if len(sublist) > 1 for item in sublist[1:]]
    return duplicates

def log_and_print(message: str) -> None:
    """Log a message and print it to the console."""
    logging.info(message)
    print(message)

def delete_files(files: List[Tuple[str, float]], move_to_trash: bool = False, backup_folder: Optional[str] = None) -> None:
    """Delete the specified files, move them to the trash, or move them to a backup folder."""
    if not files:
        log_and_print("No files to delete.")
        return

    for file_path, _ in files:
        try:
            if move_to_trash:
                send2trash(file_path)
                log_and_print(f"Moved to trash: {file_path}")
            elif backup_folder:
                os.makedirs(backup_folder, exist_ok=True)
                backup_path = os.path.join(backup_folder, os.path.basename(file_path))
                os.rename(file_path, backup_path)
                log_and_print(f"Moved to backup: {file_path} -> {backup_path}")
            else:
                os.remove(file_path)
                log_and_print(f"Deleted: {file_path}")
        except FileNotFoundError:
            log_and_print(f"File not found: {file_path}")
        except PermissionError:
            log_and_print(f"Permission denied: {file_path}")
        except Exception as e:
            log_and_print(f"Error processing {file_path}: {e}")

def get_user_confirmation(prompt: str) -> bool:
    """Get a yes/no confirmation from the user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            log_and_print("Invalid response. Please answer with 'yes' or 'no'.")

def get_file_types() -> Optional[List[str]]:
    """Get file types to filter from user input."""
    file_types_input = input("Enter file types to scan for duplicates (comma-separated, e.g., .jpg,.png,.pdf) or leave blank for all: ")
    if file_types_input:
        # Split by comma and strip whitespace, ensuring valid extensions
        file_types = [ft.strip().lower() for ft in file_types_input.split(',')]
        # Validate file types to ensure they start with a dot
        valid_file_types = [ft for ft in file_types if ft.startswith('.')]
        if not valid_file_types:
            log_and_print("No valid file types entered. Defaulting to all file types.")
            return None
        return valid_file_types
    return None

def main() -> None:
    """Main function to execute the duplicate file finder and handler."""
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    log_and_print(f"Scanning for duplicates in: {downloads_folder}")
    log_and_print("Scanning...")

    start_time = time.time()  # Start timing the operation
    file_types = get_file_types()
    duplicates = find_duplicates(downloads_folder, file_types)
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    log_and_print(f"Scanning completed in {elapsed_time:.2f} seconds.")

    if not duplicates:
        log_and_print("No duplicate files found.")
        return

    log_and_print(f"Found {len(duplicates)} duplicate files:")
    for file_path, _ in duplicates:
        log_and_print(f" - {file_path}")

    action = input("Do you want to (d)elete, (b)ackup, or (m)ove to trash? (d/b/m): ").strip().lower()
    
    if action == 'd':
        if get_user_confirmation("Are you sure you want to delete these older duplicates? (yes/no): "):
            delete_files(duplicates)
            log_and_print("Deletion complete.")
        else:
            log_and_print("Deletion canceled.")
    elif action == 'm':
        if get_user_confirmation("Are you sure you want to move these older duplicates to trash? (yes/no): "):
            delete_files(duplicates, move_to_trash=True)
            log_and_print("Moved to trash complete.")
        else:
            log_and_print("Move to trash canceled.")
    elif action == 'b':
        backup_folder = os.path.join(downloads_folder, "Duplicates_Backup")
        if get_user_confirmation("Are you sure you want to move these older duplicates to the backup folder? (yes/no): "):
            delete_files(duplicates, backup_folder=backup_folder)
            log_and_print("Backup complete.")
        else:
            log_and_print("Backup canceled.")
    else:
        log_and_print("Invalid option selected.")

if __name__ == "__main__":
    main()

