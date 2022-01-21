"""
Module to unzip the fastq files
"""

# META VARIABLES
__author__ = "Lisa Hu"
__version__ = 1.0

# IMPORTS
import os
import glob
import subprocess
import concurrent.futures as confut
from termcolor import colored


class Unzipper:
    """
    Class that unzips the fastq.gz files
    """
    def __init__(self, outdir):
        self.outdir = outdir

    def multi_run(self, fastqdir):
        """
        The main process for the unzipper, collects the files needed and processes them with
        the unzip_fastq function.
        :param fastqdir:    Directory of fastq files
        :return:            a directory with unzipped fastq files
        """
        # Get the files of the fastq directory
        files = glob.glob(f"{fastqdir}/*.gz")

        for file_ in files:
            # Split to filenames
            full_filename = file_.split("/")[-1]

            # Copy the gzipped files to RawData
            if not os.path.exists(f"{self.outdir}/RawData/fastqFiles/{full_filename}"):
                print(colored(f"  Copy {full_filename} to RawData", "yellow"))
                cp_process = subprocess.Popen(["cp", file_,
                                               f"{self.outdir}/RawData/fastqFiles/{full_filename}"],
                                              stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                                              text=True)
                cp_process.wait()

        # Form the processor
        with confut.ProcessPoolExecutor() as executor:
            rawfiles = glob.glob(f"{self.outdir}/RawData/fastqFiles/*")
            results = executor.map(self.unzip_fastq, rawfiles)

    @staticmethod
    def unzip_fastq(file):
        """
        This module unzips the fastq files for trimming
        :param      file: the pathway for the fastq file.
        :return:    a file, unzipped
        """
        # Unzip the files for trimming
        try:
            print(colored(f"  Unzip {file}", "yellow"))
            subprocess.run([f"gzip -vkd {file}"], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command '{e.cmd}' return with error"
                               f"(code {e.returncode}): {e.output}")
