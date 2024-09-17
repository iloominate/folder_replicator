import argparse
import os
import os.path
import time
import hashlib
import shutil
from typing import final


CHUNK_SIZE: final = 1024 * 8  # 8 KiB


class FolderReplicator:
    def __init__(self, source_dir, replica_dir, interval, log_path):
        self.source_dir = source_dir
        self.replica_dir = replica_dir
        self.interval = int(interval)
        self.log_f = open(log_path, "w")

    def log_message(self, content):
        print(content)
        self.log_f.write(content + "\n")

    def copy_file(self, s_file_path):

        relative_path = os.path.relpath(s_file_path, self.source_dir)
        replica_file_path = os.path.join(str(replica_dir), str(relative_path))

        shutil.copy(s_file_path, replica_file_path)
        self.log_message(f"File added: {replica_file_path}")

    def copy_folder_recursive(self, s_dir):
        # Create empty folder
        os.mkdir(replica_dir + s_dir.name)
        self.log_message(f"Folder created: {replica_dir + s_dir.name}")

        # Copy source folder content to new replica folder
        with os.scandir(s_dir) as s_entries:
            for s_entry in s_entries:
                if s_entry.is_dir():  # Recursive folder copy
                    self.copy_folder_recursive(s_dir)
                else:  # File copy
                    self.copy_file(s_entry.path)

    def delete_file(self, r_file_path):
        try:
            os.remove(r_file_path)
            self.log_message(f"File deleted: {r_file_path}")
        except OSError:
            raise Exception(f"Couldn't delete file: {r_file_path}")

    def delete_folder_recursive(self, r_dir):
        with os.scandir(r_dir) as r_entries:
            for r_entry in r_entries:
                if r_entry.is_dir():  # Recursive folder deletion
                    self.delete_folder_recursive(r_dir)
                else:   # File deletion
                    self.delete_file(r_entry.path)

        os.rmdir(r_dir)
        self.log_message(f"Folder deleted: {r_dir}")

    def compare_file_content(self, s_file_path, r_file_path):
        source_f_hash = get_file_hashsum(s_file_path)
        replica_f_hash = get_file_hashsum(r_file_path)
        if replica_f_hash != source_f_hash:
            shutil.copy(s_file_path, r_file_path)
            self.log_message(f"File modified: {r_file_path}")

    def compare_folder_with_entries(self, s_dir, r_entries, source_items):
        folder_found = False
        for r_entry in r_entries:  # Look for the folder name in replica
            if r_entry.name == s_dir.name:
                source_items.append(s_dir.name)
                if r_entry.is_dir():  # Folder with the same name was found
                    folder_found = True
                    self.compare_folder_content_recursive(s_dir.path, r_entry.path)
                else:  # File with the same name was found
                    self.delete_file(r_entry.path)
                break
        if not folder_found:  # Folder with the same name was not found in replica folder
            self.copy_folder_recursive(s_dir)
            source_items.append(s_dir.name)

    def compare_file_with_entries(self, s_file, r_entries, s_entries_checked):
        file_found = False
        for r_entry in r_entries:
            if r_entry.name == s_file.name:
                file_found = True
                s_entries_checked.append(s_file.name)
                if r_entry.is_file():
                    self.compare_file_content(s_file.path, r_entry.path)
                else:
                    self.delete_folder_recursive(r_entry.path)
                break
        if not file_found:  # File with the same name was not found in replica folder
            self.copy_file(s_file.path)
            s_entries_checked.append(s_file.name)

    def compare_folder_content_recursive(self, source_path, replica_path):
        s_entries_checked = []  # All entries that exist in source directory
        with os.scandir(source_path) as s_entries:
            with os.scandir(replica_path) as r_entries:
                for s_entry in s_entries:   # Go through each source folder item
                    if s_entry.is_dir():    # Item is a folder
                        self.compare_folder_with_entries(s_entry, r_entries, s_entries_checked)
                    else:   # Item is a file
                        self.compare_file_with_entries(s_entry, r_entries, s_entries_checked)

            # Delete files and folders that do not exist in source:
            with os.scandir(replica_path) as r_entries_updated:
                for r_entry in r_entries_updated:
                    if r_entry.name not in s_entries_checked:
                        if r_entry.is_dir():
                            self.delete_folder_recursive(r_entry.path)
                        else:
                            self.delete_file(r_entry.path)

    def replicate(self, source, replica):
        if not os.path.isdir(source):
            print("Source folder does not exist")
            return

        if not os.path.isdir(replica):
            os.makedirs(replica)

        self.compare_folder_content_recursive(source, replica)

    def run(self):
        while True:
            self.replicate(self.source_dir, self.replica_dir)
            time.sleep(int(self.interval))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--Source", help="Provide path to source folder")
    parser.add_argument("-r", "--Replica", help="Provide path to replica folder")
    parser.add_argument("-i", "--Interval", help="Provide synchronization interval in seconds")
    parser.add_argument("-l", "--Log", help="Provide path to a log file")
    return vars(parser.parse_args())


def get_file_hashsum(file_path):
    # Calculate the MD5 hash of a file.
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(CHUNK_SIZE):
            file_hash.update(chunk)
    return file_hash.hexdigest()


if __name__ == '__main__':

    # Argument parsing
    args_parsed = parse_args()
    source_dir = args_parsed['Source']
    replica_dir = args_parsed['Replica']
    interval = args_parsed['Interval']
    log_path = args_parsed['Log']

    log_f = open(f"{log_path}", "w")

    replicator = FolderReplicator(source_dir, replica_dir, interval, log_path)
    replicator.run()
