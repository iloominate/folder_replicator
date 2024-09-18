# Folder Replicator

## Overview
FolderReplicator is a Python script designed to synchronize files and folders between a source directory and a replica directory.
The script continuously monitors the source folder and ensures that the replica folder is kept in sync by copying new files, updating modified files, and deleting files that no longer exist in the source.

## Features
- **File Synchronization:** Automatically copies files from the source to the replica directory.
- **Folder Synchronization:** Creates or deletes folders in the replica directory to match the source.
- **File Integrity Check:** Compares files in the source and replica directories by their MD5 hash and updates if changes are detected.
- **Logging:** Logs all synchronization actions (copy, modify, delete) to a specified log file.

## Prerequisites
- Python 3.10 or higher.
- No external dependencies except for standard Python libraries.

## Usage
1. Clone or download the repository.
2. Run the script using Python, providing the required arguments.

## Command-line Arguments
| Argument | Short form   | Description  |
|---|---|---|
| --Source  | -s | Path to the source folder to replicate.  |
|  --Replica | -r  | Path to the replica folder to synchronize to.  |
|  --Interval | -i  | Synchronization interval in seconds.  |
|  --Log |   | -l  | Path to the log file where sync actions are recorded.  |   |

## Example Command
```bash
python main.py -s "/path/to/source" -r "/path/to/replica" -i 60 -l "/path/to/logfile.log"
```
## Known Limitations
**File and Folder Renaming:** The script's current version does not track the renaming of files or folders.
If a file or folder is renamed in the source directory, it will be treated as a new file or folder, and the old file or folder in the replica directory will be deleted.
This may lead to redundant copying of large files that were simply renamed.

Future improvements could address this by implementing a mechanism that would work with inodes (or equivalent file system metadata) to detect renames instead of treating them as separate delete-and-add operations.
## License
This project is open-source and available under the MIT License.

## Author
Written by Aliaksei Klimau.
