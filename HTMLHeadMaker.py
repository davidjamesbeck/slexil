'''
******************************************************************
SLEXIL—Software Linking Elan XML to Illuminated Language
Copyright (C) 2019 Paul Shannon and David Beck

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full version of the GNU General Public License is found at
<https://www.gnu.org/licenses/>.

Information about the software can be obtained by contacting
david.beck at ualberta.ca.
******************************************************************
'''

# HTMLHeadMaker.py: a class to build a header for the SLEXIL-generated HTML
# that contains the necessary CSS and javascripts
# -------------------------------------------------------------------------------

import os, sys


def getCSS(stylesheetFile):
    with open(stylesheetFile,"r") as f:
        cssText = f.read()
    fullCssText = "".join(["<style>", cssText, "</style>"])
    return (fullCssText)


def getSlexiljs(javascriptFile):
    with open(javascriptFile,"r") as f:
        slexiljsText = f.read()
    fulljsText = "".join(["<script>", slexiljsText, "</script>"])
    return (fulljsText)


def getJquery(jqueryFile):
    with open(jqueryFile,"r") as f:
        jqueryText = f.read()
    jqueryText = "".join(["<script>", jqueryText, "</script>"])
    return (jqueryText)

