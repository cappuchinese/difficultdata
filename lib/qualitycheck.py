"""
Module to check the quality
"""

# META VARIABLES
__author__ = "Lisa Hu"
__version__ = 1.0

# IMPORTS
import glob
from subprocess import Popen, PIPE
import concurrent.futures as confut
from termcolor import colored


def friendly_error(f_err):
    """
    This method creates user friendly error messages.
    :param f_err: The standard error of the fastqc tool.
    """
    # Make a list of each line in the error output:
    f_err = f_err.split('\n')
    # Define empty list of new error messages:
    errors = []

    for i, line in enumerate(f_err):
        if line.startswith('Failed to'):
            # Get the error explanation from the next line
            error = f_err[i + 1]
            # Save everything after ':'
            error_start = error.find(':')
            error = error[error_start:-1]
            # Add the current line and the error together to create a nice message
            error_message = f'{line}{error}'
            # Add the message to the list of error messages
            errors.append(error_message)
    # Return new error messages
    return '\n'.join(errors)


class QualityCheck:
    """
    Perform FastQC check and write output to Results/fastQC/ folder.
    """

    def __init__(self, outputdir):
        self.outdir = outputdir

    def __str__(self):
        """
        String representation of the module
        """
        return "Quality check on fasta files"

    def check(self, file):
        """
        Perform quality check on file
        :param file: Fastq file
        """
        # Create process
        command = [f"fastqc {file} -o {self.outdir}/Results/fastQC"]
        process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        # Get process outputs
        out, err = process.communicate()
        # Create friendly error message
        friendly_error(err)
        # Print output
        print(out)

    def multi_run(self):
        """
        Multiprocess the quality check
        """
        print(colored("Performing quality check...", "blue", attrs=["bold"]))

        # Get all .gz files
        files = glob.glob(f"{self.outdir}/RawData/fastqFiles/*.gz")
        correct_files = []
        for filename in files:
            unzipped = filename.rsplit(".", 1)[0]
            correct_files.append(unzipped)

        # Form the processes
        with confut.ProcessPoolExecutor() as executor:
            print(colored("  Running multi runs...", "yellow"))
            results = executor.map(self.check, correct_files)
