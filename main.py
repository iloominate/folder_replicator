import argparse
import os
import os.path
import time


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--Source", help="Provide path to source folder")
parser.add_argument("-r", "--Replica", help="Provide path to replica folder")
parser.add_argument("-i", "--Interval", help="Provide synchronization interval")
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
