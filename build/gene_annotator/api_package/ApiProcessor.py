import pandas as pd


class ApiProcessor:
    def invalid_filter_error(self, message) -> str:
        return f"Provided filter is invalid. {message}. Please provide a valid filter with the following components: filter_by, operation, value. Example usage: http://127.0.0.1:5000/getData?filter_by=AF_1000_genomes&operation=equal&value=0.5"

    def minimal_filter_validation(self, filter):
        model = {
            "filter_by": {"DP", "AF_1000_genomes"},
            "operation": {"bigger_than", "smaller_than", "equal"},
            "value": "float",
        }
        # check keys
        for key in model:
            if key not in filter:
                return self.invalid_filter_error(f"Missing key: {key}")

        # Check if 'filter_by' is valid
        if filter["filter_by"] not in model["filter_by"]:
            return f"Invalid value in 'filter_by': {filter['filter_by']}"

        # Check if 'operation' is valid
        if filter["operation"] not in model["operation"]:
            return f"Invalid value in 'operation': {filter['operation']}"

        # Check if 'value' is of the correct type
        try:
            filter["value"] = float(filter["value"])
        except ValueError:
            return f"Invalid value in 'value': {filter['value']}. Please provide a float value"

        return None

    def convert_df_to_dict(self, df: pd.DataFrame) -> dict:
        df.reset_index(drop=True, inplace=True)
        return df.to_dict("dict")

    def filter_data(
        self, annotation_df: pd.DataFrame, full_filter: dict
    ) -> pd.DataFrame:
        if full_filter["operation"] == "bigger_than":
            filtered_data_df = annotation_df[
                annotation_df[full_filter["filter_by"]] > full_filter["value"]
            ]
            return filtered_data_df, self.convert_df_to_dict(filtered_data_df)
        elif full_filter["operation"] == "smaller_than":
            filtered_data_df = annotation_df[
                annotation_df[full_filter["filter_by"]] < full_filter["value"]
            ]
            return filtered_data_df, self.convert_df_to_dict(filtered_data_df)
        elif full_filter["operation"] == "equal":
            filtered_data_df = annotation_df[
                annotation_df[full_filter["filter_by"]] == full_filter["value"]
            ]
            return filtered_data_df, self.convert_df_to_dict(filtered_data_df)
        else:
            return f"Invalid operation. Please provide a valid operation: bigger_than, smaller_than, equal"
