from datetime import datetime
import json
import logging

from backdrop.collector.logging_setup import set_up_logging
from backdrop.collector.write import Bucket
from backdrop.collector import arguments

from collector.pingdom import Pingdom


def get_contents_as_json(path_to_file):
    with open(path_to_file) as file_to_load:
        logging.debug(path_to_file)
        return json.load(file_to_load)


def convert_from_pingdom_to_backdrop(pingdom_stats, name_of_check):
    timestamp = pingdom_stats['starttime'].isoformat()
    name_for_id = name_of_check.replace(' ', '_')
    return {
        '_id': "%s.%s" % (name_for_id, timestamp),
        '_timestamp': timestamp,
        'avgresponse': pingdom_stats['avgresponse'],
        'uptime': pingdom_stats['uptime'],
        'downtime': pingdom_stats['downtime'],
        'unmonitored': pingdom_stats['unmonitored'],
        'check': name_of_check
    }


def truncate_hour_fraction(a_datetime):
    return a_datetime.replace(minute=0, second=0, microsecond=0)


if __name__ == '__main__':
    set_up_logging('pingdom', logging.DEBUG)

    args = arguments.parse_args(name="Pingdom")

    collection_date = datetime.now()
    if args.end_at:
        collection_date = args.end_at

    pingdom = Pingdom(args.credentials)

    check_name = args.query['query']['name']
    timestamp = truncate_hour_fraction(collection_date)
    pingdom_stats = pingdom.stats_for_24_hours(check_name, timestamp)

    bucket_url = args.query['target']['bucket']
    bucket_token = args.query['target']['token']
    bucket = Bucket(url=bucket_url, token=bucket_token)
    bucket.post([convert_from_pingdom_to_backdrop(thing, check_name) for
                 thing in pingdom_stats])
