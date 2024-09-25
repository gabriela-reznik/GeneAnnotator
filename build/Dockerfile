FROM ensemblorg/ensembl-vep

USER root

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir pandas flask flask-restful snakemake

# Install conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && /opt/conda/bin/conda clean -tip

# Make conda available in the path
ENV PATH="/opt/conda/bin:$PATH"

# Install snakemake using conda, ensuring all dependencies are resolved
# RUN conda config --append channels conda-forge
RUN conda install -n base -c conda-forge mamba
RUN mamba install -c conda-forge -c bioconda snakemake

# copying all necessary code
COPY gene_annotator /gene_annotator

# get vep cache now so that run is faster
RUN mkdir -p /gene_annotator/vep_cache
RUN cd /gene_annotator/vep_cache && \
    wget --progress=bar:force:noscroll https://ftp.ensembl.org/pub/grch37/release-112/variation/indexed_vep_cache/homo_sapiens_vep_112_GRCh37.tar.gz && \
    tar -xzf homo_sapiens_vep_112_GRCh37.tar.gz && rm homo_sapiens_vep_112_GRCh37.tar.gz

# COPY gene_annotator/Snakefile /gene_annotator/Snakefile