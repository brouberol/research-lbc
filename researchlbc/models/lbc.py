# -*- coding: utf-8 -*-

"""Definition of models related to the leboncoin.fr website"""

import re
import datetime


abbr_months = {
    'jan': 1,
    'fév': 2,
    'mar': 3,
    'avr': 4,
    'mai': 5,
    'juin': 6,
    'jui': 7,
    'aôut': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'déc': 12
}

date_pattern = r'(?P<day>\d{2}) (?P<month>\w+)$'
hour_pattern = r'(?P<hour>\d{2}):(?P<minute>\d{2})$'


class Ad(object):

    """Wrapper around a bs4.element.Tag object, providing helper
    properties and methods.

    """

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.title)

    @property
    def title(self):
        """The ad title."""
        return self.tag.find_next('div', class_='title').text.strip()

    @property
    def url(self):
        """The ad link bs4 Tag."""
        return self.tag.attrs['href']

    @property
    def price_text(self):
        """The ad price text."""
        return self.tag.find_next('div', class_='price').text.strip()

    @property
    def price(self):
        return int(
            re.search(r'[\d\s]+', self.price_text).group().replace(' ', ''))

    @property
    def location(self):
        """The ad location."""
        location = self.tag.find_next('div', class_='placement').text.strip()
        return re.sub(r'\s{2,}', '', location)

    @property
    def city(self):
        return self.location.split('/')[0]

    @property
    def pro(self):
        """Whether the ad is handled by a professional seller."""
        cat_text = self.tag.find_next('div', class_='category').text
        return 'pro' in cat_text

    @property
    def pubdate(self):
        """The ad publication date."""
        pubdate_text = self.tag.find_next('div', class_='date').text
        daytext, hourtext = pubdate_text.split('\n')[1:3]

        # parsing of the day text
        if daytext == "Aujourd'hui":
            date = datetime.date.today()
        elif daytext == "Hier":
            date = datetime.date.today() - datetime.timedelta(days=1)
        else:
            date_match = re.search(date_pattern, daytext)
            day_nbr = int(date_match.groupdict()['day'])
            month = abbr_months[date_match.groupdict()['month']]
            current_year = datetime.date.today().year
            date = datetime.date(current_year, month, day_nbr)

        # parsing of the hour text
        hour_match = re.search(hour_pattern, hourtext)
        hour = int(hour_match.groupdict()['hour'])
        minute = int(hour_match.groupdict()['minute'])
        time = datetime.time(hour, minute)
        pubdate = datetime.datetime.combine(date, time)
        return pubdate

    def to_dict(self):
        """Return an Ad as dict."""
        return {
            'title': self.title,
            'url': self.url,
            'price': self.price,
            'city': self.city,
            'pro': self.pro,
            'pubdate': self.pubdate,
        }
