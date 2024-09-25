from pathlib import Path
from functools import cached_property
import pandas as pd
import re


class AnnotatorParser:
    def __init__(self, annotation: Path) -> None:
        self.annotation = annotation
        self.parsed_annotation_content = self.original_annotation_content

    @cached_property
    def original_annotation_content(self):
        return self.get_vcf_content(self.annotation)

    @cached_property
    def parsed_information(self):
        self.add_rsid_column()
        self.add_AF_1000_genomes_column()
        self.add_DP_column()
        return self.parsed_annotation_content

    def get_vcf_table_header(self, vcf: Path) -> list:
        f = open(vcf, "r")
        for line in f.readlines():
            if "CHROM" in line:
                vcf_header = line.strip().split("\t")
        return vcf_header

    def get_vcf_content(self, vcf: Path) -> pd.DataFrame:
        df = pd.read_csv(vcf, sep="\t", comment="#", header=None)
        df.columns = self.get_vcf_table_header(vcf)
        return df

    def add_rsid_column(self) -> None:
        """
        Get the rsid from Existing_variation annotation. Warning: might be unstable and dbSNP_ID might not match input ID field.
        """
        # get the rsid from annotated INFO field
        self.parsed_annotation_content["dbSNP_ID"] = self.parsed_annotation_content[
            "INFO"
        ].apply(
            lambda x: re.search(r"rs\d+", x).group(0)
            if re.search(r"rs\d+", x)
            else None
        )
        # TODO:minimal test for the function

    def add_AF_1000_genomes_column(self) -> None:
        """
        Add the AF from 1000 genomes project column to a column for future filtering. Warning: might be unstable.
        """
        # get the AF from annotated INFO field. It is supposed to be the firs info after "CSQ=".
        self.parsed_annotation_content[
            "AF_1000_genomes"
        ] = self.parsed_annotation_content["INFO"].apply(
            lambda x: re.search(r"CSQ=([\d.]+)", x).group(1)
            if re.search(r"CSQ=([\d.]+)", x)
            else None
        )
        # TODO:minimal test for the function

    def add_DP_column(self) -> None:
        """
        Add the DP information from original vcf INFO field to a column for future filtering.
        """
        self.parsed_annotation_content["DP"] = self.parsed_annotation_content["INFO"].apply(lambda x: re.search(r"DP=(\d+)", x).group(1) if re.search(r"DP=(\d+)", x) else None)

    def export_parsed_information(self, output_path: Path) -> None:
        self.parsed_information.to_csv(output_path, sep="\t", index=False)
        print(f"Exported parsed information to {output_path}")
