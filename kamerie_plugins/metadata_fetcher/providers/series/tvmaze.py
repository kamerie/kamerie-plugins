import requests
from pprint import pformat
from kamerie.utilities.utilities import get_logger
from kamerie.utilities.db import db, attrs_to_db_set, query_by_id, ObjectId, sanitize_name, FIELD_SERIES_ID

BASE_ENDPOINT = 'http://api.tvmaze.com'
SERIES_ENDPOINT = BASE_ENDPOINT + '/search/shows?q=%s'
EPISODES_ENDPOINT = BASE_ENDPOINT + '/shows/%s/episodes'
SCORE_THRESHOLD = 1.0


class TVMaze(object):

    def __init__(self):
        self._logger = get_logger('tvmaze')
        self.db = db

    def fetch_metadata(self, media_item):
        self._logger.info("Fetching tvmaze info for %s" % pformat(media_item.dump_attributes()))
        ep = self.db.Media.find_one(query_by_id(media_item))
        serieses = []

        if ep.get(FIELD_SERIES_ID, None) is None:
            series_by_name = self.db.Series.find_one({'sanitized_name': sanitize_name(ep['name'])})

            if series_by_name is not None:
                self._logger.info('Series found by name')
                serieses.append(series_by_name)
                matched_series = series_by_name

            else:
                r = requests.get(SERIES_ENDPOINT % media_item.name)

                if r.status_code == 200:
                    # for each show returned by api
                    for result in r.json():
                        # find by show name
                        # find by api show id
                        series_by_tvmaze_id = self.db.Series.find_one({
                            'tvmaze': { '$elemMatch': {
                                'show.id': result['show']['id']
                            }}})

                        # if not found, append it
                        if series_by_tvmaze_id is None:
                            self._logger.info('Series not found in collection, inserting new one')
                            if result.get('searches', None) is None:
                                result['searches'] = []
                            result['searches'].append(media_item.name)

                            inserted = self.db.Series.insert_one({
                                'name': result['show']['name'],
                                'sanitized_name': sanitize_name(result['show']['name']),
                                'api_results': {'tvmaze': [result]},
                                'main_source': 'tvmaze'
                            })
                            serieses.append(inserted)
                            matched_series = inserted
                        else:
                            self._logger.info('Series found by TVMaze ID')
                            serieses.append(series_by_tvmaze_id)
                            matched_series = series_by_tvmaze_id

            results = [result for result in serieses if result.get('score', 1.0) >= SCORE_THRESHOLD]

            if matched_series is None and len(results) > 0:
                matched_series = results[0]

            attrs = {
                FIELD_SERIES_ID: query_by_id(matched_series),
            }

            self._logger.info('Saving result to media item')
            self.db.Media.update_one(query_by_id(media_item), attrs_to_db_set(attrs))
