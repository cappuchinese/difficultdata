"""
Module to check the quality
"""

# META VARIABLES
__author__ = "Lisa Hu"
__version__ = 1.0

# IMPORTS
import glob
from subprocess import Popen, check_call, PIPE
import concurrent.futures as confut
from termcolor import colored


class QualityCheck:
    """
    Perform FastQC check and write output to Results/fastQC/ folder.
    """

    def __init__(self, outputdir):
        self.outdir = outputdir

    def __str__(self):
        """
        String representation of the module
        """
        return "Quality check on fasta files"

    def check(self, file):
        """
        Perform quality check on file
        :param file: Fastq file
        """
        process = Popen(["fastqc", "--extract", file, "-o", f"{self.outdir}/Results/fastQC"],
                        stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)

        out, err = process.communicate()
        print(colored(f"Output: {out}", "green"))
        print(colored(f"Error: {err}", "red"))

    def multi_run(self):
        """
        Multiprocess the quality check
        """
        print(colored("Performing quality check...", "blue", attrs=["bold"]))

        # Get all .gz files
        files = glob.glob(f"{self.outdir}/RawData/fastqFiles/*.gz")
        correct_files = []
        for filename in files:
            unzipped = filename.rsplit(".", 1)[0]
            correct_files.append(unzipped)

        print(correct_files)
        # Form the processes
        with confut.ProcessPoolExecutor() as executor:
            print(colored("  Running multi runs...", "yellow"))
            results = executor.map(self.check, correct_files)
