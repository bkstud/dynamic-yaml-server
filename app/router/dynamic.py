from fastapi import APIRouter
import json
import pathlib
from app.common.json import stringify_text_entries_shallow
from app.common.file import get_files_by_type
from app.common.utils import logger


class DynamicJsonRouter(APIRouter):

    @staticmethod
    def create_get_call(in_dict: dict) -> dict:
        # TODO: Add search parameters GET /emails&name=jakisname ,
        # /emails&wrongname=name -> should give information that there is not such

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
                    # TODO: Make this exception more verbose
                    # but service should start even if there is broken json
                    # TODO: Create special endpoint handling this situastopm
                    # 50.. something code + json data telling what happened
                    # wrong 
                    # {detail: "info about error from json file"}
                    logger.error(exc)
            stringify_text_entries_shallow(json_)
            self.add_api_route(f"/{api_path}",
                               self.create_get_call(json_))
