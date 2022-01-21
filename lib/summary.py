"""
Module to align the trimmed read files against a genome
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman "
__status__ = "Summary.txt writing script"
__version__ = "1.0"

# IMPORTS
import glob
import sys
import subprocess
import concurrent.futures as confut


class SummaryWriter:
    def __init__(self, outdir):
        self.outputdir = outdir
        self.fastq_files = glob.glob(f"{outdir}/RawData/fastqFiles/*.fastq")

    def unzip_multi(self):
        with confut.ProcessPoolExecutor() as executor:
            rawfiles = glob.glob(f"{self.outputdir}/Results/fastQC/*.zip")
            results = executor.map(self.unzip_fastq, rawfiles)

    def unzip_fastq(self, file):
        """
        This module unzips the fastq data files for information
        :param      file: the pathway for the fastq file.
        :return:    a file, unzipped
        """
        # Unzip the files for trimming
        command = [f"unzip {file} -d {self.outputdir}/Results/fastQC/"]
        proc = subprocess.Popen(command, shell=True)
        proc.wait()

    def read_files(self, fastq_file):
        file_name = fastq_file.split("/")[-1]
        fastq_identifier = file_name.split(".")[0]
        head_fastqc_data = []
        summary_data_saved =[]
        trimming_data_saved =[]

        try:
            with open(f"{self.outputdir}/Results/fastQC/{fastq_identifier}_fastqc/"
                      f"fastqc_data.txt", "r") as fastqc_data:
                head_fastqc_data = [next(fastqc_data).strip("\n") for x in range(10)]
        except FileNotFoundError:
            print(f"Couldn't find the {fastq_identifier}_fastqc/fastqc_data.txt file.")

        try:
            with open(f"{self.outputdir}/Results/fastQC/{fastq_identifier}_fastqc/"
                      f"summary.txt", "r") as summary_data:
                summary_data_saved = summary_data.read().splitlines()
        except FileNotFoundError:
            print(f"Couldn't fint the {fastq_identifier}_fastqc/summary.txt file.")

        try:
            with open(f"{self.outputdir}/Preprocessing/trimmed/{fastq_identifier}."
                      f"fastq_trimming_report.txt", "r") as trimming_data:
                for _ in range(22):
                    next(trimming_data)
                trimming_data_saved = [next(trimming_data).strip("\n") for x in range(10)]
        except FileNotFoundError:
            print(f"Couldn't find the {fastq_identifier}.fastq_trimming_report.txt file.")

        information = head_fastqc_data + summary_data_saved + trimming_data_saved
        return information, fastq_identifier

    def write_summary(self, information, identifier):
        with open(f"{self.outputdir}/Results/Summary/{identifier}_sum.txt", "w") as summary:
            for line in information:
                summary.write(f"{line}\n")

    def main_summary(self):
        self.unzip_multi()
        for file in self.fastq_files:
            information, identifier = self.read_files(file)
            self.write_summary(information, identifier)
        print("Finished generating summary files.")

def main():
    summary = SUMMARYWRITER("/students/2021-2022/Thema06/dhaandrikman")
    summary.main_summary()


if __name__ == '__main__':
    sys.exit(main())
