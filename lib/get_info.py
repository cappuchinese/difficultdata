"""
Script for function "determine_genome_info"
"""

__author__ = "Lisa Hu"
__version__ = 1.0

from termcolor import colored


class GenomeInfo:
    """
    This module contains 3 different directories:

    - genomeHisat2, that contains the directory in this tool to the
    indexes of HiSat2 of the belonging genome.
    - gtfFile, that contains the directory in this tool. This file consists
    of the genome annotation.
    - genomeFast, that contains the directory in this tool. This file
    is the fasta file that is used to build the genomeHisat2 index in
    HiSat2.

    These directories are callable via the identifier
    :return: The directories according to the identifier
    """
    def __init__(self, identifier):
        self.identifier = identifier

    def determine_genome_info(self):
        """
        Function contains dictionary of directories for each identifier
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

        if self.identifier in organisms:
            return organisms[self.identifier]

        print(colored("Make sure the chosen organism is valid!", "red"))
        print("Use --help for more information")
        return None, None, None
