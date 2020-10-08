from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from youtube_module.models import Keyword
from youtube_module.tests.test_setup import TestSetup


class TestViews(TestSetup):

    def test_set_keyword(self):
        self.authenticate()
        self.client.post(self.set_keyword_url, self.keyword, format="json")
        return self.assertTrue(Keyword.objects.filter(value=self.keyword.get('value')).exists())

    def test_get_video_data_no_keyword(self):
        self.authenticate()
        res = self.client.get(self.get_video_data_url)
        print(res)
        return self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_get_video_data_success(self):
        self.authenticate()
        self.client.post(self.set_keyword_url, self.keyword, format="json")
        res = self.client.get(self.get_video_data_url)
        return self.assertEqual(res.status_code, HTTP_200_OK)
