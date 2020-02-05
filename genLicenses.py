# Copyright Wicklets LLC 2020, All Rights Reserved
# Edited by: Luca Damasco
#
# genLicenses.py
#
# This file reads a json file of the format
# -PackageName
# | - libraryURL (url)
# | - licenseURL (.txt)
#
# This file can be generated using npm-license-crawler.
#
# It downloads a series of .txt files corresponding to the licenses and creates a licenses.html file which can be used to display licenses within the project.
# Note, this is a helper script. Every file generated and loaded needs to be manually checked for accuracy.

import json 
import requests

fileName = "direct_dependencies.json"
finalFile = "licenseInfo.html";

with open(fileName) as f:
  data = json.load(f)
  
license_header = '''
  <h1> Wick Editor Open Source Notices </h1>
    <p> 
      The Wick Editor is an open source project that utilizes the shared code of dozens of other open source libraries. Below, you can find a list of the projects we use, links to their repositories, and a copy of their license terms. If we have missed a library, or if you have any questions about this list, please send a message to contact@wickeditor.com.
    </p>
'''


default_license = '''

  <p>
    <h3>Library: <a href="<LIB_URL>"><LIB_NAME></a>, License: <LICENSE_TYPE></h3>
    <h4>Used in: <PROJECT_PARENT></h4>
    <br>
      The <LIB_NAME> library is governed by the following license:
    <br>
    <p>
      <FULL_LICENSE>
    </p>
  </p>
'''

with open(finalFile, "w") as outFile:
    outFile.write(license_header)
    
for library in sorted(data.keys()):
  split = library.split('@')
  libName = split[0]
  libUrl = data[library]['repository']

  licenseURL = data[library]['licenseUrl']
  libLicenses = data[library]['licenses']
  libParent = data[library]['parents'].replace('wick-editor-react', 'Wick Editor Interface')

  namedLicense = default_license.replace('<LIB_NAME>', libName)
  urlLicense = namedLicense.replace('<LIB_URL>', libUrl)
  typeLicense = urlLicense.replace('<LICENSE_TYPE>', libLicenses)
  parentLicense = typeLicense.replace('<PROJECT_PARENT>', libParent)

  fullLicense = '';
  print("Adding Library: ", libName)
  try:
    r = requests.get(licenseURL)
    fullLicense = parentLicense.replace('<FULL_LICENSE>', str(r.content))
  except: 
    print("Can't load " + libName)
    
  try:
    with open(finalFile, "a") as outFile:
      outFile.write(fullLicense)
  except:
    print("Can't write: " + libName)
  