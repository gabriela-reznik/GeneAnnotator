from AnnotatorParser import AnnotatorParser

from pathlib import Path
import argparse

p = argparse.ArgumentParser(
    "Annotator parser from raw VEP output to intended format/info"
)
p.add_argument("annotation_path", type=Path, help="Path to annotation file")
p.add_argument("parsed_output_path", type=Path, help="Path for parsed output")
args = p.parse_args()

parser = AnnotatorParser(
    annotation=Path(args.annotation_path), output_path=Path(args.parsed_output_path)
)
parser.export_parsed_information()
