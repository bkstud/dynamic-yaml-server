from fastapi import APIRouter, Depends
from typing import Union, Optional, Callable
from pydantic import create_model
import json
import pathlib
from app.common.json import stringify_text_entries_shallow
from app.common.file import get_files_by_type
from app.common.utils import logger


class DynamicJsonRouter(APIRouter):

    @staticmethod
    def create_get_call(in_: Union[dict, list],
                        name: Optional[str] = None) -> Callable:
        """Generator of GET handle functions returning dictionary data

        Args:
            in_: dictionary or list containing json data to return by call
        Returns:
            callable: fastapi compatible
            name: name of the handle method to give to callable
                  and dynamically  created query model
        """

        # return in case in_ is not indexble array
        async def non_queryable_api_data():
            "In case in_ is non indexable."
            return in_

        in_dict_schema = None
        out_fn = None

        if type(in_) is dict:
            # TODO: To be considered if in case of just dictionary
            # we want to have fixed model for example key='somekey'
            # that would make call return just single dictionary
            # key
            out_fn = non_queryable_api_data
        elif type(in_) is list and type(in_[0]) is dict:
            # TODO: Probably this is too simplified and we should
            # check if each dictionary has the same keys or create set
            # containing keys from all data.
            # The edge case: input list [{}, {"foo": "bar", "name": "some"},
            #  {...}]
            in_dict_schema = in_[0]
        else:
            out_fn = non_queryable_api_data

        if in_dict_schema:
            query_params = {str(k): (Optional[type(v)], None)
                            for k, v in in_dict_schema.items()}

            query_model = create_model("Query", **query_params)

            # return in case in_ a is list of dictonaries with some keys
            async def querable_api_data(params: query_model = Depends()):
                """In case in_ is list of dictionaries"""
                set_params = params.dict(exclude_none=True)
                # TODO: Consider if deep properties should be accessable using
                return [el for el in in_
                        if all([el.get(k) == v
                               for k, v in set_params.items()])
                        ]

            out_fn = querable_api_data

        if name:
            out_fn.__name__ = name

        return out_fn

    @staticmethod
    def handle_json_exception():
        ""
        raise NotImplementedError()

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
            call_name = f"Get {api_path.name}"
            self.add_api_route(f"/{api_path}",
                               self.create_get_call(json_, name=call_name),
                               methods=["GET"])
