import yaml
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, dump
from xml.dom import minidom
import xmlschema
schemaXSD = "http://www.mpi.nl/tools/elan/EAFv3.0.xsd"
schema = xmlschema.XMLSchema(schemaXSD)
xmlFilename = "inferno-threeLines.eaf"
print("%s valid xml: %s" % (xmlFilename, schema.is_valid(xmlFilename)))
schema.validate(xmlFilename)

