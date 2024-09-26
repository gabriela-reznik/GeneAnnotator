# GeneAnnotator
Implementing a bioinformatics pipeline that performs, based on the provided VCF file, the annotation of variants with gene, dbSNP ID, and frequency from at least one population database.Result is delivered through an API and an interactive web interface (Flask) that interacts with the API to filter variants by frequency and depth (DP).


Minimum Requirements:

Linux or macOS environment (Zsh or Bash shell)
Docker
Git
21 GB of available disk space
Open port 8000 (verify by running: lsof -i :8000)


1. download git repository
2. build application (This will take several minutes)
cd git/build
docker build --platform=linux/amd64 -t gene-annotator:latest .

3. create a folder to get results and run docker detached with it mounted
mkdir results && cd results


(you can also run it interactively if you prefer by using 
docker run -it -p 8000:8000 -v .:/data -w / gene-annotator)

4. Run everything you need inside that docker

4.a) run snakemake 
snakemake all -s gene_annotator/Snakefile 

4.b) filter data
in case all runs well, you'll be able to query the output of the pipeline in your navigator by accessing
http://localhost:8000/?{you query}

query is expected to follow the model
        model = {
            "filter_by": {"DP", "AF_1000_genomes"},
            "operation": {"bigger_than", "smaller_than", "equal"},
            "value": "float",
        }

This means you can filter data by "DP" or "AF_1000_genomes", choose between operations "bigger_than", "smaller_than" or "equal" and provide a numerical value for the filtering.

the parsed url should look like:
http://localhost:8000/getData?filter_by=AF_1000_genomes&operation=equal&value=0.5

You'll be able to see the filtered data in your terminal and in the navigator. Optional files are also available.

You can now close

6. Optional - exporting filtered data and intermediate files
Move your files to mounted folder by running
mv gene_annotator/NIST.vcf gene_annotator/annotated_NIST.vcf gene_annotator/parsed_annotation.csv gene_annotator/csv_filtered_data.csv gene_annotator/filtered_data_dict.json getData

all files should be now in your local machine results/ directory

7. stop and remove container