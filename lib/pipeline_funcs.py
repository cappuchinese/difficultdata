"""
Module to make all the dictionaries that are going to be used
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import os
import shutil
import sys
import glob
import subprocess
from termcolor import colored


class PipelineFuncs:
    """
    Functions used in the pipeline
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

    def _build_outdir(self):
        """
        Check if output directory exist, otherwise create it.
        """
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def _extend_outdir(self):
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

    def _create_resdir(self):
        """
        Check if Results directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/Results/"):
            os.makedirs(f"{self.outdir}/Results/")
            os.makedirs(f"{self.outdir}/Results/alignment")
            os.makedirs(f"{self.outdir}/Results/fastQC")
            os.makedirs(f"{self.outdir}/Results/multiQC")

    def _create_codedir(self):
        """
        Check if Code directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/Code/"):
            os.makedirs(f"{self.outdir}/Code/")
            os.makedirs(f"{self.outdir}/Code/aligningPipeline")
            os.makedirs(f"{self.outdir}/Code/analysis")

    def _create_rawdir(self):
        """
        Check if RawData directory exist, otherwise create it.
        """
        if not os.path.exists(f"{self.outdir}/RawData/"):
            os.makedirs(f"{self.outdir}/RawData/")
            os.makedirs(f"{self.outdir}/RawData/fastqFiles")
            os.makedirs(f"{self.outdir}/RawData/counts")

    def create_all(self):
        """
        Run all the directory methods
        """
        self._build_outdir()
        self._extend_outdir()
        self._create_resdir()
        self._create_codedir()
        self._create_rawdir()

    def copy_aligningcode(self):
        """
        TODO docstring copy
        :return:
        """
        print(colored("Transfering first code files...", "blue", attrs=["bold"]))
        for files in glob.glob(f"{os.getcwd()}/*.py"):
            pythonfile = files.split("/")[-1]
            subprocess.run(["cp", "-v", files, self.outdir, "Code/aligningPipeline/", pythonfile])

    def remove_folders(self):
        """
        Remove unnecessary folders
        :return:
        """
        if os.path.exists(f"{self.outdir}/Preprocessing/"):
            shutil.rmtree(f"{self.outdir}/Preprocessing/")

    @staticmethod
    def determine_genome_info(identifier):
        """
        This module contains 3 different directories:

        - genomeHisat2, that contains the directory in this tool
            to the indexes of HiSat2 of the belonging genome.
        - gtfFile, that contains the directory in this tool.
            This file consists of the genome annotation.
        - genomeFast, that contains the directory in this tool.
            This file is the fasta file that is used to build the genomeHisat2 index in HiSat2.

        These directories are callable via the identifier
        :return: The directories according to the identifier
        """
        organisms = {"hs": ["Genome/HiSat2/Homo_sapiens/GRCh38.92",
                            "Genome/Homo_sapiens.GRCh38.92.gtf",
                            "Genome/Homo_sapiens.GRCh38.dna_sm.primary_assembly.fa"],

                     "mmu": ["Genome/HiSat2/Macaca_mulatta/genome",
                             "Genome/Macaca_mulatta.Mmul_8.0.1.92.gtf",
                             "Macaca_mulatta.Mmul_8.0.1.dna.toplevel.fa"],

                     "mm": ["Genome/HiSat2/Mus_musculus/GRCm38",
                            "Genome/Mus_musculus.GRCm38.92.gtf",
                            "Genome/Mus_musculus.GRCm38.dna_sm.primary_assembly.fa"],

                     "rn": ["Genome/HiSat2/Rattus_norvegicus/Rnor6.0",
                            "Genome/Rattus_norvegicus.Rnor_6.0.93.gtf",
                            "Genome/Rattus_norvegicus.Rnor_6.0.dna_sm.toplevel.fa"],

                     "dr": ["Genome/HiSat2/Danio_rerio/GRCz11.93",
                            "Genome/Danio_rerio.GRCz11.93.gtf",
                            "Genome/Danio_rerio.GRCz11.93.dna_sm.primary_assembly.fa"]
                     }

        if identifier in organisms:
            return organisms[identifier]

        print(colored("Make sure the chosen organism is valid!", "red"))
        print("Use --help for more information")
        return None, None, None