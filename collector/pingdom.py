from datetime import timedelta, datetime
import pytz
import requests
import time
import logging

logging.basicConfig(level=logging.DEBUG)


class Pingdom(object):
    def __init__(self, config):
        self.user = config['user']
        self.password = config['password']
        self.app_key = config['app_key']
        self.API_LOCATION = "https://api.pingdom.com/api/2.0/"


    def _make_request(self, path, url_params={}):
        response = requests.get(
            url=self.API_LOCATION + path,
            auth=(self.user, self.password),
            headers={
                "App-Key": self.app_key
            },
            params=url_params
        )
        return response

    def _build_response(self, response):
        hours = response['summary']['hours']
        new_hours = []
        for hour in hours:
            hour.update({'starttime': datetime.fromtimestamp(
                hour['starttime'],
                tz=pytz.UTC
            )})
            new_hours.append(hour)
        return new_hours

    def uptime_for_last_24_hours(self, name, day):
        app_code = self.check_id(name)
        previous_day = day - timedelta(days=1)
        params={
                "includeuptime": "true",
                "from": time.mktime(previous_day.timetuple()),
                "to": time.mktime(day.timetuple()),
                "resolution": "hour"
        }
        response = \
            self._make_request("summary.performance/" + str(app_code), params)

        if response.status_code in [500, 502, 503, 504]:
            logging.error("5xx response: %s" % response.text)
            return None
        else:
            return self._build_response(response.json())

    def check_id(self, name):
        response = self._make_request("checks")

        if response.status_code in [401, 403]:
            logging.error("401/403 response from Pingdom: bad credentials?")

        check_to_find = [check for check in response.json()["checks"]
             if check["name"] == name]

        return check_to_find[0]["id"]
