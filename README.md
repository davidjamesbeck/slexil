# slexil
Software  Linking Elan Xml to Illuminated Language

This software is a webapp designed to convert ELAN time-aligned transcription files to animated HTML that allows for continuous highlighted or line by line playback of texts. Texts can be prepared in 2 line (text-translation) or 4 line (text, interlinearization, translation) format, and supports the addition of an additional transcription line and a translation into a second language. The software runs on a remote server and is accessed by users via a web-browser and ordinary internet connection. An instance of SLEXIl is currently running at slexil.artsrn.ualberta.ca

Running SLEXIL offline

SLEXIL is designed to be run as a webapp but can also be downloaded and run on a user's personal computer, provided the following resources are available:

•	Python (3.6 or higher)
•	gunicorn
•	xmlschema
•	soundfile
•	dash 1.01
•	dash_table 4.0.1
•	dash_core_components 1.0.0
•	dash_html_components 1.0.0
•	dash-dangerously-set-inner-html 0.0.2
•	pandas
•	pyyaml
•	yattag
•	bs4

The Python packages are listed in the file requirement.tx and can be batch installed using pip (“pip install -r requirements.txt”).

In order to be run on an user's computer, the main Python file, webapp4.py, must be edited. Specifically, the lines at the end of the file (currently lines 932–941) need to be altered so that the correct __main__ method is run. This is dont by commenting out the lines following "enable these lines if running with gunicorn" and uncommenting the lines following "enable these lines for running from bash and python" so that the code looks like this:

\# enable these lines for running from bash and python
if __name__ == "__main__":
        app.run_server(host='0.0.0.0', port=60041)

\# enable these lines if running with gunicorn
\# if __name__ == "__main__":
\#     server = app.server
\#     app.run()

