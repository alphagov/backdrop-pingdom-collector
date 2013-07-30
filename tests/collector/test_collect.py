from datetime import datetime
import unittest
from hamcrest import *
import pytz
from collect import convert_from_pingdom_to_backdrop, truncate_hour_fraction


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
        doc = convert_from_pingdom_to_backdrop(hourly_stats, name_of_check)

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

        doc = convert_from_pingdom_to_backdrop(hourly_stats, name_of_check)

        assert_that(doc, has_entry('_id', 'name_with_whitespace.'
                                          '2013-06-15T22:00:00+00:00'))

    def test_truncate_hour_fraction(self):
        assert_that(
            truncate_hour_fraction(datetime(2013, 6, 15, 22, 0, 0, 0)),
            is_(datetime(2013, 6, 15, 22, 0, 0, 0))
        )
        assert_that(
            truncate_hour_fraction(datetime(2013, 6, 15, 22, 1, 2, 3)),
            is_(datetime(2013, 6, 15, 22, 0, 0, 0))
        )
