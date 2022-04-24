from datetime import datetime
from urllib.request import urlopen
import requests

class Thread:
    """
       A class to verify thread information before creating a new thread
       Attributes
       ----------
       None

       Methods
       -------
       check_new_thread(title, text, tags,author, video_link, image_link)
       receives new thread info gathered from /new_thread
       if there is a video link or image link included, it makes sure
       that link is valid before adding it to the database. Also,
       transforms youtube link to work in html.
       create_comment(author, text, thread_id, image_link)
       receives comment info from /thread and verifies image link before
       adding it to the comment info and storing it in a dictionary
       check_img_url(url):
       receives a url for an image link and verifies the link.
       Returns True if the link is valid
       check_youtube_url(self, url):
       receives a url for a youtube video and verifies the link.
       Returns True if the link is valid
       """
    def __init__(self):
        pass

    def check_new_thread(self, title, text, tags,author,
                         video_link, image_link):
        '''
        creates dictionary with thread info to be sent to MONGODB
        :param title: str - title of thread
        :param text: str - content of the thread
        :param tags: str - tags for thread
        :param author: str - username of person creating thread
        :param video_link - url for youtube link
        :param image_link - url for image link
        :return thread_info - dictionary
        '''
        thread_info = {}
        if tags != '':
            thread_info['tags'] = tags
        if self.check_youtube_url(video_link):
            video_link = video_link.replace('watch?v=', 'embed/')
            thread_info['video_link'] = video_link
        if tags != '':
            thread_info['tags'] = tags
        if self.check_img_url(image_link):
            thread_info['image_link'] = image_link
        thread_info['title'] = title
        thread_info['text'] = text
        thread_info['author'] = author
        thread_info['date_time'] = datetime.now().strftime("%m/%d/%Y")
        return thread_info

    def create_comment(self, author, text, thread_id, image_link):
        '''
        creates dictionary with comment info to be sent to MONGODB
        :param text: str - text of comment
        :param author: str - username of person making comment
        :param thread_id str - MongoDB ID of thread comment is being made on
        :param image_link - url for image link
        :return comment_info - dictionary
        '''
        comment_info = {'text': text,
                        'author': author,
                        'date_time': datetime.now().strftime("%m/%d/%Y"),
                        'thread_id': thread_id}
        if self.check_img_url(image_link):
            comment_info['image_link'] = image_link
        return comment_info

    def check_img_url(self, url):
        '''
        verifies that image url is valid
        :param url: str - image url
        :return: True if url is valid, False otherwise
        '''
        if url == '':
            return False
        image_formats = ("image/png", "image/jpeg", "image/gif")
        site = urlopen(url)
        meta = site.info()  # get header of the http request
        return meta["content-type"] in image_formats

    def check_youtube_url(self, url):
        '''
        verifies that youtube url is valid
        :param url: str - image url
        :return: True if url is valid, False otherwise
        '''
        if 'youtube.com/watch' not in url:
            return False
        if len(url) < 32:
            return False
        if url[:8] != 'https://':
            url = "https://" + url
        r = requests.get(url)
        return not "Video unavailable" in r.text
