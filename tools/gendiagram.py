#!/usr/bin/env python

import argparse
import os
import re
import sys
import string
import traceback
import urllib


ALL_STYLES = [
    'default', 'earth', 'qsd',                # traditional
    'rose', 'napkin', 'mscgen',               # traditional
    'modern-blue', 'omegapple', 'roundgreen', # colourful
]

WEBSITE="http://www.websequencediagrams.com/"


def gen_sequence_diagram(source, target=None, style='default'):

    # read source content
    with open(source, 'r') as f:
        text = f.read()
    if not text:
        print "%s is empty, exit..." % source
        sys.exit(0)

    # make request
    request = {}
    request["apiVersion"] = "1"
    request["message"] = text
    request["style"] = style

    url = urllib.urlencode(request)

    resp = urllib.urlopen(WEBSITE, url)
    line = resp.readline()
    resp.close()

    expr = re.compile("(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
    match = expr.search(line)

    if match == None:
        raise Exception("Invalid response from server.")

    image_url = match.group(0)

    if not target:
        suffix = string.split(image_url, '=')[0][1:]
        dirname = os.path.dirname(source)
        basename = os.path.basename(source)
        filename = string.rstrip(basename, '.wsd')
        output = string.join([filename , suffix], sep='.')
        target = os.path.join(dirname, output)

    urllib.urlretrieve(WEBSITE + image_url, target)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', metavar='input file',
                        required=True, help='Input file name')
    parser.add_argument('-o', '--output', metavar='output file',
                        default=None, help='Output file name')
    parser.add_argument('-s', '--style', metavar='output style',
                        default='modern-blue',
                        help='Output image style, all style: %s' % ALL_STYLES)

    args = parser.parse_args()

    source = args.input
    target = args.output
    style = args.style

    if not os.path.exists(source):
        print "%s do not exists" % source
        sys.exit(-1)

    if style not in ALL_STYLES:
        print  "%s style do not supported" % style
        sys.exit(-2)

    try:
        gen_sequence_diagram(source, target, style=style)
    except Exception as e:
        print traceback.print_exc()
        sys.exit(-3)
