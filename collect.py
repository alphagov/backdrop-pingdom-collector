from datetime import date
import json
from backdrop.collector.write import Bucket
from collector.pingdom import Pingdom
from backdrop.collector import arguments

def get_contents_as_json(path_to_file):
    with open(path_to_file) as file_to_load:
        print path_to_file
        return json.load(file_to_load)



def convert_from_pingdom_to_backdrop(pingdom_stats, name_of_check):
    timestamp = pingdom_stats['starttime'].isoformat()
    return {
        '_id': "%s.%s" % (name_of_check, timestamp),
        '_timestamp': timestamp,
        'avgresponse': pingdom_stats['avgresponse'],
        'uptime': pingdom_stats['uptime'],
        'downtime': pingdom_stats['downtime'],
        'unmonitored': pingdom_stats['unmonitored'],
    }

if __name__ == '__main__':
    args = arguments.parse_args(name="Pingdom")


    pingdom = Pingdom(args.credentials)

    check_name = args.query['query']['name']
    pingdom_stats = pingdom.uptime_for_last_24_hours(check_name, date.today())

    bucket_url = args.query['target']['bucket']
    bucket_token = args.query['target']['token']
    bucket = Bucket(url=bucket_url, token=bucket_token)
    bucket.post([convert_from_pingdom_to_backdrop(thing, check_name) for
                 thing in pingdom_stats])
