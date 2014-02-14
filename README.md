# backdrop-pingdom-collector

[![Build Status](https://travis-ci.org/alphagov/backdrop-pingdom-collector.png?branch=master)](https://travis-ci.org/alphagov/backdrop-pingdom-collector?branch=master)


[![Dependency Status](https://gemnasium.com/alphagov/backdrop-pingdom-collector.png)](https://gemnasium.com/alphagov/backdrop-pingdom-collector)

Collects data from [Pingdom](https://www.pingdom.com/)'s api about up and response times and sends it to [backdrop](https://github.com/alphagov/backdrop).

To test locally:

- create a config json file for credentials following the format in config/example_credentials.json;
- create a config json file for the pingdom query following the format in queries/example_query.json;
- create a log directory;
- run with:

```  python collector.py -c path/to/mycredentials.json -q path/to/myquery.json  ```