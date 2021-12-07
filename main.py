#!/usr/bin/python3

"""
Rewritten pipeline using old code as reference
"""

__author__ = "Lisa Hu"
__date__ = 2021.11
__version__ = 1.0

# Imports
import sys
import argparse
import configparser

# Import self created modules
from lib.create_dirs import CreateDirs
from lib.fasta_processing import FastaProcessing
from lib.get_info import GenomeInfo
from lib.qualitycheck import QualityCheck
from lib.trim_files import TrimFiles


def __arguments():
    """
    Parse terminal commands
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--fastqDir', required=True,
                        help='[REQUIRED] Directory to the fq.gz/fastq.gz files')
    parser.add_argument('-o', '--organism', required=True,
                        help='[REQUIRED] Define the two letter id for the organism for the '
                             'alignment:\nHuman=hs\nMouse=mm\nMacaque=mmu\nRat=rn')
    parser.add_argument('-out', '--outputDir', required=True,
                        help='[REQUIRED] Pathways to output directory')
    parser.add_argument('-s', '--seqType', required=True,
                        help='[REQUIRED] Define SE for single end sequencing or '
                             'PE for paired end sequencing')
    parser.add_argument('-p', '--threads', help='Define number of threads to use')
    parser.add_argument('-t', '--trim', help='Define the last bp to keep for trimming')

    # Save all of the defined parameters in the variable args.
    args = parser.parse_args()

    return args


def read_config():
    """
    Read the config file "config.ini" to get the pathways of tools
    :return: config information
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    default = config["DEFAULT"]

    return default


def main():
    """
    Main function of the pipeline
    :return 0: exitcode
    """
    # Get all the arguments and the config
    args = __arguments()
    config = read_config()

    # Create all the dictionaries
    dirs = CreateDirs(args.outputDir)
    dirs.create_all()

    # Perform quality check
    quality = QualityCheck(args.outputDir)
    quality.multi_run(args.fastqDir)

    # Trim the files
    trimmer = TrimFiles(args.outputDir, args.trim, config["trimGalore"])
    trimmer.multi_trim(args.fastqDir)

    return 0


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
