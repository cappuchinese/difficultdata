"""
Module to check the quality
"""

# META VARIABLES
__author__ = "Lisa Hu"
__version__ = 1.0

# IMPORTS
import glob
from subprocess
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
        TODO
        :param fastqdir: Directory of fastq files
        :return:
        """
        # Get the files of the fastq directory
        files = glob.glob(f"{fastqdir}/*.gz")

        for file_ in files:
            # Split to filenames
            full_filename = file_.split("/")[-1]

            # Copy the gzipped files to RawData
            if not os.path.exists(f"{self.outdir}/RawData/fastqFiles/{full_filename}"):
                print(colored(f"  Copy {full_filename} to RawData", "yellow"))
                cp_process = subprocess.Popen(["cp", "-v", file_,
                                               f"{self.outdir}/RawData/fastqFiles/{full_filename}"],
                                              stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                                              text=True)

        # Form the processor
        with confut.ProcessPoolExecutor() as executor:
            results = executor.map(self.unzip_fastq, files)

    def unzip_fastq(self, file):
        """
        TODO
        :param file:
        :return:
        """
        # Unzip the files for trimming
        try:
            print(colored(f"  Unzip {file}", "yellow"))
            subprocess.run(f"gzip -vkd {self.outdir}/RawData/fastqFiles/{file}",
                           stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command '{e.cmd}' return with error"
                               f"(code {e.returncode}): {e.output}")
