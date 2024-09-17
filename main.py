import argparse
import os
import os.path
import time
import hashlib
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--Source", help="Provide path to source folder")
parser.add_argument("-r", "--Replica", help="Provide path to replica folder")
parser.add_argument("-i", "--Interval", help="Provide synchronization interval in seconds")
parser.add_argument("-l", "--Log", help="Provide path to a log file")


def md5(file_path):
    # Calculate the MD5 hash of a file.
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def log_message(content):
    print(content)
    log_f.write(content + "\n")


def copy_file(s_file_path, s_file_name):
    shutil.copy(s_file_path, replica_dir + s_file_name)
    log_message(f"File added: {replica_dir+s_file_name}")


def copy_folder_recursive(s_dir):
    # Create empty folder
    os.mkdir(replica_dir + s_dir.name)
    log_message(f"Folder created: {replica_dir + s_dir.name}")

    # Copy source folder content to new replica folder
    with os.scandir(s_dir) as s_entries:
        for s_entry in s_entries:
            if s_entry.is_dir():  # Recursive folder copy
                copy_folder_recursive(s_dir)
            else:  # File copy
                copy_file(s_entry.path, s_entry.name)


def delete_file(r_file_path):
    try:
        os.remove(r_file_path)
        log_message(f"File deleted: {r_file_path}")
    except OSError:
        raise Exception(f"Couldn't delete file: {r_file_path}")


def delete_folder_recursive(r_dir):
    with os.scandir(r_dir) as r_entries:
        for r_entry in r_entries:
            if r_entry.is_dir():  # Recursive folder deletion
                delete_folder_recursive(r_dir)
            else:   # File deletion
                delete_file(r_entry.path)
    try:
        os.remove(r_dir)
        log_message(f"File deleted: {r_dir}")
    except OSError:
        raise Exception(f"Couldn't delete folder: {r_dir}")


def compare_file_content(s_file_path, r_file_path):
    source_f_hash = md5(s_file_path)
    replica_f_hash = md5(r_file_path)
    if replica_f_hash != source_f_hash:
        shutil.copy(s_file_path, r_file_path)
        log_message(f"File modified: {r_file_path}")


def compare_folder_content_recursive(source_path, replica_path):


def replicate(source, replica):
    if not os.path.isdir(source):
        print("Source folder does not exist")
        return

    if not os.path.isdir(replica):
        os.makedirs(replica)

    compare_folder_content_recursive(source, replica)


if __name__ == '__main__':

    # Argument parsing
    args_parsed = vars(parser.parse_args())
    source_dir = args_parsed['Source']
    replica_dir = args_parsed['Replica']
    interval = args_parsed['Interval']
    log_path = args_parsed['Log']

    log_f = open(f"{log_path}", "w")

    while True:
        replicate(source_dir, replica_dir)
        time.sleep(int(interval))
