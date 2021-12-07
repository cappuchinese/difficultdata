"""
TODO program docstring
"""

__author__ = "Lisa Hu"
__version__ = 1.0
__status__ = "Uncommented"

import os
import glob
import subprocess
from termcolor import colored


class CopyAligningCode:
    """
    Copy all the code files
    """

    def __init__(self, output_dir):
        self.outdir = output_dir

    def __str__(self):
        """
        String representation of the module
        """
        return f"Output directory: {self.outdir}"

    def copy(self):
        """
        TODO docstring copy
        :return:
        """
        print(colored("Transfering first code files...", "blue", attrs=["bold"]))
        for files in glob.glob(f"{os.getcwd()}/*.py"):
            pythonfile = files.split("/")[-1]
            subprocess.run(["cp", files, self.outdir, "Code/aligningPipeline/", pythonfile])
