from datetime import date
import json
from pprint import pprint
from collector.pingdom import Pingdom
from backdrop.collector import arguments

def get_contents_as_json(path_to_file):
    with open(path_to_file) as file_to_load:
        print path_to_file
        return json.load(file_to_load)

args = arguments.parse_args(name="Pingdom")


pingdom = Pingdom(args.credentials)


pprint(args.query)

r = pingdom.uptime_for_last_24_hours(args.query['query']['name'], date.today())

pprint(r)
