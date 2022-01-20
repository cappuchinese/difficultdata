"""
Module that trims the files
"""

# META VARIABLES
__author__ = "Lisa Hu"
__version__ = 1.0

# IMPORTS
import os
import subprocess
import glob
import shutil
import time
import gzip
import concurrent.futures as confut
from termcolor import colored


class TrimFiles:
    """
    The files are trimmed based on trim_galore if no parameter is given or by fastx_trimmer.
    trim_galore determined the cut off based on the quality of the reads
        and removes the adapters if necessary.
    fastx_trimmer requires an end bp or a beginning and an end bp for the trimming.
    """

    def __init__(self, output_dir, trim, trim_galore):
        self.outdir = output_dir
        self.trim = trim
        self.galore = trim_galore

    def trimmer(self, file_):
        """
        Trim the file
        :param file_:
        :return: extension
        """
        filename, ext, zip_ext = file_.split(".")

        if self.trim is None:
            subprocess.run([self.galore, file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                            f"{self.outdir}/Preprocessing/trimmed/"],
                           stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, check=True)

        else:
            sep_trim = self.trim.split("-")

            if len(sep_trim) == 1:
                subprocess.run(["fastx_trimmer", "-l", self.trim, "-i",
                                file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                                f"{self.outdir}/Preprocessing/trimmed/{filename}_trimmed.{ext}"],
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, check=True)
            else:
                subprocess.run(["fastx_trimmer", "-f", sep_trim[0], "-l", sep_trim[1], "-i",
                                file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                                f"{self.outdir}/Preprocessing/trimmed/{filename}_trimmed.{ext}"],
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, check=True)

    def multi_trim(self):
        """
        Multiprocess the trimming
        """
        print(colored("Trimming files...", "blue", attrs=["bold"]))

        # Form the processes
        with confut.ProcessPoolExecutor() as executor:
            # Prints for program progress
            if self.trim:
                print(colored("  Trimming with fastx_trimmer...", "yellow"))
            else:
                print(colored("  Trimming with TrimGalore...", "yellow"))

            files = glob.glob(f"{self.outdir}/RawData/fastqFiles/*")
            results = executor.map(self.trimmer, files)
