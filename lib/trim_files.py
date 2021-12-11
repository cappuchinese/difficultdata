"""
Module that trims the files
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import subprocess
import glob
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
        filename, ext = file_.split(".")[:2]

        # TODO find new trimmer
        if self.trim is None:
            print(colored("Trimming with Cutadapt default trims...", "yellow"))

            subprocess.run(["cutadapt", "-a", "", file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                            f"{self.outdir}/Preprocessing/trimmed/{filename}_trimmed.{ext}"],
                           stdout=subprocess.STDOUT, text=True, check=True)

        else:
            print(colored("Trimming with fastx_trimmer...", "yellow"))
            sep_trim = self.trim.split("-")

            if len(sep_trim) == 1:
                subprocess.run(["fastx_trimmer", "-l", self.trim, "-i",
                                file_.replace(f".{ext}.gz", f".{ext}"), "-o",
                                f"{self.outdir}/Preprocessing/trimmed/{filename}_trimmed.{ext}"],
                               stdout=subprocess.STDOUT, text=True, check=True)
            else:
                subprocess.run(["fastx_trimmer", "-f", sep_trim[0], "-l", sep_trim[1], "-i",
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
        with confut.ProcessPoolExecutor() as executor:
            results = executor.map(self.trimmer, files)

        for result in results:
            print(result)
