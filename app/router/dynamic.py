"Dynamic json router"
import json
import pathlib

from fastapi import APIRouter

from app.common.file import get_files_by_type
from app.common.json import stringify_text_entries_shallow
from app.common.utils import logger

from .call import create_get_call, json_exception_call


class DynamicJsonRouter(APIRouter):
    "A GET calls router automatically created based on given input directories with json files."
    def __init__(self, input_directory: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_directory = input_directory
        share_files = get_files_by_type(input_directory, "json")
        base = pathlib.Path(input_directory).resolve()
        relative = [f.relative_to(base).with_suffix("") for f in share_files]

        for file_, api_path in zip(share_files, relative):
            call_name = f"Get {api_path.name}"

            with open(file_, "r", encoding="utf-8") as infile:
                try:
                    json_ = json.load(infile)
                except json.decoder.JSONDecodeError as exc:
                    logger.warning(exc)
                    self.add_api_route(f"/{api_path}",
                                       json_exception_call(
                                                         exc,
                                                         file_name=file_,
                                                         call_name=call_name),
                                       methods=["GET"],
                                       status_code=500)
                    continue

            stringify_text_entries_shallow(json_)
            self.add_api_route(f"/{api_path}",
                               create_get_call(json_, call_name=call_name),
                               methods=["GET"])
