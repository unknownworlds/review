"""
UWE Review Scraper Tool
Review Module
author: hugh@unknownworlds.com
"""
from datetime import datetime

class ValveObject:
    """
    An instance of an individual Steam review
    """

    def __init__(self, raw_data: dict):

        assert isinstance(raw_data, dict)

        try:
            self._parse_data(raw_data)
        except KeyError:
            print('\n Begin raw data:\n')
            print(raw_data)
            print('\n -- End raw data')
            raise RuntimeError('Valve responded with an unrecognised review format')

    def _parse_timestamp(self, unix_timestamp: int) -> datetime:
        """
        Parse a unix timestamp into a datetime
        """
        assert isinstance(unix_timestamp, int)
        return datetime.utcfromtimestamp(unix_timestamp)

    def _parse_data(self, raw_data: dict) -> None:
        """
        Parse raw object data into member variables
        """
        raise NotImplementedError

    def _add(self, member) -> str:
        """
        Return a comma terminated value
        """
        addition = str(member) + ','
        return addition
