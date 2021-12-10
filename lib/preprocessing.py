#!/usr/bin/env python3

"""
    usage:

"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.5"

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

    def runPicard(self):
        outputDir = f'{self.outputDir}/Preprocessing'
        os.system(f"mkdir {outputDir}/temp")

        for alignedFiles in glob.glob(f'{outputDir}/aligned/*.bam'):
            os.system(f"cp {alignedFiles} {outputDir}/temp")
            file = re.search(r"[^/]+(?=\.bam)", alignedFiles).group(0)
            alignedFiles = f"{outputDir}/temp/{file}.bam"
            programs = [("", "SortSam", "SO=queryname", f"java -jar tools/picard.jar"),

                        ("SortSam", "AddOrReplaceReadGroups",
                         f"LB={file} PU={file} SM={file} PL=illumina CREATE_INDEX=true", f"java -jar tools/picard.jar"),

                        ("AddOrReplaceReadGroups", "FixMateInformation", "", f"java -jar tools/picard.jar"),

                        ("FixMateInformation", "MergeSamFiles", "CREATE_INDEX=true USE_THREADING=true",
                         f"java -jar tools/picard.jar"),

                        ("MergeSamFiles", "MarkDuplicates",
                         f"CREATE_INDEX=true METRICS_FILE={outputDir}/markDuplicates/{file}.metrics.log",
                         f"java -jar tools/picard.jar"),

                        ("MarkDuplicates", "sort -n", "", "samtools")]

            for program in programs:
                os.system(f"{program[3]} {program[1]} "
                          f"I={alignedFiles[:-4]}{program[0][0:4]}.bam "
                          f"O={alignedFiles[:-4]}{program[1][0:4]}.bam "
                          f"{program[2]}")

            os.system(f"mv {outputDir}/temp/{file}Sort.bam {outputDir}/markDuplicates/{file}_sorted.bam")

        os.system(f"rm -r {outputDir}/temp")


