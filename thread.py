from datetime import datetime
from urllib.request import urlopen
import requests

class Thread:
    def __init__(self):
        pass

    def check_new_thread(self, title, text, tags,author,
                         video_link, image_link):
        thread_info = {}
        if tags != '':
            thread_info['tags'] = tags
        if video_link != '' and self.check_youtube_url(video_link):
            video_link = video_link.replace('watch?v=', 'embed/')
            thread_info['video_link'] = video_link
        if tags != '':
            thread_info['tags'] = tags
        if image_link != '' and self.check_img_url(image_link):
            thread_info['image_link'] = image_link
        thread_info['title'] = title
        thread_info['text'] = text
        thread_info['author'] = author
        thread_info['date_time'] = datetime.now().strftime("%m/%d/%Y")
        return thread_info

    def create_comment(self, author, text, thread_id, image_link):
        comment_info = {'text': text,
                        'author': author,
                        'date_time': datetime.now().strftime("%m/%d/%Y"),
                        'thread_id': thread_id}
        if self.check_img_url(image_link):
            comment_info['image_link'] = image_link

    def check_img_url(self, url):
        image_formats = ("image/png", "image/jpeg", "image/gif")
        site = urlopen(url)
        meta = site.info()  # get header of the http request
        return meta["content-type"] in image_formats

    def check_youtube_url(self, url):
        if 'youtube.com/watch' not in url:
            return False
        if len(url) < 32:
            return False
        if url[:8] != 'https://':
            url = "https://" + url
        r = requests.get(url)
        return not "Video unavailable" in r.text
