from datetime import date, datetime
import unittest
from hamcrest import *
from mock import patch, Mock
import pytz
from requests import Response
from collector.pingdom import Pingdom


class TestPingdomApi(unittest.TestCase):
    def setUp(self):
        self.config = {
            "user": "foo@bar.com",
            "password": "secret",
            "app_key": "12345"
        }

    def test_init_from_config(self):
        pingdom = Pingdom(self.config)
        assert_that(pingdom, is_(instance_of(Pingdom)))

    @patch("requests.get")
    def test_querying_for_uptime(self, mock_get_request):
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"summary": {"hours": []}}
        mock_get_request.return_value = fake_response

        pingdom = Pingdom(self.config)
        mock_check_id = Mock()
        mock_check_id.return_value = '12345'
        pingdom.check_id = mock_check_id
        uptime = pingdom.uptime_for_last_24_hours(name='Foo',
                                                      day=date(2013, 1,
                                                                     1))

        from_value = mock_get_request.call_args_list[0][1]['params']['from']
        to_value = mock_get_request.call_args_list[0][1]['params']['to']
        seconds_in_day = 60 * 60 * 24

        mock_get_request.assert_called_with(
            url="https://api.pingdom.com/api/2.0/summary.performance/12345",
            auth=("foo@bar.com","secret"),
            params={
                "includeuptime": "true",
                "from": 1356912000.0,
                "to": 1356998400.0,
                "resolution": "hour"
            },
            headers={
                "App-Key": "12345"
            }
        )

        assert_that(to_value - from_value, is_(seconds_in_day))
        assert_that(uptime, is_([]))

    @patch("requests.get")
    def test_response_unixtime_converted_to_isodate(self, mock_get_request):
        mock_response = Mock()
        mock_response.json.return_value = {
            'summary': {
                'hours': [{'starttime': 1356998400}, {'starttime': 1356998500}]
            }
        }
        mock_get_request.return_value = mock_response

        pingdom = Pingdom(self.config)

        mock_check_id = Mock()
        mock_check_id.return_value = '12345'
        pingdom.check_id = mock_check_id
        uptime = pingdom.uptime_for_last_24_hours(name='Foo',
                                                      day=date(2013, 1, 1))

        assert_that(uptime[0]['starttime'],
                    is_(datetime(2013, 1, 1, 0, tzinfo=pytz.UTC)))
        assert_that(uptime[1]['starttime'],
                    is_(datetime(2013, 1, 1, 0, 1, 40, tzinfo=pytz.UTC)))

    @patch("requests.get")
    def test_uptime_returns_none_when_there_is_an_error(self, mock_request):
        response = Response()
        response.status_code = 500
        mock_request.return_value = response

        pingdom = Pingdom(self.config)
        mock_check_id = Mock()
        mock_check_id.return_value = '12345'
        pingdom.check_id = mock_check_id
        uptime = pingdom.uptime_for_last_24_hours(name="don't care",
                                                      day=date(2013, 1, 1))
        assert_that(uptime, is_(None))
