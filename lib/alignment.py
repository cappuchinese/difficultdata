
"""
This module is to align the sequences in the files with the trimmed reads from the trim_files module.
# The trimmed reads are obtained from the trimmed reads folder or directly from the other module.
The log file of the alignment is written to the following folder: "Results/Alignment".
This script also creates the .bam file for futher use.
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman"
__status__ = "Alignment script, WIP"
__version__ = "0.3"

# Import modules
import concurrent.futures
import os
import glob


class Alignment:

    def __init__(self, OutputDir, extension):
        self.outputdir = OutputDir
        self.extension = extension

    def main_process(self):
        # TODO: Align the files and see about paired end alignments
        self.uniquefilenames = []
        files = glob.glob(f"{self.outputdir}/Preprocessing/trimmed/*.{self.extension}")


