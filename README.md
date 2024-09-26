# VariantAnnotator
This repository contains an implementation of a bioinformatics pipeline that performs, based on the provided VCF file, the annotation of variants with gene, dbSNP ID, and frequency from at least one population database. Result is delivered through an API and an interactive web interface (Flask) that interacts with the API to filter variants by frequency and depth (DP).


## Minimum Requirements:
- Linux or macOS environment (Zsh or Bash shell)
- Docker
- Git
- 21 GB of available disk space
- Open port 8000 (verify by running: lsof -i :8000)


## Running the pipeline:

### 1. Download git repository:
```
$ git clone https://github.com/gabriela-reznik/VariantAnnotator.git
```

### 2. Build application (This will take several minutes)
```
$ cd VariantAnnotator/build
$ docker build --platform=linux/amd64 -t variant-annotator:latest .
```

### 3. Create a folder to get results and run docker interactive with it mounted. Note that you can also run it without mount if you don't want to recover any files.

```
$ mkdir results && cd results
$ docker run -it -p 8000:8000 -v .:/data -w / variant-annotator
```

### 4. Run everything you need inside that docker

* **Run(exec) snakemake** (This can take some minutes). You're ready for next step once you can see `Serving Flask app 'API'` in the LOG.
```
/# snakemake all -s /variant_annotator/Snakefile 
```

* **Finally filter data**

In case all runs well, you'll be able to query the output of the pipeline in your navigator by accessing
`http://localhost:8000/?{you query}`

query is expected to follow the model
```
        model = {
            "filter_by": {"DP", "AF_1000_genomes"},
            "operation": {"bigger_than", "smaller_than", "equal"},
            "value": "float",
        }
```

This means you can filter data by "DP" or "AF_1000_genomes", choose between operations "bigger_than", "smaller_than" or "equal" and provide a numerical value for the filtering.

Example usage:
`http://localhost:8000/getData?filter_by=AF_1000_genomes&operation=equal&value=0.5`

You'll be able to see the filtered data in your terminal and in the navigator. Output files are also available.

* To quit the API press CTRL+C

### 6. Optional - exporting filtered data and intermediate files
```
/# cp variant_annotator/NIST.vcf variant_annotator/annotated_NIST.vcf variant_annotator/parsed_annotation.csv variant_annotator/csv_filtered_data.csv variant_annotator/filtered_data_dict.json data
``` 
All files should be now in your local machine results/ directory.

### 7. Exit interactive docker container
```
/# exit
```