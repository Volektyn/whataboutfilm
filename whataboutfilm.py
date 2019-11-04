from bs4 import BeautifulSoup as bs

from flask import Flask, send_file

from urllib.request import urlopen, urlretrieve, HTTPError
from re import compile, match


import random


app = Flask(__name__)
target = "http://kinozal.tv/top.php"


"""
    Function that retrieve poster image of random film from http://kinozal.tv/top.php
"""


def get_poster(target_site):
    with urlopen(target_site) as html:
        bs_obj = bs(html.read(), features="html.parser")
        # from string below we can get direct links to some host with image or relative link to target_site
        img_list = [img.get("src") for img in bs_obj.find("div", {"class": "bx1 stable"}).findAll("img") if img.get("src")]
        chosen_img = random.choice(img_list)
        posters = compile("^/i/poster/[0-9]/[0-9]/[0-9]+(.jpg)") # if chosen_img is relative link
        if match(posters, chosen_img):
            chosen_img = target_site + chosen_img
        try:
            urlretrieve(chosen_img, r"/tmp/film_getter/poster.jpg")
        except HTTPError:
            get_poster(target_site) # if file cannot be retrieved try to retrieve another one


@app.route('/')
def index():
    try:
        get_poster(target)
        return send_file("/tmp/film_getter/poster.jpg", mimetype='image/jpg')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)

# def main():
#     try:
#         if sys.argv.__len__() > 1:
#             download_path = sys.argv[0]
#             get_poster(target)
#             send_poster()
#             return __doc__
#         else:
#             raise AttributeError("Need download path")
#     except AttributeError as ae:
#         return ae


# def print_log(chosen_image):
#     pass


# if __name__ == "__main__":
#     main()




