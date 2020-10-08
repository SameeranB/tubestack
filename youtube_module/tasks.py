from __future__ import absolute_import

import os

from celery import shared_task

from youtube_module.utils import YoutubeClient


@shared_task
def run_keyword_search(keyword):
    """
    This is the task that celery runs periodically. It calls the run_search method we declared in the utils.py
    """
    youtube_client = YoutubeClient(api_token=os.environ.get('YOUTUBE_API_TOKEN'))
    youtube_client.run_search(keyword=keyword)
