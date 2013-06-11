from datetime import date, datetime
import json
from pprint import pprint
import sys
import argparse
from backdrop.pingdom import Pingdom

def get_contents_as_json(path_to_file):
    with open(path_to_file) as file_to_load:
        contents = file_to_load.read()
    return contents

parser = argparse.ArgumentParser(
    description="Read up time and response time from the Pingdom API and send"
                "to backdrop"
)

parser.add_argument('-q', '--query', dest='query',
                    help="File containing query and destination information")

parser.add_argument('-c', '--credentials', dest='credentials',
                    help="File containing Pingdom credentials",
                    default="config/credentials.json")

args = parser.parse_args()

pingdom_credentials = get_contents_as_json(args.credentials)
query = get_contents_as_json(args.query)

pingdom = Pingdom(pingdom_credentials)

name_of_check = json.loads(args.query)

name = "EFG"
r = pingdom.uptime_for_week(pingdom.check_id(name), date.today())

pprint(r)
