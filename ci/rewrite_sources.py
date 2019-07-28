#!/bin/python
"""
Rewrite the source code path in coverage.xml to a new value for use by CI.

In the container it's always: <sources><source>/code</source></sources>

However, the coverage tool for Azure Pipelines needs the path to match
the directory outside of the container.
"""

import sys
import xml.etree.ElementTree as ET


def main(path, new_sources):
    tree = ET.parse(path)
    for elem in tree.findall("sources/source"):
        elem.text = new_sources
    tree.write(path)


if __name__ == "__main__":
    main(*sys.argv[1:])
