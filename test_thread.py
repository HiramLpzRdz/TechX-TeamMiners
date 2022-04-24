import unittest
import thread

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.test_thread = thread.Thread()
        self.valid_image_link = 'https://source.unsplash.com/user/c_v_r/1900x800'
        self.invalid_image_link = 'https://www.reddit.com'
        self.valid_youtube_link = 'https://www.youtube.com/watch?v=WMsOjf_3hnk'
        self.invalid_youtube_link = 'www.youtube.com'
        self.incomplete_youtube_link = 'www.youtube.com/watch?v=WMsOjf_3hnk'


    def test00(self):
        self.assertTrue(self.test_thread.check_img_url(self.valid_image_link))
        self.assertFalse(self.test_thread.check_img_url(self.invalid_image_link))

    def test01(self):
        self.assertTrue(self.test_thread.check_youtube_url(self.valid_youtube_link))
        self.assertFalse(self.test_thread.check_youtube_url(self.invalid_youtube_link))

    def test02(self):
        self.assertTrue(self.test_thread.check_youtube_url(self.incomplete_youtube_link))
