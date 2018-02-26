"""
UWE Review Scraper Tool
Request Module
author: hugh@unknownworlds.com
"""
from urllib.request import Request as WebRequest
from urllib.request import urlopen
from urllib.error import HTTPError
import json
import copy
from source.review import Review

class Request:
    """
    Retrieve a set of reviews from a given offset
    """
    _PARAMETERS = {
        'filter': 'recent',
        'language': 'all',
        'review_type': 'all',
        'purchase_type': 'all'
    }
    _HEADERS = {'Content-Type': 'application/json'}
    _API_ROOT = 'store.steampowered.com/appreviews/'
    _API_TAIL = '?json=1'

    def __init__(self, app_id: int, offset: int):
        
        assert isinstance(offset, int)
        assert isinstance(app_id, int)
        self._offset = offset
        self._app_id = app_id
        self._reviews = None
        self._total_available = None

        return

    def execute(self):
        """
        Execute the underlying http request
        """
        url = 'https://' + self._API_ROOT + str(self._app_id) + self._API_TAIL
        for key in self._PARAMETERS:
            url += '&' + key + '=' + self._PARAMETERS[key]
        url += '&start_offset=' + str(self._offset)
        request = WebRequest(url, method='GET')
        response = urlopen(request)
        raw_response = json.loads(response.read().decode('utf-8'))
        self._reviews = list()
        for raw_review in raw_response['reviews']:
            self._reviews.append(Review(raw_review))

        try:
            self._total_available = raw_response['query_summary']['total_reviews']
        except KeyError:
            self._total_available = None

        return

    def reviews(self) -> [Review]:
        """
        Return retrieved reviews
        """ 
        if self._reviews is None:
            raise RuntimeError("Reviews requested before execution completed")

        return self._reviews

    def number_of_reviews_retrieved(self) -> int:
        """
        Return the number of reviews retrieved in this batch
        """
        if self._reviews is None:
            raise RuntimeError("Reviews requested before execution completed")
        return len(self._reviews)

    def total_reviews_available(self) -> int:
        """
        Return the total number of reviews estimated to be available at
        the time of this request.
        """
        if self._reviews is None:
            raise RuntimeError("Reviews requested before execution completed")
        return self._total_available

    def csv_lines(self) -> [[str]]:
        """
        Return a list of lists of strings descrbing this requests reviews
        """
        strings = list()
        for review in self._reviews:
            strings.append(review.csv_line())
        return strings