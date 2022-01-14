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
        filename, ext = file_.split(".")

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

    def multi_trim(self, fastqdir):
        """
        Multiprocess the trimming
        :param fastqdir: Directory with fastq files
        """
        print(colored("Trimming files...", "blue", attrs=["bold"]))

        # Get the files of the fastq directory
        files = glob.glob(f"{fastqdir}/*.gz")

        for file_ in files:
            # Split to filenames
            full_filename = file_.split("/")[-1]
            unzipped_name = full_filename.rsplit(".", 1)[0]

            # Copy the gzipped files to RawData
            if not os.path.exists(f"{self.outdir}/RawData/fastqFiles/{full_filename}"):
                print(colored(f"  Copy {full_filename} to RawData", "yellow"))
                cp_process = subprocess.Popen(["cp", "-v", file_,
                                               f"{self.outdir}/RawData/fastqFiles/{full_filename}"],
                                              stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                                              text=True)
                cp_process.wait()

            # Unzip the files for trimming
            if not os.path.exists(f"{self.outdir}/RawData/fastqFiles/{unzipped_name}"):
                try:
                    print(colored(f"  Unzip {full_filename} for trimming", "yellow"))
                    subprocess.run(f"gzip -vd {self.outdir}/RawData/fastqFiles/{full_filename}",
                                   stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, check=True, shell=True)
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"command '{e.cmd}' return with error"
                                       f"(code {e.returncode}): {e.output}")

        # Form the processes
        with confut.ProcessPoolExecutor() as executor:
            # Prints for program progress
            if self.trim:
                print(colored("  Trimming with fastx_trimmer...", "yellow"))
            else:
                print(colored("  Trimming with TrimGalore...", "yellow"))

            files = glob.glob(f"{self.outdir}/RawData/fastqFiles/*")
            results = executor.map(self.trimmer, files)
