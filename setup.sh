#!/usr/bin/env bash

# install packages
echo 'installing cutadapt...'
pip3 install cutadapt;
echo 'installing multiqc...'
pip3 install multiqc;
echo 'installing python packages...'
pip3 install -r requirements.txt
echo 'installing PyFPDF...'
pip3 install fpdf

if [ ! -d bin ]; then
  mkdir bin
fi

# installation hisat2
if [ ! -d bin/hisat2 ]; then
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
if [ ! -d bin/subread-2.0.2-source ]; then
  wget https://sourceforge.net/projects/subread/files/subread-2.0.2/subread-2.0.2-source.tar.gz
  tar xvzf subread-2.0.2-source.tar.gz -C bin/
  cd bin/subread-2.0.2-source/src
  make -f Makefile.Linux
  cd ../../..
fi
