#!/usr/bin/env bash

# install packages
echo 'installing cutadapt...'
pip3 install cutadapt;
echo 'installing multiqc...'
pip3 install multiqc;
echo 'installing python packages...'
pip3 install -r requirements.txt

mkdir RawTools

# installation hisat2
if [[! -d bin/hisat2-2.2.1]]; then
  wget https://cloud.biohpc.swmed.edu/index.php/s/oTtGWbWjaxsQ2Ho/download -P RawTools/
  unzip -vl RawTools/hisat2-2.2.1-Linux_x86_64.zip -d bin/
  cd bin/hisat2-2.2.1
  make
  cd ../..
fi

# installation TrimGalore
if [[! -d bin/trim_galore]]; then
  cd RawTools
  curl -fsSL https://github.com/FelixKrueger/TrimGalore/archive/0.6.6.tar.gz -o trim_galore.tar.gz
  tar xvzf trim_galore.tar.gz -C bin/
fi

# installation Subread
if [[! -d bin/subread-2.0.3-source]]; then
  wget https://sourceforge.net/projects/subread/files/subread-2.0.3/subread-2.0.3-source.tar.gz/download
  tar xvzf subread-2.0.3-source -C bin/
  cd bin/subread-2.0.3-source/src
  make -f Makefile.Linux
  cd ../../..
fi
