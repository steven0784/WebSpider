#!/usr/bin/env python

import os
import sys

def warc_download(file_name, url, sessions_dir, sitetype):
	'''(str, str, int, str) -> NoneType
	Creates a WARC file from the URL in a zipped file and an HTML for
	for viewing using the OS' wget function.

	The WARC and HTML files are saved into the WARC directory for grabbing.
	Also, it assumes the server is ran from the makefile.
	'''
	dirname = "Session " + str(sessions_dir) + " " + sitetype
	wgetcommand = 'wget "' + url + '" --warc-file="' + file_name + '"'
	os.chdir("../")
	os.chdir("WARC")
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)
		os.system(wgetcommand)
		#Return to the current working directory
		os.chdir("../")
		os.chdir("../")
		os.chdir("WebSpider")
	else:
		os.chdir(dirname)
		os.system(wgetcommand)
		os.chdir("../")
		os.chdir("../")
		os.chdir("WebSpider")