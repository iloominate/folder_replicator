import argparse
import os
import os.path
import time


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--Source", help="Provide path to source folder")
parser.add_argument("-r", "--Replica", help="Provide path to replica folder")
parser.add_argument("-i", "--Interval", help="Provide synchronization interval")
parser.add_argument("-l", "--Log", help="Provide path to a log file")


def replicate(source, replica, log):
    if not os.path.isdir(source):
        print("Source folder does not exist")
        return

    if not os.path.isdir(replica):
        os.makedirs(replica)


if __name__ == '__main__':

    # Argument parsing
    args_parsed = vars(parser.parse_args())
    source_dir = args_parsed['Source']
    replica_dir = args_parsed['Replica']
    interval = args_parsed['Interval']
    log_path = args_parsed['Log']

    log_f = open(f"{log_path}", "w")

    while True:
        replicate(source_dir, replica_dir, log_f)
        time.sleep(interval)