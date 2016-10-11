#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Copyright (c) 2016, Dheepak Krishnamurthy
All rights reserved.

License : BSD 3-Clause
"""


from __future__ import print_function

# import sys
from copy import deepcopy
from pandocfilters import walk, toJSONFilter

span_count = 0
tag_count = 0
element_type = 'aside'


def custom_notes(key, value, fmt, meta):

    # sys.stderr.write('\n\n' + str(key) + '\t' + str(value) + '\n\n')

    store = dict()

    global span_count

    def convert_note_to_element_type(store):
        global tag_count
        global element_type
        value = deepcopy(store['store'])

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
        if value[0]['c'][0]['t'] == 'Strong':
            span_count = span_count + 1
            return {"c": [
                ["{}-{}".format(element_type, span_count - 1), [], []], []], "t": "Span"
            }
        else:
            pass

    if key == 'Para':
        walk(value, action, fmt, meta)
        # sys.stderr.write('Walking down Para\n')
        if store:
            # sys.stderr.write('Found a Note in Para\n')
            v = convert_note_to_element_type(store)
            # sys.stderr.write('Converted the Note\n')
            # sys.stderr.write(repr(store['store']) + '\n')
            # sys.stderr.write(repr(v) + '\n')
            if v is not None:
                v.insert(0, {'t': 'Para',
                    'c': value})
                return v

if __name__ == "__main__":
    toJSONFilter(custom_notes)
