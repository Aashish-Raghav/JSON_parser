import argparse
import sys
from jsonparser import JSON_parser


def parseFile(filename):
    with open(filename, 'r', encoding='utf-8') as file_handle:
        content = file_handle.read()
    json_parser = JSON_parser(content)
    return json_parser.initializeParsing()


def main():
    parser = argparse.ArgumentParser(prog="JSON parser")
    parser.add_argument("filenames",nargs=argparse.REMAINDER)

    args = parser.parse_args()
    for filename in args.filenames:
        parsed_data = parseFile(filename)
        print(parsed_data)
    

if __name__ == '__main__':
    main()
    