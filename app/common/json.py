"For storing json related processors and helper functions."

import copy
import json


def stringify_text_entries_deep(input_: dict,
                                keyword="text",
                                delimiter="\n",
                                exact_match=False) -> dict:
    out = copy.deepcopy()
    stringify_text_entries_shallow(keyword, delimiter, exact_match)
    return out


def stringify_text_entries_shallow(input_: dict,
                                   delimiter="") -> bool:
    """Search and replace dict string array containing word T|text
    into multiline string.

    This function will replace string dictionary arrays like
    {"text": ["foo", "bar]} -> {"text": "foobar"]}
    """
    def _is_str_list(obj):
        return type(obj) is list and \
               all([type(it) is str for it in obj])

    keywords = ["text", "Text"]
    changed = False
    stack = [input_]
    while stack:
        top = stack.pop()
        if type(top) is dict:
            for k, v in top.items():
                if type(k) is str and \
                   any([kw in k for kw in keywords]) and \
                   _is_str_list(v):
                    changed = True
                    top[k] = delimiter.join(v)
                elif type(v) is dict:
                    stack.append(v)
                elif type(v) is list:
                    stack += v
        elif type(top) is list:
            stack += top

    return changed


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
        try:
            json_ = json.load(infile)
        except json.decoder.JSONDecodeError as exc:
            # TODO: to be logged
            print(exc)
            return False

    stringify_text_entries_shallow(json_)

    with open(output_file, "w") as outfile:
        json.dump(json_, outfile)

    return True
