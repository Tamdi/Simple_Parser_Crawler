from datetime import datetime

from dateparser import parse
from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse


def parse_short_obj(params):
    response = requests.get(
        "https://www.zakon.kz/",
        timeout=10,
    )
    if response.ok:
        response_content = response.content
        soup = BeautifulSoup(response_content, 'html.parser')
        div = soup.find("div", {"class": "lastnews"})
        data = []
        for _a in div.find_all('a'):
            time = _a.text.strip()[0:5]
            title = _a.text.replace(time, '').strip()
            data.append(
                {
                    "time": time,
                    "title": title,
                }
            )
        # print(data)
        if params:
            return data[0:int(params['count'])]
        return data


def parse_full_obj(params):
    response = requests.get(
        "https://www.zakon.kz/",
        timeout=10,
    )
    if response.ok:
        response_content = response.content
        soup = BeautifulSoup(response_content, 'html.parser')
        div = soup.find("div", {"class": "lastnews"})
        data = []
        for _i, _a in enumerate(div.find_all('a')):
            if params:
                if str(_i) == params:
                    break
            url = _a.get('href')
            if (url[0] == "/") and (url[1] != "/"):
                url = "".join(("https://www.zakon.kz", url))
            response_new = requests.get(
                url=url,
                timeout=10,
            )
            response_content_new = response_new.content
            soup_new = BeautifulSoup(response_content_new, 'html.parser')

            # image_url
            div_img = soup_new.find("div", {"class": "newspic"})
            if not div_img:
                continue
            image_link = div_img.findAll('img')[0]['src']
            # for _i in div_img.findAll('img'):
            #     image = _i['src']
            #     continue
            if '//' in image_link:
                image_link = "".join(("https:", image_link))
            # if (image[0] == "/") and (image[1] == "/"):
            #     image_link = "".join(("https:", image))

            # title
            div_head = soup_new.find("div", {"class": "fullhead"})
            head = div_head.findAll('h1')[0].text.strip()

            # text
            full_text = soup_new.find("div", {"class": "newscont"}).text.strip()
            # full_text = ""
            # for _i in div_text.findAll('p'):
            #     text = _i.text.strip()
            #     full_text = full_text + " " + text
            # print(full_text)

            # date
            div_date = soup_new.find("div", {"class": "extrainfo"})
            date = div_date.span
            date_field=str(date)
            date_text = date_field.replace("<span>", '').replace("</span>", '').replace("октября", 'October')
            # print(meme)
            dt = parse(date_text)
            new_date = datetime.strftime(dt, '%d %m %Y, %H:%M')
            # print(new_date)

            data.append(
                {
                    "url": url,
                    "title": head,
                    "text": full_text,
                    "img_url": image_link,
                    "date": new_date,
                }
            )
        return data


# ______________________________________________________
# def parse_full_obj(params, type):
#     response = requests.get(
#         "https://www.zakon.kz/",
#         timeout=10,
#     )
#     if response.ok:
#         response_content = response.content
#         soup = BeautifulSoup(response_content, 'html.parser')
#         div = soup.find("div", {"class": "lastnews"})
#         data = []
#         for _a in div.find_all('a'):
#             url = _a.get('href')
#             # contents = link.text
#             if (url[0] == "/") and (url[1] != "/"):
#                 good_url = "".join(("https://www.zakon.kz", url))
#             time = _a.text.strip()[0:5]
#             title = _a.text.replace(time, '').strip()
#             data.append(
#                 {
#                     "time": time,
#                     "title": title,
#                     "url": good_url,
#                 }
#             )
#         # print(data)
#         if params:
#             return data[0:int(params['count'])]
#         return data
