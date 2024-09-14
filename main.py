import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--Source", help="Provide path to source folder")
parser.add_argument("-r", "--Replica", help="Provide path to replica folder")
parser.add_argument("-i", "--Interval", help="Provide synchronization interval")
parser.add_argument("-l", "--Log", help="Provide path to a log file")


def replicate():
    args_parsed = vars(parser.parse_args())
    print(f"Source:{args_parsed['Source']}")
    print(f"Replica:{args_parsed['Replica']}")
    print(f"Interval:{args_parsed['Interval']}")
    print(f"Log file:{args_parsed['Log']}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    replicate()

