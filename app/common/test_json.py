# pylint: disable=C0116,C0116,W1514
"""Tests for json module"""

from app.common import json


class TestStringify:
    "Json operations tests class"
    def test_empty_dict(self):
        in_ = {}
        assert json.stringify_text_entries_shallow(in_) is False

    def test_empty_arr(self):
        in_ = {}
        assert json.stringify_text_entries_shallow(in_) is False

    def test_dictionary(self):
        in_ = {"textualArray": ["foo", "bar"], "dict": {"foo": "bar",
                                                        "text": ["aa\n",
                                                                 "bb"],
               "test": [{"a": "b", "textEntry": ["a", "b", "c"]}]}
               }
        assert json.stringify_text_entries_shallow(in_) is True
        assert in_["dict"]["text"] == "aa\nbb"
        assert in_["textualArray"] == "foobar"
        assert in_["dict"]["test"][0]["textEntry"] == "abc"

    def test_array(self):
        in_ = [{"id_:": "msg1",
                "text": ["multi\n", "line\n", "text"]},
               {"id_:": "2", "teamShareConsentText": ["a", "b"]}]
        assert json.stringify_text_entries_shallow(in_) is True
        assert in_[0]["text"] == "multi\nline\ntext"
        assert in_[1]["teamShareConsentText"] == "ab"
