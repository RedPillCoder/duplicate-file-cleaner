import os
import hashlib
import time

def generate_sha1(file_path):
    """Generate SHA-1 hash for a file."""
    hash_sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def find_duplicates(folder_path):
    """Find duplicate files in the specified folder."""
    files_by_hash = {}
    duplicates = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = generate_sha1(file_path)  # Change to SHA-1
            last_modified = os.path.getmtime(file_path)

            if file_hash in files_by_hash:
                files_by_hash[file_hash].append((file_path, last_modified))
            else:
                files_by_hash[file_hash] = [(file_path, last_modified)]

    # Identify duplicates
    for file_hash, file_list in files_by_hash.items():
        if len(file_list) > 1:
            # Sort by last modified time (latest first)
            file_list.sort(key=lambda x: x[1], reverse=True)
            # Keep the latest file and mark the rest for deletion
            duplicates.extend(file_list[1:])  # Exclude the first (latest) file

    return duplicates

def delete_files(files):
    """Delete the specified files."""
    for file_path, _ in files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def main():
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"Scanning for duplicates in: {downloads_folder}")

    duplicates = find_duplicates(downloads_folder)

    if not duplicates:
        print("No duplicate files found.")
        return

    print(f"Found {len(duplicates)} duplicate files:")
    for file_path, _ in duplicates:
        print(f" - {file_path}")

    confirmation = input("Do you want to delete these older duplicates? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        delete_files(duplicates)
        print("Deletion complete.")
    else:
        print("Deletion canceled.")

if __name__ == "__main__":
    main()
