from flask import Flask, request
import argparse
from pathlib import Path
import pandas as pd

from api_package.ApiProcessor import ApiProcessor
from annotator_parser.AnnotatorParser import AnnotatorParser


app = Flask(__name__)


@app.route("/")
def index():
    return "To filter annotated data, use /getData?{filter}. Usage example:http://127.0.0.1:5000/getData?filter_by=AF_1000_genomes&operation=equal&value=0.5"


@app.route("/getData")
def getData():
    full_filter = dict(request.args)
    api_processor = ApiProcessor()
    message = api_processor.minimal_filter_validation(full_filter)
    if message:
        return message
    else:
        filtered_data_df, filtered_data_dict = api_processor.filter_data(
            df_data, full_filter
        )
        print(filtered_data_df)
        return filtered_data_dict


if __name__ == "__main__":
    p = argparse.ArgumentParser("API for VEP data")
    p.add_argument(
        "parsed_annotation_path", type=Path, help="Path to parsed annotation file"
    )
    args = p.parse_args()

    # reusing for convenince. TODO: make it a proper shared library
    annotation_parser = AnnotatorParser(annotation=Path(args.parsed_annotation_path))
    df_data = annotation_parser.get_vcf_content(annotation_parser.annotation)

    app.run(debug=True)
