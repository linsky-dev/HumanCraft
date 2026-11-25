"""为证据命令行入口读取无歧义的 JSON。"""

import json
import math


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field")
        result[key] = value
    return result


def _finite_number(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Non-finite JSON number")
    return number


def loads(text):
    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_float=_finite_number,
        parse_constant=_finite_number,
    )
