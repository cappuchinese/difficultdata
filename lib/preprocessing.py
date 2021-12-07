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
        outputDir = f'{self.outputDir}/Preprocessing'
        programs = ["SortSam", "AddOrReplaceReadGroups"]
                    #, "FixMateInformation", "MergeSamFiles", "MarkDuplicates"]

        for alignedFiles in glob.glob(f'{outputDir}/aligned/*.bam'):
            file = re.search(r"[^/]+(?=\.bam)", alignedFiles).group(0)
            options = ["SO=queryname",
                       f"LB={file} PU={file} SM={file} PL=illumina CREATE_INDEX=true"]
            for program in programs:
                os.system(f"{self.picard} {program} "
                          f"I={alignedFiles} "
                          f"O={alignedFiles} "
                          f"{options[programs.index(program)]}")
            #os.system(f"mv {alignedFiles} {outputDir}/markDuplicates")


# os.system(
#     "java -jar " + picard + " AddOrReplaceReadGroups INPUT=" + outputDir + "/Preprocessing/sortedBam/" + currentFile + ".bam OUTPUT=" + outputDir + "/Preprocessing/addOrReplace/" + currentFile + ".bam " + " LB=" + currentFile + " PU=" + currentFile + " SM=" + currentFile + " PL=illumina CREATE_INDEX=true")
# os.system(
#     "java -jar " + picard + " FixMateInformation INPUT=" + outputDir + "/Preprocessing/addOrReplace/" + currentFile + ".bam")
# os.system(
#     "java -jar " + picard + " MergeSamFiles INPUT=" + outputDir + "/Preprocessing/addOrReplace/" + currentFile + ".bam OUTPUT=" + outputDir + "/Preprocessing/mergeSam/" + currentFile + ".bam " + " CREATE_INDEX=true USE_THREADING=true")
# os.system(
#     "java -jar " + picard + " MarkDuplicates INPUT=" + outputDir + "/Preprocessing/mergeSam/" + currentFile + ".bam OUTPUT=" + outputDir + "/Preprocessing/markDuplicates/" + currentFile + ".bam " + " CREATE_INDEX=true METRICS_FILE=" + outputDir + "/Preprocessing/markDuplicates/" + currentFile + ".metrics.log")
# os.system(
#     "samtools sort -n " + outputDir + "/Preprocessing/markDuplicates/" + currentFile + ".bam -o " + outputDir + "/Preprocessing/markDuplicates/" + currentFile + "_sorted.bam")


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
