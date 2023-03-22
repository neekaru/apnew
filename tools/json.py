# this for handling nasty json overall this quite good code from my old code

import json
import re
from datetime import datetime, date
from decimal import Decimal
from tools.url import Url


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode("utf-8", "ignore")
        elif isinstance(obj, str):
            # Remove non-valid symbols
            obj = re.sub(r"[^\x00-\x7F]+", "", obj)
            # Escape special characters
            obj = obj.encode("unicode_escape").decode("utf-8")
            return obj
        elif obj is None:
            return ""
        else:
            return super().default(obj)

    def encode(self, obj):
        # Remove occurrences of multiple spaces
        result = super().encode(obj).replace("   ", " ").replace("  ", " ")
        # Remove occurrences of "undefined"
        result = re.sub(r'"undefined"', '""', result)

        # Fix multiple JSON elements and string wrapping
        result = result.strip().strip('"')
        if result.startswith("[") and result.endswith("]"):
            return result
        elif result.startswith("{") and result.endswith("}"):
            return result
        else:
            try:
                # Try to parse as number
                float(result)
                return result
            except ValueError:
                pass

            # Escape special characters
            result = result.encode("unicode_escape").decode("utf-8")

            # Add quotes around the string
            result = f'"{result}"'

            # Fix the "Expecting comma or }" error
            result = re.sub(
                r'"([^"]+)":\s*"({[^}]+})"+([^"])"', r'"\1": \2,\3', result)

            return result


def decode_unicode(data):
    if isinstance(data, str):
        return re.sub(r'u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), data)
    elif isinstance(data, dict):
        return {decode_unicode(key): decode_unicode(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_unicode(item) for item in data]
    else:
        return data


def json_dumps_fix(d: None, double_slash: bool = False, hard_fix: bool = False):
    ls = json.dumps(d, cls=CustomEncoder)
    if double_slash is True:
        dl = ls.replace("\\", "")

    if hard_fix is True:
        dl = Url(d).fix_annoy(double_newline=True)
        dl = dl.replace("   ", "").replace("       ", "").replace(
            "       ", "").replace("undefined", '""')
    return dl
