import os
import hashlib
import logging
from typing import List, Tuple
from send2trash import send2trash  # Import send2trash

# Set up logging
logging.basicConfig(filename='deleted_files.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_sha1(file_path: str) -> str:
    """Generate SHA-1 hash for a file."""
    hash_sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def find_duplicates(folder_path: str) -> List[Tuple[str, float]]:
    """Find duplicate files in the specified folder."""
    files_by_hash = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = generate_sha1(file_path)
            last_modified = os.path.getmtime(file_path)
            files_by_hash.setdefault(file_hash, []).append((file_path, last_modified))

    # Identify duplicates
    duplicates = [
        file_list[1:]  # Exclude the first (latest) file
        for file_list in files_by_hash.values() if len(file_list) > 1
    ]
    return [item for sublist in duplicates for item in sublist]  # Flatten the list

def delete_files(files: List[Tuple[str, float]], move_to_trash: bool = False, backup_folder: str = None) -> None:
    """Delete the specified files, move them to the trash, or move them to a backup folder."""
    for file_path, _ in files:
        try:
            if move_to_trash:
                send2trash(file_path)  # Move to system trash
                logging.info(f"Moved to trash: {file_path}")
                print(f"Moved to trash: {file_path}")
            elif backup_folder:
                # Move to backup folder
                os.makedirs(backup_folder, exist_ok=True)  # Create backup folder if it doesn't exist
                backup_path = os.path.join(backup_folder, os.path.basename(file_path))
                os.rename(file_path, backup_path)  # Move the file to the backup folder
                logging.info(f"Moved to backup: {file_path} -> {backup_path}")
                print(f"Moved to backup: {file_path} -> {backup_path}")
            else:
                os.remove(file_path)
                logging.info(f"Deleted: {file_path}")
                print(f"Deleted: {file_path}")
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            print(f"File not found: {file_path}")
        except PermissionError:
            logging.error(f"Permission denied: {file_path}")
            print(f"Permission denied: {file_path}")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            print(f"Error processing {file_path}: {e}")

def main() -> None:
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"Scanning for duplicates in: {downloads_folder}")
    print("Scanning...")

    duplicates = find_duplicates(downloads_folder)

    if not duplicates:
        print("No duplicate files found.")
        logging.info("No duplicate files found.")
        return

    print(f"Found {len(duplicates)} duplicate files:")
    for file_path, _ in duplicates:
        print(f" - {file_path}")

    action = input("Do you want to (d)elete, (b)ackup, or (m)ove to trash? (d/b/m): ").strip().lower()
    if action == 'd':
        if input("Are you sure you want to delete these older duplicates? (yes/no): ").strip().lower() == 'yes':
            delete_files(duplicates)
            print("Deletion complete.")
        else:
            print("Deletion canceled.")
    elif action == 'm':
        if input("Are you sure you want to move these older duplicates to trash? (yes/no): ").strip().lower() == 'yes':
            delete_files(duplicates, move_to_trash=True)
            print("Moved to trash complete.")
        else:
            print("Move to trash canceled.")
    elif action == 'b':
        backup_folder = os.path.join(downloads_folder, "Duplicates_Backup")  # Define backup folder
        if input("Are you sure you want to move these older duplicates to the backup folder? (yes/no): ").strip().lower() == 'yes':
            delete_files(duplicates, backup_folder=backup_folder)
            print("Backup complete.")
        else:
            print("Backup canceled.")
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
