from fastapi import APIRouter
import json
import pathlib
from app.common.json import stringify_text_entries_shallow
from app.common.file import get_files_by_type


class DynamicJsonRouter(APIRouter):

    @staticmethod
    def create_get_call(in_dict: dict) -> dict:
        def callable():
            return in_dict
        return callable

    def __init__(self, input_directory: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_directory = input_directory
        share_files = get_files_by_type(input_directory, "json")
        base = pathlib.Path(input_directory).resolve()
        relative = [f.relative_to(base).with_suffix("") for f in share_files]

        for file_, api_path in zip(share_files, relative):
            with open(file_, "r") as infile:
                try:
                    json_ = json.load(infile)
                except json.decoder.JSONDecodeError as exc:
                    # TODO: to be logged
                    print(exc)
                    return False
            stringify_text_entries_shallow(json_)
            self.add_api_route(f"/{api_path}",
                               self.create_get_call(json_))
