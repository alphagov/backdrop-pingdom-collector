import unittest
from hamcrest import *
from collector.pingdom import Collector


class TestCollector(unittest.TestCase):
    def test_collector(self):
        config = {"foo": "bat"}
        collector = Collector(config)

        #collector.send_records_for()

        assert_that(collector, is_(instance_of(Collector)))