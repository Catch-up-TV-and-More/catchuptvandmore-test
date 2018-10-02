#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re

strings_po = sys.argv[1]

if os.path.exists(strings_po):  # pragma: no branch
    with open(strings_po, "rb") as fo:
        raw_strings = fo.read()

    # Parse strings using Regular Expressions
    res = u"^msgctxt\s+[\"']#(\d+?)[\"']$[\n\r]^msgid\s+[\"'](.+?)[\"']$"
    data = re.findall(res, raw_strings.decode("utf8"), re.MULTILINE | re.UNICODE)

    dict_str = 'FAKE_LABELS = {\n'

    for value, key in data:
        dict_str += '\t'
        dict_str += str(value)
        dict_str += ": '"
        dict_str += key.encode('utf-8')
        dict_str += "',\n"
    dict_str += "}"

    print dict_str
