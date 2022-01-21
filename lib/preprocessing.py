"""
Module which handles the preprocessing needs of the files using picard and samtools programs.
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Ready to be test, WIP"
__version__ = "1.0"

# IMPORTS
import subprocess
import re
import concurrent.futures
import glob
from termcolor import colored


class Preprocessing:
    """
    Main class which handles the output directory and all necessary bam programs.
    """
    def __init__(self, output_dir):
        """
        Initialises the object so that the output dir is recognized.
        :param output_dir:      a string, contains the filepath for the output directory of this
                                script
        """
        self.outputDir = f"{output_dir}/Preprocessing"

    def run_picard(self):
        """
        Detects the relevant files so that the programs can be executed on them.
        Calls upon process_file function for every bam file found.
        """
        print(colored("Perform the processing steps necessary to create count file...",
                      "blue", attrs=["bold"]))
        files = glob.glob(f'{self.outputDir}/aligned/*.bam')
        # Creates a temporary directory in which the module will apply all necessary steps
        # leading up to the final file.
        subprocess.Popen(f"mkdir {self.outputDir}/temp", shell=True)
        copy = subprocess.Popen(f"cp {self.outputDir}/aligned/*.bam {self.outputDir}/temp", shell=True)
        copy.wait()
        print("test1")
        print(files)
        # Initialises the multiprocessing module so all files can be finished separately.
        executor = concurrent.futures.ProcessPoolExecutor()
        print("test2")
        executor.map(self.process_file, files)
        print("test3")
        executor.shutdown()
        print("test4")
        # Remove the unnecessary files used in achieving the end file.
        subprocess.run(f"rm -r {self.outputDir}/temp", shell=True)
        print("test5")

    def process_file(self, file):
        """
        Executes the programs which are specified in the programs list
        on the preprocessing files found.-
        :param file:        a string, contains the filepath & filename for the .bam file
        :return:            a file, a sorted .bam file
        """

        # Retrieve the file name from the file path.
        print(file)
        file_name = re.search(r"[^/]+(?=\.bam)", file).group(0)
        print(file_name)
        file = f"{self.outputDir}/temp/{file_name}.bam"

        # A list of program parameters to be called with the programs.
        # Every tuple entry specifies something
        # [0] = Prior program, [1] = Next program, [2] = Program options, [3] = Command prefix.
        programs = [("", "SortSam", "SO=queryname", f"java -jar bin/picard.jar"),

                    ("SortSam", "AddOrReplaceReadGroups",
                     f"LB={file_name} PU={file_name} SM={file_name} PL=illumina CREATE_INDEX=true",
                     "java -jar bin/picard.jar"),

                    ("AddOrReplaceReadGroups", "FixMateInformation", "",
                     "java -jar bin/picard.jar"),

                    ("FixMateInformation", "MergeSamFiles", "CREATE_INDEX=true USE_THREADING=true",
                     "java -jar bin/picard.jar"),

                    ("MergeSamFiles", "MarkDuplicates", "CREATE_INDEX=true",
                     f"METRICS_FILE={self.outputDir}/markDuplicates/{file_name}.metrics.log",
                     "java -jar bin/picard.jar"),

                    ("MarkDuplicates", "sort -n", "", "samtools")]
        # Run every program on the file.
        # Append program names to file names as identifiers when looking for the previous file.
        for program in programs:
            if program[0] != "MarkDuplicates":
                proc =  subprocess.Popen(f"{program[3]} {program[1]} "
                            f"I={file[:-4]}{program[0][0:4]}.bam "
                            f"O={file[:-4]}{program[1][0:4]}.bam "
                            f"{program[2]}", shell=True)
                proc.wait()

            else:
                proc =  subprocess.Popen(f"{program[3]} {program[1]} "
                                         f"{file[:-4]}Merg.bam -o "
                                         f"{file[:-4]}{program[0][0:4]}Mark.bam", shell=True)
                proc.wait()


        # Complete the preprocessing by moving the final file to the markDuplicates directory.
        subprocess.run(f"mv {self.outputDir}/temp/{file_name}Mark.bam "
                       f"{self.outputDir}/markDuplicates/{file_name}_sorted.bam", shell=True)
