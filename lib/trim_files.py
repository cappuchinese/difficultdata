"""
Module that trims the files
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import subprocess
import glob
from multiprocessing import Process
from subprocess import run as sub_run
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
        :return:
        """
        filename, ext = file_.split(".")[:2]

        if self.trim is None:
            print(colored("Trimming with trim_galore...", "yellow"))

            sub_run([self.galore, "--path_to_cutadapt ~/.local/bin/cutadapt",
                     file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                     f"{self.outdir}/Preprocessing/trimmed"],
                    stdout=subprocess.STDOUT, text=True, check=True)

        else:
            print(colored("Trimming with fastx_trimmer...", "yellow"))
            sep_trim = self.trim.split("-")

            if len(sep_trim) == 1:
                sub_run(["fastx_trimmer", "-l", self.trim, "-i",
                         file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                         f"{self.outdir}/Preprocessing/trimmed/{filename}_trimmed.{ext}"],
                        stdout=subprocess.STDOUT, text=True, check=True)
            else:
                sub_run(["fastx_trimmer", "-f", sep_trim[0], "-l", sep_trim[1], "-i",
                         file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                         f"{self.outdir}/Preprocessing/trimmed/{filename}_trimmed.{ext}"],
                        stdout=subprocess.STDOUT, text=True, check=True)

    def multi_trim(self, fastqdir):
        """
        Multiprocess the trimming
        :param fastqdir: Directory with fastq files
        """
        print(colored("Trimming files...", "blue", attrs=["bold"]))

        # Get the files of the fastq directory
        files = glob.glob(f"{fastqdir}/*.gz")
        # Form the processes
        processes = [Process(target=self.trimmer, args=(file_,)) for file_ in files]

        for process in processes:
            process.start()
        for process in processes:
            process.join()
