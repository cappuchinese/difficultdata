"""
Module to align the trimmed read files against a genome
"""

# METADATA VARIABLES
__author__ = "Dennis Haandrikman "
__status__ = "PDF writing script"
__version__ = "1.0"

# IMPORTS
import glob
import argparse
from fpdf import FPDF
from summary import SummaryWriter

# Global for the fdpf package
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
        # Arial bold 14
        self.set_font('Arial', 'B', 14)
        # Title
        self.cell(w=0, h=6, txt=f'{chapter_title}', ln=1, align='L')
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


class PDFWrite:
    def __init__(self, outputdir):
        self.title = "Project Chocokoffie"
        self.pdf = PDF()
        self.pdf.alias_nb_pages()
        self.pdf.set_title(self.title)
        self.pdf.set_author("Mats Slik, Lisa Hu, Orfeas Gkourlias, Dennis Haandrikman")
        self.outputdir = outputdir

    def file_grabber(self):
        information_files = glob.glob(f"{self.outputdir}/Results/Summary/*.txt")
        for fastq_file in information_files:
            file_name = fastq_file.split("/")[-1]
            file_title = file_name.split(".")[0]
            self.pdf.print_chapter(file_title, fastq_file)

    def output(self):
        self.pdf.output(f"{self.outputdir}/PDF/Results_FastQ_files.pdf", "F")

    def main_process(self):
        sum_gen = SummaryWriter(self.outputdir)
        sum_gen.main_summary()
        self.file_grabber()
        self.output()
        print("Finished generating the pdf.")


def main():

    parser = argparse.ArgumentParser(description="script to creat a single pdf report of the created results")
    parser.add_argument("-d", "--output directory", action='store_true', dest='outputdir',
                        help="put directory location where Main.py is located")

    arguments = parser.parse_args()
    create_pdf = PDFWrite(arguments.outputdir)


    return 0


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)