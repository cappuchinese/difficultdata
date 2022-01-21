"""
Module to align the trimmed read files against a genome
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman & Mats Slik"
__status__ = "Alignment script, WIP"
__version__ = "1.0"

# IMPORTS
import concurrent.futures
import glob
import subprocess
import sys
import os

from termcolor import colored


class Alignment:
    """
    This class is for the functionality of aligning paired & unpaired trimmed reads to an
    established hisat2 genome and then output the alignments as a .bam file.
    The trimmed reads are obtained from the trimmed reads folder.
    The log file_ of the alignment is written to the following folder: "Results/Alignment".
    """

    def __init__(self, outputdir, hisat_genome):
        """
        Initialize the class and all the arguments needed.

        :param outputdir:   a string, the output directory
        :param genomehs2:   genomeHiSat2 is the reference genome,
                            that the alignments will be aligned against
        """
        self.outputdir = outputdir
        self.extension = "fq"
        self.genome = hisat_genome

        self.files = glob.glob(f"{self.outputdir}/Preprocessing/trimmed/*.{self.extension}")
        self.unique_filenames_unpaired = []
        self.unique_filenames_paired = []
        self.unique_filenames = []
        self.paired_files = {}

    def main_process(self):
        """
        This is the main function of the file.
        This function calls upon all the other functions in the class to process the trimmed
        fasta/fastq files and align them against the hisat2 genome,
        creating .bam/.sam files in the process.
        """
        print(colored("Starting the alignment process", "blue", attrs=["bold"]))

        print(f"Looking in the following folder {self.outputdir}/Preprocessing/trimmed/")
        # Looping through the trimmed files
        for files in self.files:
            print(f"Found file: {files} in folder: {self.outputdir}")   # debug
            # checking if the file_ name is unique
            unique_flag = self.check_unique(files)
            if unique_flag:
                print(f"{files} passed the unique_flag statement")  # Debug
                if files not in self.unique_filenames:
                    # Add the unique filenames to a list
                    self.unique_filenames.append(files)
                    if len(files.split("_")) == 3:
                        # If there are 3 parts in the filename, it means a paired alignment
                        self.unique_filenames_paired.append(files)
                    else:
                        # Else it is an unpaired alignment
                        self.unique_filenames_unpaired.append(files)
            else:
                print("Duplicate file_ detected: " + colored(files, "green") + " -> skipped")
        print(f"The list of unique filenames is as follows:\n{self.unique_filenames}")  # Debug
        # If pair-ended files are included, attempt to combine the pairs
        if len(self.unique_filenames_paired) > 1:
            self._paired_finder()
        print(f'here{self.unique_filenames_unpaired}')
        print(colored("  Amount of unpaired: ", "yellow") + str(len(self.unique_filenames_unpaired)))
        print(colored("  Amount of paired: ", "yellow") + str(len(self.paired_files)))

        # Form the processes
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.align, self.unique_filenames_unpaired)  # The unpaired alignments
            executor.map(self.paired_align, self.paired_files)  # The paired alignments

        print(colored("  Finished with alignment of the files.", "yellow"))

    def check_unique(self, file):
        """
        Simple function to compare a given file_ name with the list of files,
        to check if its a unique name

        :PARAM: file:       string, a file_ name
        :RETURN: check_f:   boolean, a TRUE or FALSE flag to be given back stating
                                    if the file_ is unique or not
        """

        check_f = False

        if self.files.count(file) == 1:
            if os.path.getsize(file) != 0:
                check_f = True
            else:
                print(colored(f"File: {file} doesn't have any bytes, will be excluded", "red"))

        return check_f

    def _paired_finder(self):
        """
        This function goes through the list of paired sequences and combines the 2 that are paired.
        It also sorts the files so that the r1 sequence is always the first in the list.
        These will be stored in self.paired_files.

        :OUTPUT: a dict containing lists, self.paired_files,
                this dict contains the paired_end files,
                coupled with each corresponding forward & reverse read.
        """
        for file_ in self.unique_filenames_paired:
            sequence_name = file[0].split("_")
            if sequence_name in self.paired_files:
                self.paired_files[sequence_name].append(file)
            else:
                x = []
                self.paired_files[sequence_name] = x
                self.paired_files[sequence_name].append(file)

        # Sort the lists in the dict so that r1 is always first in the list
        for key in self.paired_files:
            self.paired_files[key] = sorted(self.paired_files[key])

    def align(self, file_):
        """
        This function aligns the sequences in the files to the genome generated beforehand.

        :param file_: a string, the name & location of the file
        :OUTPUT: a .bam file, returns the alignment of unpaired reads to the genome in a .bam file
        """
        filename = file_.split("/")[-1]
        fastq_name = filename.split(".")[0]
        log_file = f"{self.outputdir}/Results/alignment/{fastq_name.replace('_trimmed', '')}.log"

        command = ["hisat2", f"-x {self.genome}/Homo_sapiens.GRCh38.dna.primary_assemblytest",
                   f"-U {self.outputdir}/Preprocessing/trimmed/{filename}",
                   f"-S {log_file}", "-p 2", "|", "samtools", "view", log_file, f"-Sbo {self.outputdir}/Preprocessing/aligned/{fastq_name.replace('_trimmed', '')}.bam"]
        hi = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

    def paired_align(self, files):
        """
        This functions aligns the paired sequences in the files to the genome generated beforehand
        The input of this file_ needs to be 2 reads.

        :param files:   a list with strings, a list of the pathway & name of 2 files.
        :OUTPUT:    a .bam file, output of the alignment of paired reads to the genome
                    in a .bam file
        """
        file_names = []
        # Extract the names of both files
        for file_ in files:
            filename = file_.split("/")
            file_names.append(filename)
            filename = filename[0].split(".")
        # Due to the paired reads having the same code,
        # fastq_name only needs to be established once
        fastq_name = filename[0].split("_")
        log_file = f"{self.outputdir}/Results/alignment/{fastq_name.replace('_trimmed', '')}.log"

        subprocess.run(["hisat2", "-x", f"./{self.genome}/Homo_sapiens.GRCh38.dna.primary_assemblytest", "-1", f"{file_names[0]}", "-2",
                        f"{file_names[1]}", "2>",
                        f"{self.outputdir}/Results/alignment/{fastq_name}.log",
                        "|", "samtools", "view", log_file, "-Sbo",
                        f"{self.outputdir}/Preprocessing/aligned/{fastq_name}.bam", "-"],
                       stdout=subprocess.STDOUT, text=True, check=True)
