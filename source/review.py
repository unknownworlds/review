"""
UWE Review Scraper Tool
Review Module
author: hugh@unknownworlds.com
"""
from source.valve_object import ValveObject
from source.author import Author
import datetime

class Review(ValveObject):
    """
    An instance of an individual Steam review
    """

    def describe(self) -> str:
        """
        Return a string describing this review
        """
        return str(self._recommendation_id)

    def _parse_data(self, raw_data: dict) -> None:

        self._recommendation_id = raw_data['recommendationid']
        self._author = Author(raw_data['author'])
        self._language = raw_data['language']
        self._review = raw_data['review']
        self._timestamp_created = self._parse_timestamp(raw_data['timestamp_created'])
        self._timestamp_updated = self._parse_timestamp(raw_data['timestamp_updated'])
        self._voted_up = raw_data['voted_up']
        self._votes_up = raw_data['votes_up']
        self._votes_funny = raw_data['votes_funny']
        self._weighted_vote_score = raw_data['weighted_vote_score']
        self._comment_count = raw_data['comment_count']
        self._steam_purchase = raw_data['steam_purchase']
        self._received_for_free = raw_data['received_for_free']
        self._written_during_early_access = raw_data['written_during_early_access']

        return

    @staticmethod
    def csv_headers() -> [str]:
        """
        Return csv headers
        """
        csv_headers = ['review_id'] + Author.csv_headers()
        csv_headers += [
            'language',
            'review_text',
            'time_created',
            'time_updated',
            'voted_up',
            'votes_up',
            'votes_funny',
            'weighted_review_score',
            'comment_count',
            'steam_purchase',
            'received_for_free',
            'early_access'
        ]
        return csv_headers

    def csv_line(self) -> [str]:
        """
        Return a list of values describing this review
        """
    
        csv_line = [str(self._recommendation_id)] + self._author.csv_line()
        csv_line += [str(self._language), str(self._review), str(self._timestamp_created),
                     str(self._timestamp_updated), str(self._voted_up),
                     str(self._votes_up), str(self._votes_funny), str(self._weighted_vote_score),
                     str(self._comment_count), str(self._steam_purchase),
                     str(self._received_for_free), str(self._written_during_early_access)]

        return csv_line
