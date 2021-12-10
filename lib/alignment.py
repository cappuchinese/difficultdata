
"""
This module is to align the sequences in the files with the trimmed reads from the trim_files module.
# The trimmed reads are obtained from the trimmed reads folder or directly from the other module.
The log file of the alignment is written to the following folder: "Results/Alignment".
This script also creates the .bam file for futher use.
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman"
__status__ = "Alignment script, WIP"
__version__ = "0.5"

# Import modules
import concurrent.futures
import os
import glob
from termcolor import colored


class Alignment:

    def __init__(self, outputdir, extension, genomehisat2):
        # Outputdir is the output directory
        self.outputdir = outputdir
        # extension is the file extension, example: .fasta
        self.extension = extension
        # genomeHiSat2 is the reference genome the alignments will be done against
        self.genome = genomehisat2

    def main_process(self):
        """

        """
        # TODO: Write fancy colored console messages & 1 pair check to prevent crashing
        # Load in the names of the files & make sure only unique files are added for alignment
        print("Starting the alignment process")
        self.unique_filenames_unpaired = []
        self.unique_filenames_paired = []
        self.unique_filenames = []
        for files in glob.glob(f"{self.outputdir}/Preprocessing/trimmed/*.{self.extension}"):
            if files not in self.unique_filenames:
                self.unique_filenames.append(files)
                if len(files.split("_")) == 3:
                    self.unique_filenames_paired.append(files)
                else:
                    self.unique_filenames_unpaired.append(files)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            unpaired_alignments = executor.map(self.align, self.unique_filenames_unpaired)
            paired_alignments = executor.map(self.paired_align, self.paired_files)

        for result in unpaired_alignments:
            print(result)
        for result in paired_alignments:
            print(result)



    def paired_finder(self):
        """
        This function goes through the list of paired sequences and combines the 2 that are paired.
        :return:
        """
        self.paired_files = {}
        for file in self.unique_filenames_paired:
            sequence_name = file[0].split("_")
            if sequence_name in self.paired_files:
                self.paired_files[sequence_name].append(file)
            else:
                x = []
                self.paired_files[sequence_name] = x
                self.paired_files[sequence_name].append(file)

    def align(self, file):
        """
        This function aligns the sequences in the files to the genome generated beforehand.
        """
        filename = file.split("/")
        fastq_name = filename[0].split(".")
        os.system(f"hisat2 -x ./{self.genome} -U {filename} 2> "
                  f"{self.outputdir}/Results/alignment/{fastq_name.replace('_trimmed', '')}.log | samtools view -Sbo "
                  f"{self.outputdir}/Preprocessing/aligned/{fastq_name.replace('_trimmed', '')}.bam -")

    def paired_align(self, files):
        """
        This functions aligns the paired sequences in the files to the genome generated beforehand
        The input of this file needs to be 2 reads.
        """
        file_names = []
        for file in files:
            filename = file.split("/")
            file_names.append(filename)
            filename = filename[0].split(".")
            fastq_name = filename[0].split("_")

        os.system(f"hisat2 -x ./{self.genome} -1 {file_names[0]} -2 {file_names[0]} 2> "
                  f"{self.outputdir}/Results/alignment/{fastq_name}.log | samtools view -Sbo "
                  f"{self.outputdir}/Preprocessing/aligned/{fastq_name}.bam -")




