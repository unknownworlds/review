"""
UWE Review Scraper Tool
Batch Module
author: hugh@unknownworlds.com
"""
from multiprocessing.dummy import Pool
from source.request import Request
import datetime

class Batch:
    """
    Concurrently retrieves a set of reviews
    """
    _DEFAULT_THREADS = 8
    _REVIEWS_PER_BATCH = 20
    _TIME_FORMAT = "[%Y-%m-%d_%H:%M:%S]"
    
    def __init__(self, app_id: int, start: int, concurrent_requests: int = None):
        assert isinstance(start, int)
        assert isinstance(app_id, int)
        if concurrent_requests is not None:
            assert isinstance(concurrent_requests, int)
            self._threads = concurrent_requests
        else:
            self._threads = self._DEFAULT_THREADS
        self._start = start
        self._pool = Pool(self._threads)
        self._requests = list()
        stop = start + (self._threads * self._REVIEWS_PER_BATCH)
        for offset in list(range(start, stop, self._REVIEWS_PER_BATCH)):
            self._requests.append(Request(app_id, offset))
        assert len(self._requests) == self._threads
        _ = self._pool.map(self._execute_request, self._requests)
        self._pool.close()
        self._pool.join()

        return

    def _execute_request(self, request: Request) -> None:
        """
        Execute a request
        """
        request.execute()
        return

    def print_reviews(self) -> None:
        for request in self._requests:
            reviews = request.reviews()
            for review in reviews:
                print(review.describe())

    def number_of_reviews_retrieved(self) -> int:
        """
        Return the integer number of reviews retrieved
        in this batch
        """
        if hasattr(self, '_number_reviews_retrieved'):
            return self._number_reviews_retrieved
        count = 0
        for request in self._requests:
            count += request.number_of_reviews_retrieved()
        assert isinstance(count, int)
        self._number_reviews_retrieved = count
        return count

    def _total_retrieved(self) -> int:
        """
        Return the total number of reviews retrieved so far
        """
        if hasattr(self, '_total_retrieved_so_far'):
            return self._total_retrieved_so_far
        self._total_retrieved_so_far = self._start + self.number_of_reviews_retrieved()
        assert isinstance(self._total_retrieved_so_far, int)
        return self._total_retrieved_so_far

    def next_batch_start(self) -> int:
        """
        Return the integer offset at which a following Batch
        should start.
        """
        start = self._total_retrieved() + 1
        return start

    def estimated_total_available(self) -> int:
        """
        Return an integer number of reviews estimated to be available
        on Steam. May return None, as Valve is inconsistent about returning
        total available reviews in query summaries.
        """
        for request in self._requests:
            if request.total_reviews_available() is not None:
                return request.total_reviews_available()
        return None

    def _completion_proportion(self, total_available: int) -> float:
        """
        Return float describing the proportion of total reviews
        that have been retrieved
        """
        total_retrieved = self.number_of_reviews_retrieved() + self._start
        proportion = total_retrieved / total_available
        assert isinstance(proportion, float)
        return proportion

    def _completion_percentage(self, total_available: int) -> str:
        """
        Return as string percentage estimated completion
        """
        return str(int(self._completion_proportion(total_available) * 100)) + '%'

    def estimate_progress(self, operation_start: datetime.datetime, total_available: int) -> str:
        """
        Return a string describing present progress
        """
        estimate = datetime.datetime.strftime(datetime.datetime.now(), self._TIME_FORMAT)
        total_retrieved = self.number_of_reviews_retrieved() + self._start
        estimate += " Retrieved " + "{:,}".format(total_retrieved)
        estimate += " of ~" + "{:,}".format(total_available)
        estimate += " available reviews (" + self._completion_percentage(total_available) + ')'
        passed_time = datetime.datetime.now() - operation_start
        seconds_remaining = passed_time.total_seconds() / self._completion_proportion(total_available)
        time_remaining = datetime.timedelta(seconds=seconds_remaining)
        time_remaining_str = str(time_remaining).split('.')[0]
        estimate += '. ~' + time_remaining_str + ' remaining.'
        return estimate

    def csv_lines(self) -> [[str]]:
        """
        Return a list of lists of strings descrbing this batches reviews
        """
        strings = list()
        for request in self._requests:
            strings += request.csv_lines()

        return strings
