"""
Module to check the quality
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import glob
import subprocess
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
        subprocess.run(["fastqc", file, "-o", f"{self.outdir}/Results/fastaQC"],
                       stdout=subprocess.STDOUT, text=True, check=True)

    def multi_run(self, fastqdir):
        """
        Multiprocess the quality check
        :param fastqdir: Directory with fastq files
        """
        print(colored("Performing quality check...", "blue", attrs=["bold"]))

        # Get all .gz files
        files = glob.glob(f"{fastqdir}/*.gz")
        # Form the processes
        with confut.ProcessPoolExecutor() as executor:
            results = executor.map(self.check, files)

        for result in results:
            print(result)
