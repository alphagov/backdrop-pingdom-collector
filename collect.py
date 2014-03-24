from datetime import datetime
import json
import logging
import os

from backdrop.collector.logging_setup import set_up_logging
from backdrop.collector.write import Bucket
from backdrop.collector import arguments

from collector.pingdom import Pingdom


def main():
    configure_logging()

    args = arguments.parse_args(name="Pingdom")

    timestamp = extract_end_time_or_now(args.end_at)

    pingdom = Pingdom(args.credentials)

    check_name = args.query['query']['name']
    pingdom_stats = pingdom.stats_for_24_hours(check_name, timestamp)

    push_stats_to_bucket(
        pingdom_stats,
        check_name,
        bucket_url=args.query['target']['bucket'],
        bucket_token=args.query['target']['token'])


def configure_logging():
    app_path = os.path.dirname(os.path.realpath(__file__))
    logfile_path = os.path.join(app_path, 'log')
    set_up_logging('pingdom', logging.DEBUG, logfile_path)


def extract_end_time_or_now(end_at_datetime):
    collection_datetime = datetime.now()
    if end_at_datetime:
        collection_datetime = end_at_datetime

    return truncate_hour_fraction(collection_datetime)


def parse_time_range(start_dt, end_dt):
    """
    Convert the start/end datetimes specified by the user, specifically:
    - truncate any minutes/seconds
    - for a missing end time, use start + 24 hours
    - for a missing start time, use end - 24 hours
    - for missing start and end, use the last 24 hours
    """
    return start_dt, end_dt  # TODO


def push_stats_to_bucket(pingdom_stats, check_name, bucket_url, bucket_token):
    bucket = Bucket(url=bucket_url, token=bucket_token)
    bucket.post([convert_from_pingdom_to_backdrop(thing, check_name) for
                 thing in pingdom_stats])


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
    main()
