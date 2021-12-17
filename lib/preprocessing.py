"""
Module which handles the preprocessing needs of the files using picard and samtools programs.
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.5"

# IMPORTS
import subprocess
import re
import concurrent.futures
import glob
from termcolor import colored

class Preprocessing:
    """
    Main class which handless the output directory and all nececary bam programs.
    """
    def __init__(self, output_dir):
        """"
        Initialises the object so that the output dir is recognized.
        """
        self.outputDir = args.outputDir

    def run_picard(self):
        """
        Detects the relevant files so that the programs can be executed on them.
        Calls upon process_file function for every bam file found.
        """
        print(colored("Perform the processing steps necessary to create count file...",
                      "blue", attrs=["bold"]))
        files = glob.glob(f'{self.outputDir}/aligned/*.bam')
        # Creates a temporary directory in which the module will apply all nececary steps leaidng up to the final file.
        subprocess.run(f"mkdir {self.outputDir}/temp", shell=True)
        # Initialises the multiprocessing module so all files can be finished seperately.
        executor = concurrent.futures.ProcessPoolExecutor()
        executor.map(self.process_file, files)
        executor.shutdown()
        # Remove the unnecessary files used in achieving the end file.
        subprocess.run(f"rm -r {self.outputDir}/temp", shell=True)

    def process_file(self, file):
        """
        Executes the programs which are specified in the programs list on the preprocessing files found.
        """
        # In case the final directory doesn't exist, create it.
        subprocess.run(f"mkdir -p {self.outputDir}/markDuplicates/", shell=True)
        subprocess.run(f"cp {file} {self.outputDir}/temp", shell=True)
        # Retrieve the file nasme from the file path.
        file_name = re.search(r"[^/]+(?=\.bam)", file).group(0)
        file = f"{self.outputDir}/temp/{file_name}.bam"

        # A list of program parameters to be called with the programs. Every tuple entry specifies something
        # [0] = Prior program, [1] = Next program, [2] = Program options, [3] = Command prefix.
        programs = [("", "SortSam", "SO=queryname", f"java -jar tools/picard.jar"),

                    ("SortSam", "AddOrReplaceReadGroups",
                     f"LB={file_name} PU={file_name} SM={file_name} PL=illumina CREATE_INDEX=true",
                     "java -jar tools/picard.jar"),

                    ("AddOrReplaceReadGroups", "FixMateInformation", "",
                     "java -jar tools/picard.jar"),

                    ("FixMateInformation", "MergeSamFiles", "CREATE_INDEX=true USE_THREADING=true",
                     "java -jar tools/picard.jar"),

                    ("MergeSamFiles", "MarkDuplicates", "CREATE_INDEX=true",
                     f"METRICS_FILE={self.outputDir}/markDuplicates/{file_name}.metrics.log",
                     "java -jar tools/picard.jar"),

                    ("MarkDuplicates", "sort -n", "", "samtools")]
        # Run every program on the file.
        # Append program names to file names as identifiers when looking for the previous file.
        for program in programs:
            subprocess.run(f"{program[3]} {program[1]} "
                      f"I={file[:-4]}{program[0][0:4]}.bam "
                      f"O={file[:-4]}{program[1][0:4]}.bam "
                      f"{program[2]}", shell=True)

        # Complete the preprocessing by moving the final file to the markDuplicates directory.
        subprocess.run(f"mv {self.outputDir}/temp/{file_name}Sort.bam "
                       f"{self.outputDir}/markDuplicates/{file_name}_sorted.bam", shell=True)
