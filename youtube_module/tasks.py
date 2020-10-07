from __future__ import absolute_import

import os

from celery import shared_task

from youtube_module.utils import YoutubeClient


@shared_task
def run_keyword_search(keyword):
    youtube_client = YoutubeClient(api_token=os.environ.get('YOUTUBE_API_TOKEN'))
    youtube_client.run_search(keyword=keyword)
