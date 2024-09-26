from flask import Flask, request
import argparse
from pathlib import Path
import pandas as pd
import json

from api_package.ApiProcessor import ApiProcessor
from annotator_parser.AnnotatorParser import AnnotatorParser


app = Flask(__name__)


@app.route("/")
def index():
    return "To filter annotated data, use /getData?{filter}. Usage example:http://localhost:8000/getData?filter_by=AF_1000_genomes&operation=equal&value=0.5"


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
        # printing and saving query for convenience
        print(filtered_data_df)
        filtered_data_df.to_csv(f"variant_annotator/csv_filtered_data.csv", index=False)
        with open(f"variant_annotator/json_filtered_data.json", "w") as f:
            json.dump(filtered_data_dict, f)

        return filtered_data_dict


if __name__ == "__main__":
    p = argparse.ArgumentParser("API for VEP data")
    p.add_argument(
        "parsed_annotation_path", type=Path, help="Path to parsed annotation file"
    )
    args = p.parse_args()

    # reusing for convenince. TODO: make it a proper shared library
    api_parser = AnnotatorParser(
        annotation=Path(args.parsed_annotation_path), output_path=None
    )
    df_data = api_parser.get_vcf_content(api_parser.annotation)

    app.run(host="0.0.0.0", port=8000)
