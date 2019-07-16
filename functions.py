import urllib.request as req
from bs4 import BeautifulSoup as Soup
from google_images_download import google_images_download
from tokens import *
import re
import random
import json
import os
import tweepy
import datetime


def check_time(hours, minutes=00):
    publish_time = datetime.time(hours, minutes).strftime("%H:%M")
    current_time = datetime.datetime.now().strftime("%H:%M")
    return publish_time == current_time


def parse(url):
    uclient = req.urlopen(url)
    html = uclient.read()
    uclient.close()
    parsed_html = Soup(html, 'html.parser')
    return parsed_html


def parse_main_page(idname):
    page_soup_tfa = parse('https://en.wikipedia.org/wiki/Main_Page')
    div = page_soup_tfa.findAll('div', {'id': idname})
    link = 'https://en.wikipedia.org' + div[0].p.a['href']
    return link


def replace_html(scraped_html, element_name, tag_name=None):
    for char in scraped_html.findAll(element_name, tag_name):
        char.replace_with('')
    return scraped_html


def remove_unwanted_html(scraped_html):
    replace_html(scraped_html, 'sup')  # superscript
    replace_html(scraped_html, 'tr')  # table
    replace_html(scraped_html, 'small')  # smaller text
    replace_html(scraped_html, 'span', {'id': 'coordinates'})  # top coordinates
    replace_html(scraped_html, 'p', {'class': 'mw-empty-elt'})
    return scraped_html


def get_title(html):
    h1 = html.find('h1', {'class': 'firstHeading'})
    title = h1.text
    return title


def get_final_link(title):
    link_of_article = 'https://en.wikipedia.org/wiki/' + title.replace(' ', '_')
    return link_of_article


def fix_lenght(text, desired_lenght):
    fixed_text = ""
    if len(text) > desired_lenght:
        for i in range(desired_lenght):
            fixed_text += text[i]
        fixed_text += '... '
    else:
        fixed_text = text
    return fixed_text


def fix_format(text):
    inside_parentheses = re.sub(r'\([^)]*\)', '', text)
    double_spaces = re.sub(r'\s+', ' ', inside_parentheses)
    formatted_text = re.sub(r'\s+([?;.!,"])', r'\1', double_spaces)  # replaces spaces before punctuation
    return formatted_text


def get_final_tweet(html, link, tfa, otd):
    paragraph = html[0].p.text
    if tfa:
        final_tweet = "Today's Featured Article: " + paragraph + link
    elif otd:
        final_tweet = "On This Day: " + paragraph + link
    else:
        final_tweet = paragraph + link
    final_tweet = fix_format(final_tweet)
    final_tweet = fix_lenght(final_tweet, 260)
    print(final_tweet)
    return final_tweet


def get_image(title):
    image_name = title.replace(', ', ' ')
    response = google_images_download.googleimagesdownload()
    arguments = {'keywords': image_name, 'limit': 1, 'extract_metadata': True,
                 'no_directory': True, 'format': 'jpg', 'size': 'medium', 'print_urls': True}
    paths = response.download(arguments)
    print(paths)


def get_json_directory(title):
    name = title.replace(', ', ' ')
    json_directory = 'logs/' + name + '.json'
    return json_directory


def get_image_directory(jsonfile):
    image_name = []
    image_directory = []
    with open(jsonfile) as f:
        data = json.load(f)
    for d in data:
        image_name.append(d['image_filename'])
    for i in image_name:
        image_directory.append('downloads/' + i)
    return image_directory


def check_image_size(jsonfile, size):
    with open(jsonfile) as f:
        data = json.load(f)
    for d in data:
        height = d['image_height']
        width = d['image_width']
        pixels = width * height
        kb = pixels / 1024
        print("Image weights ", kb, "Kb.")
        return kb < size


def tweet(images, final_tweet):
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_with_media(images[0], final_tweet)
    print("Tweet published.")


def remove_files(jsonfile, images):
    for i in images:
        os.remove(i)
    os.remove(jsonfile)
    print("Files removed.")


def avoid_timeout(time):
    for i in range(1, 5):  # heroku's timeout is 30min and i want to tweet every one hour
        time.sleep(900), print('')  # 900 seconds is 15 min * 4 loops = 1 hour
