"""
UWE Review Scraper Tool
Core Module
author: hugh@unknownworlds.com
"""
import datetime
import sys
import json
import csv
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
from source.review import Review
from source.batch import Batch
from source.review import Review


OUTPUT_FILE = None
APP_ID = None
THREADS = None

HELP_TEXT = """
    Configuration flags:

    --app (-a):     [Required] Specify the Steam AppID to target.
                    E.g. python3 review.py -a 264710

    --file (-f):    [Required] Specify a file in which to write reviews.
                    E.g. python3 review.py -f all_subnautica_reviews.csv

    --threads (-t): [Optional] Specify the number of concurrent requests
                    that should be made to Steamworks. If you push this
                    too high, you may hit a rate-limit. Defaults to 8.
                    E.g. python3 review.py -t 10
"""

if len(sys.argv[1:]) < 1:
    print(HELP_TEXT)

VALID_ARGUMENTS = ['--file', '-f', '--help', '-h', '--app', '-a', '--threads', '-t']
SKIP = False
ITERATION = -1
for argument in sys.argv[1:]:
    ITERATION += 1
    if SKIP == True:
        SKIP = False
        continue
    if argument not in VALID_ARGUMENTS:
        error_string = "Invalid argument '" + str(argument) + '" supplied'
        error_string += '. Run with -h flag to see available commands'
        raise RuntimeError(error_string)
    if argument == '-h' or argument == '--help':
        quit()
    if str(argument) == '-a' or argument == '--app':
        try:
            APP_ID = int(sys.argv[1:][ITERATION + 1])
        except:
            raise RuntimeError('Value associated with --app flag invalid.')
        SKIP = True
        continue
    if argument == '--file' or argument == '-f':
        try:
            OUTPUT_FILE = str(sys.argv[1:][ITERATION + 1])
        except:
            raise RuntimeError('Value associated with --file flag invalid.')
        SKIP = True
        continue
    if argument == '--threads' or argument == '-t':
        try:
            THREADS = int(sys.argv[1:][ITERATION + 1])
        except:
            raise RuntimeError('Invalid valie associated with --threads flag')
        SKIP = True
        continue

if OUTPUT_FILE == None or APP_ID == None:
    raise RuntimeError('Required configuration flag missing. Run with --help flag.')

with open(OUTPUT_FILE, 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(Review.csv_headers())
    start = datetime.datetime.now()
    current_batch = Batch(264710, 0)
    estimated_available = current_batch.estimated_total_available()
    while current_batch.number_of_reviews_retrieved() > 0:
        print(current_batch.estimate_progress(start, estimated_available), end='\r')
        writer.writerows(current_batch.csv_lines())
        current_batch = Batch(264710, current_batch.next_batch_start())
