"""
Module to call upon the featureCounts tool
"""

# METADATA VARIABLES
__author__ = "Mats Slik"
__status__ = "Finished & checked"
__version__ = "1.0"

# IMPORTS
import subprocess
from termcolor import colored


class FeatureCount:
    """
    class feature count:    directs multiple paths to run the tool featureCount
                            and create a .bam output file & a geneCounts .txt file
    """
    def __init__(self, outputdir, gtffile):
        """
        initialization of the class
        :param: outputdir:  a string, path to the output directory
        :param: gtffile:    a string, genome annotation file path
        """
        self.outputdir = outputdir
        self.feature_count = f"bin/subread-2.0.3-source/bin/featureCounts"
        self.gtffile = gtffile

    def write_file(self):
        """
        perform the script used to run the featureCounts tool
        :param: gtffile:    a string, genome annotation file path
        :OUTPUT:            2 files, a .txt with gene counts and a .bam file with marked duplicates
        """
        print(colored("Using featureCount...", "blue", attrs=["bold"]))
        try:
            subprocess.run([self.feature_count, "-a", {self.gtffile},
                            "-o", f"{self.outputdir}/RawData/counts/geneCounts.txt",
                            f"{self.outputdir}Preprocessing/markDuplicates/*_sorted.bam"],
                           stdout=subprocess.STDOUT, text=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"command '{e.cmd}' return with error (code {e.returncode}): {e.output}")