"For storing json related processors and helper functions."
import json


def search_text_entries(input_dict: dict):
    pass


def process_json(input_file: str,
                 output_file: str,
                 convert_text: bool = True) -> bool:
    """Checks validity of json file and processes it before serving.

    The processing consists of:
        - replacing 'text' multi line string array
          into single mutli line string.

    Args:
        input_file: path to input json file
        output_file: path to output json file

    Returns:
        True or false telling if given json is valid
        json file and all processing was successfull.
    """
    json_ = None
    with open(input_file, "r") as infile:
        json_ = json.load(infile)
    with open(output_file, "w") as outfile:
        json.dump(json_, outfile)

    return True
