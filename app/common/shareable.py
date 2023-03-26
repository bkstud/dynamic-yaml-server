from .file import prepare_source_structure_and_call_by_ext
from .json import process_json
from pathlib import Path


def prepare_json_contents(source: str, destination: str):
    def json_create(src_, dst_):
        process_json(src_, Path(dst_).with_suffix(""))

    prepare_source_structure_and_call_by_ext(
        source_dir=source,
        out_dir=destination,
        ext="json",
        callable=json_create
    )
