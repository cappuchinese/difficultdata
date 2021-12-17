"""
TODO program docstring
"""

# METADATA VARIABLES
__author__ = "Mats Slik"
__status__ = "WIP"
__version__ = "0.1"

# IMPORTS
import subprocess
from termcolor import colored


class FeatureCount:
    """
    class feature count: directs multiple paths to run the tool featureCount and creat a output file
    """
    def __init__(self, outputdir, gtffile):
        """
        initialization
        :param: outputdir: path to the output directory
        :param: gtffile: genome annotation file path
        """
        self.outputdir = outputdir
        self.feature_count = f"tools/Subread-2.0.0/bin/featureCounts"
        self.gtffile = gtffile

    def write_file(self):
        """
        perform featureCounts
        :param: gtffile: genome annotation file path
        """
        print(colored("Using featureCount...", "blue", attrs=["bold"]))
        subprocess.run([self.feature_count, "-a", {self.gtffile},
                        "-o", f"{self.outputdir}/RawData/counts/geneCounts.txt",
                        f"{self.outputdir}Preprocessing/markDuplicates/*_sorted.bam"],
                       stdout=subprocess.STDOUT, text=True, check=True)
