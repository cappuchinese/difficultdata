"""
Module to check if fasta files exist
"""

__author__ = "Lisa Hu"
__date__ = 2021.11

import os
import subprocess
from termcolor import colored


class FastaProcessing:
    """
    Determine if the additional dict and index file of the organism fasta are created.
    """
    def __init__(self, genome_fasta, picard):
        self.gfasta = genome_fasta
        self.picard = picard

    def __str__(self):
        """
        String representation of the module
        """
        return f"Checking {self.gfasta}"

    def main_process(self):
        """
        Process the fasta file
        """
        print(colored("Processing genome fasta...", "blue", attrs=["bold"]))

        # Check if fasta.dict has been created
        if not os.path.isfile(self.gfasta.replace("fa", "dict")):
            # If not, create the file
            subprocess.run(f"java -jar {self.picard} CreateSequenceDictionary R={self.gfasta} "
                           f"O={self.gfasta.replace('fa', 'dict')})", stdout=subprocess.STDOUT,
                           text=True, check=True)

        # Check if fasta.fa.fai has been created
        if not os.path.isfile(f"{self.gfasta}.fai"):
            # If not, create the file
            subprocess.run(["samtools", "faidx", f"{self.gfasta}"], stdout=subprocess.STDOUT,
                           text=True, check=True)
