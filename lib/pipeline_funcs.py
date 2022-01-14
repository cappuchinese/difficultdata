"""
Module holds all the functions that do not need multiprocessing or multiple functional steps.
"""

# META VARIABLES
__author__ = "Lisa Hu"
__version__ = 1.0

# IMPORTS
import os
import glob
import shutil
import sys
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

        # Check if the output directory exist, else make
        if not os.path.isdir(output_dir):
            subprocess.run(["mkdir", output_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, check=True)

        # Empty output directory first
        if not len(os.listdir(output_dir)) == 0:
            print(colored("Output directory is not empty. Delete all files and continue? (y/n)",
                          "green"))
            answer = input().lower()

            # Empty the directory
            if answer == "y":
                print(colored("Emptying directory...", "red"))
                subprocess.run(["rm", "-rfv", f"{directory}/*"], stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, check=True)
                print(glob.glob(f"{directory}/RawData/fastqFiles/"))

            # Exit program if user does not want to empty the directory
            else:
                sys.exit(colored("Empty output directory before continuing. Exiting program...",
                                 "red"))

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
        print(colored("Creating all the dictionaries...", "blue", attrs=["bold"]))
        self._build_outdir()
        self._extend_outdir()
        self._create_resdir()
        self._create_codedir()
        self._create_rawdir()

    def remove_folders(self):
        """
        Remove unnecessary folders
        """
        print(colored("Removing Preprocessing folders...", "blue", attrs=["bold"]))
        if os.path.exists(f"{self.outdir}/Preprocessing/"):
            shutil.rmtree(f"{self.outdir}/Preprocessing/")

    @staticmethod
    def determine_genome_info(identifier, genome_path):
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

        organisms = {"hs": [f"{genome_path}/HiSat2/Homo_sapiens/GRCh38.92",
                            f"{genome_path}/Homo_sapiens.GRCh38.84.gtf",
                            f"{genome_path}/Homo_sapiens.GRCh38.dna.primary_assembly.fa"],

                     "mmu": [f"{genome_path}/HiSat2/Macaca_mulatta/genome",
                             f"{genome_path}/Macaca_mulatta.Mmul_8.0.1.92.gtf",
                             f"{genome_path}Macaca_mulatta.Mmul_8.0.1.dna.toplevel.fa"],

                     "mm": [f"{genome_path}/HiSat2/Mus_musculus/GRCm38",
                            f"{genome_path}/Mus_musculus.GRCm38.92.gtf",
                            f"{genome_path}/Mus_musculus.GRCm38.dna_sm.primary_assembly.fa"],

                     "rn": [f"{genome_path}/HiSat2/Rattus_norvegicus/Rnor6.0",
                            f"{genome_path}/Rattus_norvegicus.Rnor_6.0.93.gtf",
                            f"{genome_path}/Rattus_norvegicus.Rnor_6.0.dna_sm.toplevel.fa"],

                     "dr": [f"{genome_path}/HiSat2/Danio_rerio/GRCz11.93",
                            f"{genome_path}/Danio_rerio.GRCz11.93.gtf",
                            f"{genome_path}/Danio_rerio.GRCz11.93.dna_sm.primary_assembly.fa"]
                     }
        if identifier in organisms:
            return organisms[identifier]

        print(colored("Make sure the chosen organism is valid!", "red"))
        print("  Use --help for more information")
        return None, None, None

    def perform_multiqc(self):
        """
        Perform multiQC
        """
        print(colored(f"Performing multiqc on {self.outdir}", "blue", attrs=["bold"]))
        subprocess.run(["multiqc", self.outdir, "-o", f"{self.outdir}/Results/multiqc"],
                       stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, check=True)

    def write_file(self, gtffile, feature_count):
        """
        perform the script used to run the featureCounts tool
        :param: gtffile:    a string, genome annotation file path
        :OUTPUT:            2 files, a .txt with gene counts and a .bam file with marked duplicates
        """
        print(colored("Using featureCounts...", "blue", attrs=["bold"]))
        subprocess.run([feature_count, "-a", gtffile,
                        "-o", f"{self.outdir}/RawData/counts/geneCounts.txt",
                        f"{self.outdir}Preprocessing/markDuplicates/*_sorted.bam"],
                       stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, check=True)

    @staticmethod
    def fasta_processing(genome_fasta, picard):
        """
        Check if the fasta files exist
        :param genome_fasta: path to genome fasta file
        :param picard: path to the picard tool
        """
        print(colored("Processing genome fasta...", "blue", attrs=["bold"]))

        # Check if fasta.dict has been created
        if not os.path.isfile(genome_fasta.replace("fa", "dict")):
            print(colored("  Creating fasta.dict...", "yellow"))
            # If not, create the file
            subprocess.run(f"java -jar {picard} CreateSequenceDictionary R={genome_fasta} "
                           f"O={genome_fasta.replace('fa', 'dict')}", stdout=subprocess.PIPE,
                           stdin=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True,
                           shell=True)

        # Check if fasta.fa.fai has been created
        if not os.path.isfile(f"{genome_fasta}.fai"):
            print(colored("  Creating fasta.fa.fai...", "yellow"))
            # If not, create the file
            subprocess.run(["samtools", "faidx", f"{genome_fasta}"], stdout=subprocess.PIPE,
                           stdin=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
