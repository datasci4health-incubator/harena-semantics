import os, sys
import xml.etree.ElementTree as et

file = os.open('../../documents/pmc/pmc-text-01/09/2771650.nxml', os.O_RDONLY)
print(file)

for x in range(6):
    try:
        tree = et.parse('../../documents/pmc/pmc-text-01/09/2771650.nxml')
        print(tree)
    except et.ParseError:
        print('error')