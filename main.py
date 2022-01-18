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
from termcolor import colored

# Import self created modules
from lib.alignment import Alignment
from lib.pipeline_funcs import PipelineFuncs
from lib.preprocessing import Preprocessing
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
    # load_dotenv()
    args = __arguments()
    config = read_config()

    # Create all the dictionaries
    pipeline_mod = PipelineFuncs(args.outputDir)
    pipeline_mod.create_all()
    pipeline_mod.unzip_fastq(args.fastqDir)

    # Perform quality check
    quality = QualityCheck(args.outputDir)
    quality.multi_run()

    # Trim the files
    trimmer = TrimFiles(args.outputDir, args.trim, config["trimGalore"])
    trimmer.multi_trim()
    print(colored("  Finished trimming", "green"))

    # Determine right genome annotation
    genome_hisat, gtf, genome_fasta = pipeline_mod.determine_genome_info(args.organism,
                                                                         config["genomeDir"])

    # Make sure the fasta file of the right organism was chosen
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
