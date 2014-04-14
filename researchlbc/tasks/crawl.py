# -*- coding: utf-8 -*-

"""Definition of the crawling related tasks."""

from __future__ import absolute_import

import requests

from bs4 import BeautifulSoup
from researchlbc.tasks.celery import celery
from researchlbc.models.lbc import Ad


def get_next_page_link(soup):
    """Return the URL of the next page."""
    ul = soup.find('ul', id_='paging')
    current_page_li = ul.find('li', class_='selectd')
    next_page_li = current_page_li.find_next_sibling()
    return next_page_li.get('href')


def scrape_ads(soup):
    """Return the ads from the page soup, as bs4.element.Tag objects."""
    container = soup.find('div', class_='list-lbc')
    scraped_tags = container.find_all_next('a', title=True)
    ads = [Ad(scraped_tag).to_dict() for scraped_tag in scraped_tags]
    return ads


@celery.task()
def get_links(url):
    """Scrape the ads from a webpage of argument URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    ads = scrape_ads(soup)
    return ads
