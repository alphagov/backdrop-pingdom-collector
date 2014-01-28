from datetime import datetime
import unittest
from hamcrest import *
import pytz
import collect
from mock import patch, Mock
from backdrop import collector 
from backdrop.collector import arguments


class TestCollect(unittest.TestCase):
    def test_converting_from_pingdom_to_backdrop_records(self):
        hourly_stats = {
            u'avgresponse': 721,
            u'downtime': 523,
            u'starttime': datetime(2013, 6, 15, 22, 0, tzinfo=pytz.UTC),
            u'unmonitored': 12,
            u'uptime': 3599
        }

        name_of_check = 'testCheck'
        doc = collect.convert_from_pingdom_to_backdrop(hourly_stats, name_of_check)

        assert_that(doc,
                    has_entry('_id', 'testCheck.2013-06-15T22:00:00+00:00'))
        assert_that(doc, has_entry('_timestamp', '2013-06-15T22:00:00+00:00'))
        assert_that(doc, has_entry('check', 'testCheck'))
        assert_that(doc, has_entry('avgresponse', 721))
        assert_that(doc, has_entry('uptime', 3599))
        assert_that(doc, has_entry('downtime', 523))
        assert_that(doc, has_entry('unmonitored', 12))

    def test_converting_to_backdrop_record_removes_whitespace_from_id(self):
        hourly_stats = {
            u'avgresponse': 721,
            u'downtime': 523,
            u'starttime': datetime(2013, 6, 15, 22, 0, tzinfo=pytz.UTC),
            u'unmonitored': 12,
            u'uptime': 3599
        }
        name_of_check = "name with whitespace"

        doc = collect.convert_from_pingdom_to_backdrop(hourly_stats, name_of_check)

        assert_that(doc, has_entry('_id', 'name_with_whitespace.'
                                          '2013-06-15T22:00:00+00:00'))

    def test_truncate_hour_fraction(self):
        assert_that(
            collect.truncate_hour_fraction(datetime(2013, 6, 15, 22, 0, 0, 0)),
            is_(datetime(2013, 6, 15, 22, 0, 0, 0))
        )
        assert_that(
            collect.truncate_hour_fraction(datetime(2013, 6, 15, 22, 1, 2, 3)),
            is_(datetime(2013, 6, 15, 22, 0, 0, 0))
        )

    def test_args_parser(self):
        stub_set_up_logging = Mock()
        collect.set_up_logging = stub_set_up_logging 
        stub_pass_args = Mock()
        stub_args = Mock()
        stub_args.end_at = None 
        stub_args.query = {'query': {'name': None}, 'target': {'bucket': None, 'token': None}}
        stub_pass_args.return_value = stub_args
        arguments.parse_args = stub_pass_args 
        mock_pingdom = Mock()
        mock_pingdom.stats_for_24_hours = Mock().return_value = ["some", "things"]
        collect.Pingdom = mock_pingdom
        collect.convert_from_pingdom_to_backdrop = Mock().return_value = "HELLOO"
        collect.args_parser(arguments)
