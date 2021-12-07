#!/usr/bin/env python3

"""
    usage:

"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.1"

# IMPORTS
import sys
import re
import os
import argparse
import concurrent.futures
import glob

# CLASSES
class Preprocessing:
    """ Desc """
    def __init__(self, args):
        self.outputDir = args.outputDir
        self.picard = f"java -jar tools/picard.jar"

    def runPicard(self):
        for alignedFiles in glob.glob(f'{self.outputDir}/Preprocessing/aligned/*.bam'):
            file = re.search(r"[^/]+(?=\.bam)", alignedFiles).group(0)
            print(f"{self.picard} SortSam I={self.outputDir}/Preprocessing/aligned/{file}.bam O={self.outputDir}"
                      f"/Preprocessing/sortedBam/{file}.bam SO=queryname")
            os.system(f"{self.picard} SortSam I={self.outputDir}/Preprocessing/aligned/{file}.bam O={self.outputDir}"
                      f"/Preprocessing/sortedBam/{file}.bam SO=queryname")




# FUNCTIONS
def __arguments():
    """
    Parse terminal commands
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-out', '--outputDir', required=True,
                        help='[REQUIRED] Pathways to output directory')
    # Save all of the defined parameters in the variable args.
    args = parser.parse_args()

    return args

#with concurrent.futures.ProcessPoolExecutor() as executor:
   # executor.map(function, list)


# MAIN
def main(args):
    """ Main function """
    args = __arguments()
    x = Preprocessing(args)
    x.runPicard()
    # FINISH
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
