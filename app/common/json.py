"For storing json related processors and helper functions."

import json

from app.common.utils import logger


def stringify_text_entries_shallow(input_: dict,
                                   delimiter="") -> bool:
    """Search and replace dict string array containing word T|text
    into multiline string.

    This function will replace string dictionary arrays like
    {"text": ["foo", "bar]} -> {"text": "foobar"]}
    """
    def _is_str_list(obj):
        return isinstance(obj, list) and \
               all(isinstance(it, str) for it in obj)

    keywords = ["text", "Text"]
    changed = False
    stack = [input_]
    while stack:
        top = stack.pop()
        if isinstance(top, dict):
            for k, val in top.items():
                if isinstance(k, str) and \
                   any(kw in k for kw in keywords) and \
                   _is_str_list(val):
                    changed = True
                    top[k] = delimiter.join(val)
                elif isinstance(val, dict):
                    stack.append(val)
                elif isinstance(val, list):
                    stack += val
        elif isinstance(top, list):
            stack += top

    return changed


def process_json(input_file: str,
                 output_file: str) -> bool:
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
    with open(input_file, "r", encoding="utf-8") as infile:
        try:
            json_ = json.load(infile)
        except json.decoder.JSONDecodeError as exc:
            logger.error(exc)
            return False

    stringify_text_entries_shallow(json_)

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(json_, outfile)

    return True
