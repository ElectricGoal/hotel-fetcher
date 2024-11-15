import ast
import pandas as pd
from typing import Union

class AggHelpers:
    """
    Helper functions for data aggregation.
    """
    @staticmethod
    def merge_lists(series: pd.Series) -> list:
        """
        Merge lists and remove duplicates

        :param series: The series to merge.
        :return: The merged list.
        """
        combined = []
        for item in series:
            # Convert string representation of lists to actual lists
            if isinstance(item, str):
                item = ast.literal_eval(item)
            if isinstance(item, list):
                combined.extend(item)

        # Remove duplicates and preserve order
        return list({str(e): e for e in combined}.values())

    @staticmethod
    def merge_dict_lists(series: pd.Series, key: str) -> list:
        """
        Merge dictionary lists and remove duplicates

        :param series: The series to merge.
        :param key: The key in dict to use for removing duplicates.
        :return: The merged list.
        """
        combined = []
        for item in series:
            # Convert string representation of lists to actual lists
            if isinstance(item, str):
                item = ast.literal_eval(item)
            if isinstance(item, list):
                combined.extend(item)

        # Remove duplicates and preserve order
        items = set()
        results = []
        for item in combined:
            link = item[key]
            if link is not None and link not in items:
                items.add(link)
                results.append(item)
       
        return results

    @staticmethod
    def merge_text(series: pd.Series ) -> str:
        """
        Merge text fields (combine non-null values)

        :param series: The series to merge.
        :return: The merged text.
        """
        return " ".join(filter(None, series))

    @staticmethod
    def first_valid_num(series: pd.Series) -> Union[float, None]:
        """
        Get the first number that is not null.

        :param series: The series to search.
        :return: The first valid number.
        """
        valid_values = series[series.notnull()]
        for val in valid_values:
            if isinstance(val, (int, float)):
                return val
            else:
                try:
                    return float(val)
                except ValueError:
                    continue
        return None

    @staticmethod
    def last_valid_num(series: pd.Series) -> Union[float, None]:
        """
        Get the last number that is not null.

        :param series: The series to search.
        :return: The last valid number.
        """
        valid_values = series[series.notnull()]
        for val in reversed(valid_values):
            if isinstance(val, (int, float)):
                return val
            else:
                try:
                    return float(val)
                except ValueError:
                    continue
        return None

    @staticmethod
    def first_valid_list(series: pd.Series) -> Union[list, None]:
        """
        Get the first list that is not null and not an empty list.

        :param series: The series to search.
        :return: The first valid list.
        """
        valid_values = pd.Series(
            series[series.notnull() & series.apply(lambda x: isinstance(x, list) and len(x) > 0)]
        )
        return valid_values.iloc[0] if not valid_values.empty else None

    @staticmethod
    def last_valid_list(series: pd.Series) -> Union[list, None]:
        """
        Get the last list that is not null and not an empty list.

        :param series: The series to search.
        :return: The last valid list.
        """
        valid_values = pd.Series(
            series[series.notnull() & series.apply(lambda x: isinstance(x, list) and len(x) > 0)]
        )
        return valid_values.iloc[-1] if not valid_values.empty else None

    @staticmethod
    def longest_valid_list(series: pd.Series) -> Union[list, None]:
        """
        Get the longest list that is not null and not an empty list.

        :param series: The series to search.
        :return: The longest list.
        """
        valid_values = pd.Series(
            series[series.notnull() & series.apply(lambda x: isinstance(x, list) and len(x) > 0)]
        )
        return valid_values.loc[valid_values.str.len().idxmax()] if not valid_values.empty else None

    @staticmethod
    def longest_valid_text(series: pd.Series) -> Union[str, None]:
        """
        Get the longest text that is not null and not an empty string.

        :param series: The series to search.
        :return: The longest text.
        """
        valid_values = pd.Series(
            series[series.notnull() & (series != '')]
        )
        return valid_values.loc[valid_values.str.len().idxmax()] if not valid_values.empty else None




class FormatHelpers:
    @staticmethod
    def df_to_formatted_json(df, sep="."):
        """
        The opposite function of json_normalize in dataframe.
        It converts a dataframe to a list of dictionaries.

        :param df: The dataframe to convert.
        :param sep: The separator used in the column labels.
        :return: A list of dictionaries representing the dataframe
        """
        result = []
        for _, row in df.iterrows():
            parsed_row = {}
            for col_label,v in row.items():
                keys = col_label.split(sep)

                current = parsed_row
                for i, k in enumerate(keys):
                    if i==len(keys)-1:
                        current[k] = v if v else None
                    else:
                        if k not in current.keys():
                            current[k] = {}
                        current = current[k]
            result.append(parsed_row)
        return result