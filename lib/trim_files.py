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
            print(colored("  Trimming with TrimGalore...", "yellow"))

            subprocess.run([self.galore, file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                            f"{self.outdir}/Preprocessing/trimmed/"],
                           stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, check=True)

        else:
            print(colored("  Trimming with fastx_trimmer...", "yellow"))
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
        processed_files = []

        for file_ in files:
            # Split to filenames
            full_filename = file_.split("/")[-1]
            filename, ext = full_filename.split(".")[:2]

            # Copy the gzipped files to RawData
            print(colored("  Copy .gz files to RawData", "yellow"))
            if not os.path.exists(f"{self.outdir}/RawData/fastqFiles/{full_filename}"):
                subprocess.run(["cp", "-v", file_,
                                f"{self.outdir}/RawData/fastqFiles/{full_filename}"],
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, check=True)

            # Unzip the files for trimming
            print(colored("  Unzip the files for trimming", "yellow"))
            if not os.path.exists(f"{fastqdir}/{filename}.{ext}"):
                file_path = f"{self.outdir}/RawData/fastqFiles/{full_filename}"
                with gzip.open(file_path, "rb") as zip_obj:
                    with open(f"{self.outdir}/RawData/fastqFiles/{filename}.{ext}", "wb") as unzip:
                        shutil.copyfileobj(zip_obj, unzip)
            #     subprocess.run(["gzip", "-vd",
            #                     f"{self.outdir}/Rawdata/fastqFiles/{full_filename}"],
            #                    stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            #                    stderr=subprocess.STDOUT, text=True, check=True)
            processed_files.append(f"{self.outdir}/RawData/fastqFiles/{filename}.{ext}")

        # Form the processes
        with confut.ProcessPoolExecutor() as executor:
            results = executor.map(self.trimmer, processed_files)
            print(colored("  Finished trimming", "green"))
