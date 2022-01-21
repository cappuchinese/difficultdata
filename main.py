#!/usr/bin/python3

"""
Rewritten pipeline using old code as reference
"""

__author__ = "Lisa Hu"
__date__ = 2021.11
__version__ = 1.0

# Imports
import datetime
import os
import sys
import argparse
import configparser
from termcolor import colored

# Import self created modules
from lib.alignment import Alignment
from lib.pipeline_funcs import PipelineFuncs
from lib.preprocessing import Preprocessing
from lib.qualitycheck import QualityCheck
from lib.trim_files import TrimFiles
from lib.unzipper import Unzipper


def __arguments():
    """
    Parse terminal commands
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--fastqDir', required=True,
                        help='[REQUIRED] Directory to the fq.gz/fastq.gz files')
    parser.add_argument('-out', '--outputDir', required=True,
                        help='[REQUIRED] Pathways to output directory')
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
    time = datetime.datetime.now()
    print(time)
    # Get all the arguments and the config
    args = __arguments()
    config = read_config()

    # Create all the dictionaries
    pipeline_mod = PipelineFuncs(args.outputDir)
    pipeline_mod.create_all()

    # Unzip data files
    unzipper = Unzipper(args.outputDir)
    unzipper.multi_run(args.fastqDir)

    # Perform quality check
    quality = QualityCheck(args.outputDir)
    quality.multi_run()
    print(colored("  Finished fastqc", "green"))

    # Trim the files
    trimmer = TrimFiles(args.outputDir, args.trim, config["trimGalore"])
    trimmer.multi_trim()
    print(colored("  Finished trimming", "green"))

    # TODO commenting
    if not os.path.exists(f"{os.getcwd()}/Genome"):
        genome_dir = config["genomeDir"]
    else:
        genome_dir = f"{os.getcwd()}/Genome"

    genome_hisat = f"{genome_dir}/Hisat2_index"
    gtf = f"{genome_dir}/Homo_sapiens.GRCh38.84.gtf"
    genome_fasta = f"{genome_dir}/Homo_sapiens.GRCh38.dna.primary_assembly.fa"

    pipeline_mod.fasta_processing(genome_fasta, config["picard"])
    print(colored("  Finished genome fasta", "green"))

    # Perform alignment
    alignment = Alignment(args.outputDir, genome_hisat)
    alignment.main_process()

    # Preprocessing
    preprocessor = Preprocessing(args.outputDir)
    preprocessor.run_picard()

    # Generate count matrix
    pipeline_mod.write_file(gtf, config["featureCounts"])
    pipeline_mod.perform_multiqc()

    return 0


if __name__ == "__main__":
    EXITCODE = main()
    sys.exit(EXITCODE)
