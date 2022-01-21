# Difficult data

this is a complete rewrite from a old python 2 pipline to a streamlined multiprocessed object-oriented python 3 program

## contents
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

## instalation 

go into the downloaded folder and run setup.sh 
```bash
setup.sh

```
this will install al the necessory files en dependencies 
* cutadapt
* multiqc
* custom python packages in requirements.ini
* fpdf
* Hisat2
* Trimgalore
* subread2.0.2

please copy and  run the following in your terminal:
```bash
# installation genome reference
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
this will download the necessary genome files, 
after that please run the following command in the terminal:
```bash
hisat2-build /Genome/Homo_sapiens.GRCh38.dna.primary_assembly.fa /Hisat_index/Homo_sapiens.GRCh38.dna.primary_assemblytest
```

## usage 

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
### example:
```bash
python3 main.py -d /data/storix2/students/2019-2020/Thema06/project-data/How_to_deal_with_difficult_data/Data -o hs -out /students/2021-2022/Thema06/mpslik

```

## creators 
- Lisa Hu 
- Dennis Haandrikman 
- Orfeas Gkourlias
- Mats Slik
