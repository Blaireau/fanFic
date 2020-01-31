# -*- coding: utf-8 -*-
# TODO : General logging
# TODO : For the moment we are working directly in RAM. See if we don't consume too much resources.
import requests
import re
from fpdf import FPDF, HTMLMixin
from bs4 import BeautifulSoup
from time import sleep

# Parameters
# Parameters for the URL base
base_url = "https://www.fanfiction.net/s/"
# TODO : Make it "cli" friendly !
# id_fanfic = "6910226" # --> HP et les méthodes de la rationnalité pas utilisé pour tests.
id_fanfic = "13096584"  # --> Random fanfic pour test (15 chapitres, 103529 mots, autour de Killer Instinct)
# We build the full url, since we are going to need it !
full_fanfic_url = base_url + id_fanfic
# Regex in order to catch chapters name (awful hack done quick...) and cleaning some outputs
chap_regex = re.compile('value="')
optionoutput_regex = re.compile('</option>')
# Dictionnary for the chapters
chap_dict = {}
# List of list for all the chapters (if multiple chapters)
all_chapters = []
# We don't want to stress the website. Let's sleep a little.
time_sleep = 1


class MyFPDF(FPDF, HTMLMixin):
    pass


# Doing the request ! TODO : Error catching
print("Getting the page at : " + full_fanfic_url)
requested_page = requests.get(full_fanfic_url)
parsed_page = BeautifulSoup(requested_page.text, features="html.parser")
print("Page got and parsed by BS")

# Now we build the chapters list
# Getting the chapters list in a format we can manipulate further
print("Building chapter list")
chapters = str(parsed_page.find('select').find('option')).split('<option')

# Parsing the chapters list to build the dict we are going to use when building the pdf
# TODO : Logging here ?
for num_chap in chapters:
    pos = chap_regex.search(num_chap)
    # If we have a "value" tag, it's a part of the select drop-down menu, so it's a chapter.
    if pos:
        tmp_lst = num_chap.split('">')
        # Small cleaning, because the website adds a lot of awful html at the end of the "option" block...
        tmp_lst[1] = re.sub(optionoutput_regex, '', tmp_lst[1])
        chap_dict[tmp_lst[0][pos.end():]] = tmp_lst[1]

# Now we have a nice dict, with the chapter number and his name.
# We have to call each page in order to get the text, then we can build the output pdf.
# TODO : Maybe output in another format ? LaTex ? etc...
# TODO : Check if the fanfic has only one chapter...

print("Got " + str(len(chap_dict)) + " chapters. Let's download that !")
max_chapter = len(chap_dict)
for key in chap_dict:
    print("Getting chapter " + str(len(chap_dict) - max_chapter + 1) + " on " + str(len(chap_dict)))
    chapter_url = full_fanfic_url + '/' + key
    requested_page = requests.get(chapter_url)
    parsed_page = BeautifulSoup(requested_page.text, features="html.parser")
    # This line gets all the storytext, and convert it in a list. We will use this to build a "list of list" with all
    # the fanfic text. And then we will build our out PDF.
    all_chapters.append((chap_dict[key], parsed_page.find("div", {"id": "storytext"}).contents))
    print("Got chapter ! Going to sleep a little. No stress !")
    # In order to be a little bit polite, we sleep a little. We don't "gotta go fast"...
    sleep(time_sleep)
    max_chapter -= 1

print("All chapters of fanfic retrieved ! Let's convert that in PDF !")

print(type(all_chapters[0][1]))
print(len(all_chapters[0][1]))

print(all_chapters[0][1][1])
print(type(all_chapters[0][1][1]))
print(all_chapters[0][1][2])
print(type(all_chapters[0][1][2]))

temp_file = open("temp.txt", "w", encoding='utf-8')

for i in range(len(all_chapters)):
    temp_file.write('Title : ' + str(all_chapters[i][0]) + '\nContent : \n' + str(all_chapters[i][1]))
    temp_file.write('\n\n')

temp_file.close()

# print(all_chapters)
# print(chap_dict)

my_pdf = MyFPDF()
my_pdf.add_page()
# TODO : Maybe some parametrization for the font ?
# my_pdf.set_font("Arial", size=14)
# my_pdf.cell(200,10,txt="Welcome to Python !",ln=1,align="C")
print(all_chapters[0][1][0])
html_temp = str(all_chapters[0][1][0]).replace("<strong>", "<B>").replace("</strong>", "</B>")
print(html_temp)
my_pdf.write_html(html_temp)

print(all_chapters[0][1][2])
html_temp = str(all_chapters[0][1][2]).replace("<strong>", "<B>").replace("</strong>", "</B>")
print(html_temp)
my_pdf.write_html(html_temp)

print(all_chapters[0][1][3])
html_temp = str(all_chapters[0][1][3]).replace("<strong>", "<B>").replace("</strong>", "</B>")
print(html_temp)
my_pdf.write_html(html_temp)

print(all_chapters[0][1][8])
html_temp = str(all_chapters[0][1][8]).replace("<strong>", "<B>").replace("</strong>", "</B>").replace("<em>", "<i>").replace("</em>", "</i>")
print(html_temp)
my_pdf.write_html(html_temp)

my_pdf.output("testdemo.pdf", "F")
