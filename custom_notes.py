#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Copyright (c) 2016, Dheepak Krishnamurthy
All rights reserved.

License : BSD 3-Clause
"""


from __future__ import print_function

from pandocfilters import walk, toJSONFilter

span_count = 0
tag_count = 0
element_type = 'aside'


def custom_notes(key, value, fmt, meta):

    store = dict()

    global span_count

    def convert_note_to_element_type(store):
        global tag_count
        global element_type
        value = store['store']

        if value[0]['c'][0]['t'] == u'Strong':
            raw = value[0]['c'].pop(0)
            element_type = raw['c'][0]['c']

            if value[0]['c'][0]['t'] == u'Space':
                value[0]['c'].pop(0)

            if value[0]['c'][0]['c'] == u':':
                value[0]['c'].pop(0)

            if value[0]['c'][0]['t'] == u'Space':
                value[0]['c'].pop(0)

            value.insert(0, {
                "t": "RawBlock",
                "c": ['html', "<{} id=\"{}-{}\">".format(element_type, element_type, tag_count)]
            })
            tag_count = tag_count + 1
            value.append({
                "t": "RawBlock",
                "c": ['html', "</{}>".format(element_type)]
            })

            return value

    def action(key, value, format, meta):
        if key == 'Note':
            store['store'] = value

    if key == 'Note':
        span_count = span_count + 1
        return {"c": [
            ["{}-{}".format(element_type, span_count - 1), [], []], []], "t": "Span"
        }

    if key == 'Para':
        walk(value, action, fmt, meta)
        if store:
            v = convert_note_to_element_type(store)
            if v is not None:
                v.insert(0, {'t': 'Para',
                    'c': value})
                return v

if __name__ == "__main__":
    toJSONFilter(custom_notes)
