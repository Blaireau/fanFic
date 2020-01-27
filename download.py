# -*- coding: utf-8 -*-
# TODO : General logging
# TODO : For the moment we are working directly in RAM. See if we don't consume too much resources.
import requests
from bs4 import BeautifulSoup
import re

# Parameters
# Parameters for the URL base
base_url = "https://www.fanfiction.net/s/"
# TODO : Make it "cli" friendly !
id_fanfic = "6910226"
# We build the full url, since we are going to need it !
full__fanfic_url = base_url + id_fanfic
# Regex in order to catch chapters name (awful hack done quick...) and cleaning some outputs
chap_regex = re.compile('value="')
optionoutput_regex = re.compile('</option>')
# Dictionnary for the chapters
chap_dict = {}

# Doing the request ! TODO : Error catching
requested_page = requests.get(full__fanfic_url)
parsed_page = BeautifulSoup(requested_page.text, features="html.parser")

# Now we build the chapters list
# Getting the chapters list
chapters = parsed_page.find('select').find('option')
temporary_chap_list = str(chapters).split('<option')
# Parsing the chapters list to build the dict we are going to use when building the pdf
# TODO : Logging here ?
for num_chap in temporary_chap_list:
    pos = chap_regex.search(num_chap)
    # If we have a "value" tag, it's a part of the select drop-down menu, so it's a chapter.
    if pos:
        tmp_lst = num_chap.split('">')
        # Small cleaning, because the website adds a lot of awful html at the end of the "option" block...
        tmp_lst[1] = re.sub(optionoutput_regex, '', tmp_lst[1])
        chap_dict[tmp_lst[0][pos.end():]] = tmp_lst[1]

# Now we have a nice dict, with the chapter number and his name.
# We have to call each page in order to get the text, then we can build the output pdf.
