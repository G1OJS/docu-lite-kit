
import argparse
from .pbParse import *

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--out", help="Output file (defaults to stdout)")
parser.add_argument("--json", action="store_true", help="Emit JSON")
args = parser.parse_args()

pb = pbIO(args.infile)
output_path = args.out
output = pb.pbDumpJSON(output_path) if args.json else pb.pbPrint()

if output_path:
    with open(output_path, "w") as f:
        f.write(output)
else:
    if output is not None:
        print(output)
