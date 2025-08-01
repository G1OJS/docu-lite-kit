
import argparse
from .pbParse import *

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("--out", help = "Output file (json format)")
parser.add_argument("--noprint", action = 'store_true', help = "Don't print output to console")
args = parser.parse_args()

if(args.infile):
    pb = pbIO(args.infile)
    if(not args.noprint):
        pb.pbPrint()
    if(args.out):
        pb.pbDumpJSON(args.out) 

