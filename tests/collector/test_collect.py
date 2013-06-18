import datetime
import unittest
from hamcrest import *
import pytz
from collect import convert_from_pingdom_to_backdrop


class TestCollect(unittest.TestCase):
    def test_converting_from_pingdom_to_backdrop_records(self):
        hourly_stats = {
            u'avgresponse': 721,
            u'downtime': 523,
            u'starttime': datetime.datetime(2013, 6, 15, 22, 0,
                                            tzinfo=pytz.UTC),
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
