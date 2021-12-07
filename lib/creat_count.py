#!/usr/bin/env python3

"""
    usage:

"""

# METADATA VARIABLES
__author__ = "Mats Slik"
__status__ = "WIP"
__version__ = "0.1"

import subprocess


class FeatureCount:

    def __init__(self, outputdir, gtffile):
        """
        init
        """
        self.outputdir = outputdir
        self.feature_count = f"tools/Subread-2.0.0/bin/featureCounts"
        self.gtffile = gtffile

    def write_file(self):
        """

        """
        subprocess.run([self.feature_count,"-a", {self.gtffile},
                        "-o", f"{self.outputdir}/RawData/counts/geneCounts.txt", f"{self.outputdir}Preprocessing/markDuplicates/*_sorted.bam"],
                       stdout=subprocess.STDOUT, text=True, check=True)


