from datetime import date, datetime
import json
from pprint import pprint
import sys
from backdrop.pingdom import Pingdom


config_path = sys.argv[1]

config = json.loads(open(config_path).read())

pingdom = Pingdom(config)

name = "EFG"
r = pingdom.uptime_for_week(pingdom.check_id(name), date.today())

pprint(r)
