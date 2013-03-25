#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import chess
import optparse
import textwrap
import os

if __name__ == "__main__":
    # Parse command line arguments.
    parser = optparse.OptionParser("usage: %prog [OUTPUT OPTIONS] [INPUT FILE]")
    description = """\
                  This script converts ECO opening databases into JSON files.

                  You can create a classification table showing ECO codes keyed
                  by position.
                  You can also create a lookup table showing position and name
                  keyed by eco code.
                  """
    parser = optparse.OptionParser(usage, description=textwrap.dedent(description))
    parser.add_option("-q", "--quiet", action="store_true", default=False,
        help="quiet output")
    parser.add_option("-c", "--classification", dest="classification", default=os.devnull,
        help="the output file for the classification table")
    parser.add_option("-l", "--lookup", dest="lookup", default=os.devnull,
        help="the output file for the lookup table")

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.error("no input file given")

    # Read the input files.
    eco_parser = chess.EcoFileParser()
    for arg in args:
        eco_parser.tokenize(arg)
        while eco_parser.has_more():
            eco_parser.read_chunk()
            if eco_parser.current_state == chess.EcoFileParser.ECO_STATE and not options.quiet:
                print eco_parser.current_eco, eco_parser.current_name

    # Write output.
    json.dump(eco_parser.lookup, open(options.lookup, "w"))
    json.dump(eco_parser.classification, open(options.classification, "w"))
