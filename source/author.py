"""
UWE Review Scraper Tool
Author Module
author: hugh@unknownworlds.com
"""
from source.valve_object import ValveObject

class Author(ValveObject):
    """
    An instance of a particular review author
    """

    def _parse_data(self, raw_data: dict) -> None:

        self._steamid = raw_data['steamid']
        self._num_games_owned = raw_data['num_games_owned']
        self._num_reviews = raw_data['num_reviews']
        self._playtime_forever = raw_data['playtime_forever']
        self._playtime_last_two_weeks = raw_data['playtime_last_two_weeks']
        self._last_played = self._parse_timestamp(raw_data['last_played'])

        return

    @staticmethod
    def csv_headers() -> [str]:
        """
        Return a list of headers representing author fields
        """
        csv_headers = ['author_steamid','author_num_games_owned','author_num_reviews',
                       'author_playtime_forever', 'author_playtime_two_weeks',
                       'author_last_played']
        return csv_headers

    def csv_line(self) -> [str]:
        """
        Return a list of values describing this author
        """
        
        csv_line = [str(self._steamid), str(self._num_games_owned), str(self._num_reviews),
                    str(self._playtime_forever), str(self._playtime_last_two_weeks),
                    str(self._last_played)]
        return csv_line
