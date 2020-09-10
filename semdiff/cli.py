import argparse

from semdiff import differs
from semdiff.loader import load


def parse_args():
    p = argparse.ArgumentParser()
    type_help = "One of " + ", ".join(differs.DIFFERS.keys())
    p.add_argument("-t", "--type", help=type_help, required=True)
    p.add_argument("files", nargs=2, help="Files to diff.")
    return p.parse_args()


def display(left, right, diffs):
    for diff in diffs:
        print("<<<<<<<<<<")
        if diff.left is not None:
            print(left[diff.left.mark.start:diff.left.mark.end])
        print("==========")
        if diff.right is not None:
            print(right[diff.right.mark.start:diff.right.mark.end])
        print(">>>>>>>>>>")

        print()


def main():
    load("semdiff.differs")

    args = parse_args()

    left, right = args.files
    differ = differs.DIFFERS[args.type]
    with open(left) as l:
        with open(right) as r:
            ldata = l.read()
            rdata = r.read()
            diffs = differ(ldata, rdata)
            display(ldata, rdata, diffs)


if __name__ == "__main__":
    main()
