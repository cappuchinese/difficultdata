"""
Module to make all the dictionaries that are going to be used
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import os
import sys
import subprocess


class CreateDirs:
    """
    Create the necessary dictionaries
    """
    def __init__(self, output_dir):
        directory = str(output_dir)
        # Strip the slash (no further use)
        if directory.endswith("/"):
            directory = directory.rstrip("/")

        # Empty output directory first
        if not len(os.listdir(output_dir)) == 0:
            print("Output directory is not empty. Delete all files and continue? (y/n)")
            answer = input().lower()

            # Empty the dictionary
            if answer == "y":
                subprocess.run(["rm", "-rfv", f"~/{directory}/*"], stdout=subprocess.STDOUT,
                               text=True, check=True)

            # Exit program if user does not want to empty the directory
            else:
                sys.exit("Empty output directory before continuing. Exiting program...")

        self.outdir = directory

    def __str__(self):
        """
        String representation of the object. Returns the instance variable output_dir
        """
        return f"Output directory: {self.outdir}"

    def build_outdir(self):
        """
        Check if output directory exist, otherwise create it.
        """
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def extend_outdir(self):
        """
        Check if Preprocessing directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/Preprocessing/"):
            os.makedirs(f"{self.outdir}/Preprocessing/")
            os.makedirs(f"{self.outdir}/Preprocessing/trimmed")
            os.makedirs(f"{self.outdir}/Preprocessing/aligned")
            os.makedirs(f"{self.outdir}/Preprocessing/sortedBam")
            os.makedirs(f"{self.outdir}/Preprocessing/addOrReplace")
            os.makedirs(f"{self.outdir}/Preprocessing/mergeSam")
            os.makedirs(f"{self.outdir}/Preprocessing/markDuplicates")

    def create_resdir(self):
        """
        Check if Results directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/Results/"):
            os.makedirs(f"{self.outdir}/Results/")
            os.makedirs(f"{self.outdir}/Results/alignment")
            os.makedirs(f"{self.outdir}/Results/fastQC")
            os.makedirs(f"{self.outdir}/Results/multiQC")

    def create_codedir(self):
        """
        Check if Code directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/Code/"):
            os.makedirs(f"{self.outdir}/Code/")
            os.makedirs(f"{self.outdir}/Code/aligningPipeline")
            os.makedirs(f"{self.outdir}/Code/analysis")

    def create_rawdir(self):
        """
        Check if RawData directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/RawData/"):
            os.makedirs(f"{self.outdir}/RawData/")
            os.makedirs(f"{self.outdir}/RawData/fastqFiles")
            os.makedirs(f"{self.outdir}/RawData/counts")

    def create_all(self):
        """
        Run all the functions written above
        """
        self.build_outdir()
        self.extend_outdir()
        self.create_resdir()
        self.create_codedir()
        self.create_rawdir()
