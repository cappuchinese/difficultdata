"""
This module is to align the sequences in the files with the trimmed reads
from the trim_files module. The trimmed reads are obtained from the trimmed reads folder or directly
from the other module.
The log file of the alignment is written to the following folder: "Results/Alignment".
This script also creates the .bam file for further use.
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman"
__status__ = "Alignment script, WIP"
__version__ = "0.5"

# Import modules
import concurrent.futures
import os
import glob
import subprocess

from termcolor import colored


class Alignment:
    """
    TODO class docstring
    """

    def __init__(self, outputdir, genomehs2):
        """
        :param outputdir: output directory
        :param genomehs2: genomeHiSat2 is the reference genome the alignments will be done against
        """
        self.outputdir = outputdir
        self.extension = r"f[ast]*q"
        self.genome = genomehs2

        self.files = glob.glob(f"{self.outputdir}/Preprocessing/trimmed/*.{self.extension}")
        self.unique_filenames_unpaired = []
        self.unique_filenames_paired = []
        self.unique_filenames = []
        self.paired_files = {}

    def main_process(self):
        """
        TODO docstring
        TODO: 1 pair check to prevent crashing, load in the names of the files & make sure only
         unique files are added for alignment
        """
        print(colored("Starting the alignment process", "blue", attrs=["bold"]))

        # Looping through the trimmed files
        for files in self.files:
            # checking if the file name is unique
            unique_flag = self.check_unique(files)
            if unique_flag:
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
                print(f"Duplicate file detected: {files}, skipped")

        # Form the processes
        with concurrent.futures.ProcessPoolExecutor() as executor:
            unpaired_alignments = executor.map(self.align, self.unique_filenames_unpaired)
            paired_alignments = executor.map(self.paired_align, self.paired_files)

        for result in unpaired_alignments:
            print(result)
        for result in paired_alignments:
            print(result)

    def check_unique(self, file):
        """
        simple function to compare a given file name with the list of files, to check if its a unique name

        :PARAM: file: a file name
        :RETURN: check_f: a TRUE or FALSE flag to be given back
        """

        check_f = False

        if self.files.count(file) == 1:
            check_f = True

        return check_f

    def paired_finder(self):
        """
        This function goes through the list of paired sequences and combines the 2 that are paired.
        """
        for file in self.unique_filenames_paired:
            sequence_name = file[0].split("_")
            if sequence_name in self.paired_files:
                self.paired_files[sequence_name].append(file)
            else:
                x = []
                self.paired_files[sequence_name] = x
                self.paired_files[sequence_name].append(file)

    def align(self, file_):
        """
        This function aligns the sequences in the files to the genome generated beforehand.
        :param file_:
        """
        filename = file_.split("/")
        fastq_name = filename[0].split(".")
        subprocess.run(["hisat2", "-x", f"./{self.genome}", "-U", f"{filename}", "2>",
                        f"{self.outputdir}/Results/alignment/{fastq_name.replace('_trimmed', '')}"
                        ".log", "|", "samtools", "view", "-Sbo",
                        f"{self.outputdir}/Preprocessing/aligned/"
                        f"{fastq_name.replace('_trimmed', '')}.bam -"],
                       stdout=subprocess.STDOUT, text=True, check=True)

    def paired_align(self, files):
        """
        This functions aligns the paired sequences in the files to the genome generated beforehand
        The input of this file needs to be 2 reads.
        :param files:
        """
        file_names = []
        for file in files:
            filename = file.split("/")
            file_names.append(filename)
            filename = filename[0].split(".")
            fastq_name = filename[0].split("_")

        subprocess.run(["hisat2", "-x", f"./{self.genome}", "-1", f"{file_names[0]}", "-2",
                        f"{file_names[0]}", "2>",
                        f"{self.outputdir}/Results/alignment/{fastq_name}.log",
                        "|", "samtools", "view", "-Sbo",
                        f"{self.outputdir}/Preprocessing/aligned/{fastq_name}.bam", "-"],
                       stdout=subprocess.STDOUT, text=True, check=True)
