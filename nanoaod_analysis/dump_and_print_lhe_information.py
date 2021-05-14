import graphviz
import pylhe
import itertools
import sys

import subprocess

infilename = sys.argv[1]




tag = infilename.split('.lhe')[0]
if tag.find('/')>=0:
    tag = tag.split('/')[-1]

events = pylhe.readLHE(infilename)

for i, e in enumerate(itertools.islice(events, 0, 2)):
    imagefilename_PDF = f"VISUALIZE_PROCESS_{tag}_event{i}.pdf"
    imagefilename_PNG = f"VISUALIZE_PROCESS_{tag}_event{i}.png"
    pylhe.visualize(e, imagefilename_PDF)
    process = subprocess.run(['convert', imagefilename_PDF,imagefilename_PNG],stdout=subprocess.PIPE,universal_newlines=True)
