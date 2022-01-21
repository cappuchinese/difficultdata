"""
Module to align the trimmed read files against a genome
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman "
__status__ = "PDF writing script, WIP"
__version__ = "N/A"

# IMPORTS
import glob
import concurrent.futures as confut
import subprocess
import os
import sys

from termcolor import colored
from fpdf import FPDF

title = "Project Chocokoffie"


class PDF(FPDF):
    def header(self):
        # font type -> Arial bold 16
        self.set_font("Arial", "B", 16)
        # Calculate the width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w)/2)
        # Write the title
        self.cell(w, h=9, txt=title, align="C")
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, chapter_title):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Title
        self.cell(0, 6, f'{chapter_title}', 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, file_name):
        # Read text file
        with open(file_name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Arial', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()

    def print_chapter(self, chapter_title, fastq_file):
        self.add_page()
        self.chapter_title(chapter_title)
        self.chapter_body(fastq_file)


class PDFWRITE:
    def __init__(self, outputdir):
        self.title = "Project Chocokoffie"
        self.pdf = PDF()
        self.pdf.set_title(self.title)
        self.pdf.set_author("Mats Slik, Lisa Hu, Orfeas Gkourlias, Dennis Haandrikman")
        self.outputdir = outputdir

    def file_grabber(self):
        information_files = glob.glob(f"{self.outputdir}/Preprocessing/aligned/*.txt")
        print(information_files)
        for fastq_file in information_files:
            test_title = fastq_file.split(".")[0]
            self.pdf.print_chapter(test_title, fastq_file)

    def output(self):
        self.pdf.output("/students/2021-2022/Thema06/dhaandrikman/Results/"
                        "fastQC/Results_FastQ_files.pdf", "F")

    def main_process(self):
        self.file_grabber()
        self.output()


def main():
    pdf = PDFWRITE("/students/2021-2022/Thema06/dhaandrikman")
    pdf.main_process()


if __name__ == '__main__':
    sys.exit(main())
