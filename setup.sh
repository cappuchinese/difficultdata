#!/usr/bin/env bash

# install packages
echo 'installing cutadapt...'
pip3 install cutadapt;
echo 'installing multiqc...'
pip3 install multiqc;
echo 'installing python packages...'
pip3 install -r requirements.txt

# installation hisat2
if [ ! -d bin/hisat2-2.2.1 ]; then
  cd bin
  git clone https://github.com/DaehwanKimLab/hisat2.git
  cd hisat2
  make
  cd ..
fi

# installation TrimGalore
if [ ! -d bin/trim_galore ]; then
  curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.6.tar.gz -o trim_galore.tar.gz
  tar xvzf trim_galore.tar.gz -C bin/
fi

# installation Subread
if [ ! -d bin/subread-2.0.3-source ]; then
  wget https://sourceforge.net/projects/subread/files/subread-2.0.3/subread-2.0.3-source.tar.gz
  tar xvzf subread-2.0.3-source.tar.gz -C bin/
  cd bin/subread-2.0.3-source/src
  make -f Makefile.Linux
  cd ../../..
fi

# installation genome reference
if [ ! -d Genome ]; then
  mkdir Genome
  cd Genome
  wget ftp://ftp.ensembl.org/pub/release-84/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
  wget ftp://ftp.ensembl.org/pub/release-84/gtf/homo_sapiens/Homo_sapiens.GRCh38.84.gtf.gz
  wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/snp144Common.txt.gz
  gzip -d Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
  gzip -d Homo_sapiens.GRCh38.84.gtf.gz
  gzip -d snp144Common.txt.gz
  awk 'BEGIN{OFS="\t"} {if($2 ~ /^chr/) {$2 = substr($2, 4)}; if($2 == "M") {$2 = "MT"} print}' snp144Common.txt > snp144Common.txt.ensembl
  hisat2_extract_snps_haplotypes_UCSC.py Homo_sapiens.GRCh38.dna.primary_assembly.fa snp144Common.txt.ensembl Homo_sapiens
  cd ..
fi
