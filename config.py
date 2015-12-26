#!/bin/python
#Author: nandan.adhikari@

import jinja2
import json
import os
import argparse
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/var/log/nginx/nginx-config-gen.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

template_file = "template.j2"
json_parameter_file = "/home/nandan.adhikari/file.json"
output_directory = "/home/nandan.adhikari/includes/"

#Reading the JSON file
try:
	config_parameters = json.load(open(json_parameter_file))
except Exception,e:
	logger.info(e)
	print e
	sys.exit(2)

#Reading Template file
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/home/nandan.adhikari/"),
                         trim_blocks=True,
                         lstrip_blocks=True)
try:
	template = env.get_template(template_file)
except Exception,e:
	logger.info(e)
	print e
	sys.exit(2)

#Check for Nginx include directory
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

for team in config_parameters:
	result = template.render(key=team,bucket=config_parameters[team])
	fname = output_directory + config_parameters[team]  + "_nginx.conf"
	if os.path.isfile(fname):
	  print "Error: config file exists -", fname
	  logger.info('Error: File exists - %s' %fname)
	  sys.exit(2)
	else:
	  f = open(fname, "w")
	  f.write(result)
	  f.close()
	  print "Configs created -", fname
	  logger.info('Configuration file %s created.' %fname)

