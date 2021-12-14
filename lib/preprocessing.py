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
import concurrent.futures
import glob
from termcolor import colored

# TODO rewrite os.system to subprocess.run


class Preprocessing:
    """
    TODO class docstring
    """
    def __init__(self, output_dir):
        """"
        TODO OUTPUT MOET NOG VERANDER WORDEN NAAR ARGS.OUTPUT OFZO
        """
        self.outputDir = output_dir

    def run_picard(self):
        """
        TODO docstring
        TODO commenting
        :return:
        """
        print(colored("Perform the processing steps necessary to create count file...",
                      "blue", attrs=["bold"]))
        files = glob.glob(f'{self.outputDir}/aligned/*.bam')
        os.system(f"mkdir {self.outputDir}/temp")
        executor = concurrent.futures.ProcessPoolExecutor()
        executor.map(self.process_file, files)
        executor.shutdown()
        os.system(f"rm -r {self.outputDir}/temp")

    def process_file(self, file):
        """
        TODO docstring
        TODO commenting
        :param file:
        :return:
        """
        os.system(f"cp {file} {self.outputDir}/temp")
        file_name = re.search(r"[^/]+(?=\.bam)", file).group(0)
        file = f"{self.outputDir}/temp/{file_name}.bam"
        programs = [("", "SortSam", "SO=queryname", f"java -jar tools/picard.jar"),

                    ("SortSam", "AddOrReplaceReadGroups",
                     f"LB={file_name} PU={file_name} SM={file_name} PL=illumina CREATE_INDEX=true",
                     "java -jar tools/picard.jar"),

                    ("AddOrReplaceReadGroups", "FixMateInformation", "",
                     "java -jar tools/picard.jar"),

                    ("FixMateInformation", "MergeSamFiles", "CREATE_INDEX=true USE_THREADING=true",
                     "java -jar tools/picard.jar"),

                    ("MergeSamFiles", "MarkDuplicates", "CREATE_INDEX=true",
                     f"METRICS_FILE={self.outputDir}/markDuplicates/{file_name}.metrics.log",
                     "java -jar tools/picard.jar"),

                    ("MarkDuplicates", "sort -n", "", "samtools")]

        for program in programs:
            os.system(f"{program[3]} {program[1]} "
                      f"I={file[:-4]}{program[0][0:4]}.bam "
                      f"O={file[:-4]}{program[1][0:4]}.bam "
                      f"{program[2]}")

        os.system(f"mv {self.outputDir}/temp/{file_name}Sort.bam {self.outputDir}/markDuplicates/{file_name}_sorted.bam")
