# Difficult data

This is a complete rewrite from an old python 2 pipeline to a streamlined multiprocessed object-oriented python 3 program.

## Contents
```bash
difficultdata
├── Code
│   ├── aligningMain.py
│   ├── createDirs.py
│   └── determineGenomeInfo.py
├── Fastqc_reports
├── README.md
├── bin
│   ├── TrimGalore-0.6.6
│   ├── hisat2
│   ├── picard.jar
│   ├── subread-2.0.2-source
├── config.ini
├── lib
│   ├── alignment.py
│   ├── pdf.py
│   ├── pipeline_funcs.py
│   ├── preprocessing.py
│   ├── qualitycheck.py
│   ├── trim_files.py
│   └── unzipper.py
├── main.py
├── requirements.txt
├── setup.sh
└── trim_galore.tar.gz


```

## Installation 
This program is ment for a linux system.

To install, go into the downloaded folder and run setup.sh 
```bash
setup.sh
```
If running the aforementioned command doesn't work copy the contents of setup.sh directly into your bash terminal,
this will install al the necessary files and dependencies 
* cutadapt
* multiqc
* custom python packages in requirements.ini
* fpdf
* Hisat2
* Trimgalore
* subread2.0.2

Please copy and run the following code in your terminal:
```bash
# Installation genome reference
if [ ! -d Genome ]; then
  mkdir Genome
  cd Genome
  mkdir Hisat_index
  wget ftp://ftp.ensembl.org/pub/release-84/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
  wget ftp://ftp.ensembl.org/pub/release-84/gtf/homo_sapiens/Homo_sapiens.GRCh38.84.gtf.gz
  wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/snp144Common.txt.gz
  gzip -d Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
  gzip -d Homo_sapiens.GRCh38.84.gtf.gz
  gzip -d snp144Common.txt.gz
  awk 'BEGIN{OFS="\t"} {if($2 ~ /^chr/) {$2 = substr($2, 4)}; if($2 == "M") {$2 = "MT"} print}' snp144Common.txt > snp144Common.txt.ensembl
  ../bin/hisat2/hisat2_extract_snps_haplotypes_UCSC.py Homo_sapiens.GRCh38.dna.primary_assembly.fa snp144Common.txt.ensembl Homo_sapiens
  cd ..
fi

```
This will download the necessary genome files, 
after that please run the following command in the terminal, this will build the Assembly Hisat2 requires with the downloaded genome:
```bash
hisat2-build /Genome/Homo_sapiens.GRCh38.dna.primary_assembly.fa /Hisat_index/Homo_sapiens.GRCh38.dna.primary_assemblytest
```

## Usage 

To run/use this script, run the following commands in the directory where Main.py is located.
```bash
usage:python3 main.py [-h] -d FASTQDIR -out OUTPUTDIR [-t TRIM]

optional arguments:
  -h, --help            show this help message and exit
  -d FASTQDIR, --fastqDir FASTQDIR
                        [REQUIRED] Directory to the fq.gz/fastq.gz files
  -out OUTPUTDIR, --outputDir OUTPUTDIR
                        [REQUIRED] Pathways to output directory
  -t TRIM, --trim TRIM  Define the last bp to keep for trimming

```
### Example:
```bash
python3 main.py -d /data/storix2/students/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data -o hs -out /students/2021-2022/Thema06/mpslik
```

After running the script and if you wish to create a PDF report, please run the following script in the main directory where Main.py is located: 
```bash
python3 lib/pdf.py -d <outputdirlocation>
```

## Output

The output should consist out of a combined PDF file in the output Directory ./PDF

## Interpretation of the PDF results 

##Example :
###SRR1106138_sum
FastQC	0.11.9
Basic Statistics	pass
###Measure	Value
- Filename	SRR1106138.fastq 
  - File type	Conventional base calls
  - Encoding	Sanger / Illumina 1.9
  - Total Sequences	5627599
  - Sequences flagged as poor quality	0
  - Sequence length	25-57
  - %GC	30  ***< check if this is correct for yopur organisme*** 
  - ***pass or fail for the mentioned statistic***
    - PASS	Basic Statistics	SRR1106138.fastq
    - FAIL	Per base sequence quality	SRR1106138.fastq
    - FAIL	Per sequence quality scores	SRR1106138.fastq
    - FAIL	Per base sequence content	SRR1106138.fastq
    - PASS	Per sequence GC content	SRR1106138.fastq
    - PASS	Per base N content	SRR1106138.fastq
    - WARN	Sequence Length Distribution	SRR1106138.fastq
    - PASS	Sequence Duplication Levels	SRR1106138.fastq
    - PASS	Overrepresented sequences	SRR1106138.fastq
    - PASS	Adapter Content	SRR1106138.fastq
- === Summary === ***< if this isnt present file was trimmed empty and quality was very bad.***
  - Total reads processed: 5,627,599
  - Reads with adapters: 0 (0.0%)
  - Reads written (passing filters): 5,627,599 (100.0%)
  - Total basepairs processed: 179,811,193 bp
  - Quality-trimmed: 179,811,193 bp (100.0%)
  - Total written (filtered): 0 bp (0.0%) ***< amount of left over base pairs after trimming***

## Authors
- Lisa Hu 
- Dennis Haandrikman 
- Orfeas Gkourlias
- Mats Slik
