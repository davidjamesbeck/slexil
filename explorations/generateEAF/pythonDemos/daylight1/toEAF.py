import yaml
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, dump
from xml.dom import minidom
import datetime
import xml.etree as etree

x = yaml.load(open("daylight1.yaml"))
# print(yaml.dump(x))

generated_on = str(datetime.datetime.now())

# Configure one attribute with set()
root = Element('ANNOTATION_DOCUMENT')
root.set('VERSION', '2.8')
root.set('FORMAT', '2.8')
root.set('AUTHOR', x['author'])
root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
root.set('xsi:noNamespaceSchemaLocation',"http://www.mpi.nl/tools/elan/EAFv2.8.xsd")

header = SubElement(root, 'HEADER')
header.set("MEDIA_FILE", "")
header.set("TIME_UNITS", "milliseconds")

mediaDescriptor = SubElement(header, 'MEDIA_DESCRIPTOR')
mediaDescriptor.set('MEDIA_URL', "file:///Users/paul/github/howDaylightWasStolen-harryMoses/peelingOffSomeDaylight/daylight77a.wav")
mediaDescriptor.set('MIME_TYPE', "audio/x-wav")
mediaDescriptor.set('RELATIVE_MEDIA_URL', "file://./daylight_1_4.wav")
property = SubElement(header, "PROPERTY")
property.set('NAME', "lastUsedAnnotationId")
property.text = '340'

timeOrder = SubSelement(root, "TIME_ORDER")


xmlstr = minidom.parseString(etree.ElementTree.tostring(root)).toprettyxml(indent = "   ")
print(xmlstr)

#root.append(Comment('Generated by ElementTree_csv_to_xml.py for PyMOTW'))

