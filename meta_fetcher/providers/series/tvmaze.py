import requests
from pprint import pformat
from kamerie.utilities.utilities import get_logger
from kamerie.utilities.db import db, attrs_to_db_set, query_by_id, ObjectId, sanitize_name, FIELD_SERIES_ID
from operator import itemgetter
from collections import defaultdict

BASE_ENDPOINT = 'http://api.tvmaze.com'
SERIES_ENDPOINT = BASE_ENDPOINT + '/search/shows?q=%s'
EPISODES_ENDPOINT = BASE_ENDPOINT + '/shows/%s/episodes'
SCORE_THRESHOLD = 1.0
DEFAULT_SCORE = 0.5


class TVMaze(object):

    def __init__(self):
        self._logger = get_logger('tvmaze')
        self.db = db

    def fetch_metadata(self, media_item):
        self._logger.info("Fetching tvmaze info for %s" % pformat(media_item.dump_attributes()))

        ep = self.db.Media.find_one(query_by_id(media_item))
        matched_series = None
        serieses = []

        if ep.get(FIELD_SERIES_ID, None) is None:
            series_by_name = self.db.Series.find_one({'sanitized_name': sanitize_name(ep['name'])})

            if series_by_name is not None:
                self._logger.info('Series found by name')
                serieses.append(series_by_name)
                matched_series = series_by_name

            else:
                series_res = requests.get(SERIES_ENDPOINT % media_item.name)

                if series_res.status_code == 200:
                    # for each show returned by api
                    for result in series_res.json():
                        # find by show name
                        # find by api show id
                        series_by_tvmaze_id = self.db.Series.find_one({
                            'tvmaze': { '$elemMatch': {
                                'show.id': result['show']['id']
                            }}})

                        ep_res = requests.get(EPISODES_ENDPOINT % result['show']['id'])
                        # if not found, append it
                        if series_by_tvmaze_id is None:
                            self._logger.info('Series not found in collection, inserting new one')

                            attrs = {
                                'name': result['show']['name'],
                                'sanitized_name': sanitize_name(result['show']['name']),
                                'searches': [media_item.name],
                                'results_cache': {'tvmaze': [result]},
                                'episodes': ep_res.json(),
                                'information': result,
                                'information_type': 'tvmaze',
                            }
                            inserted = self.db.Series.insert_one(attrs)
                            serieses.append(attrs)
                            if matched_series is None:
                                matched_series = inserted
                        else:
                            self._logger.info('Series found by TVMaze ID')
                            serieses.append(series_by_tvmaze_id)
                            if matched_series is None:
                                matched_series = series_by_tvmaze_id

            results = [result for series in serieses if series.get('score', DEFAULT_SCORE) >= SCORE_THRESHOLD]
            results = sorted(results, key=lambda x: x['score'] if 'score' in x else DEFAULT_SCORE, reverse=True)

            if matched_series is None and len(results) > 0:
                matched_series = results[0]

            if len(results) == 0 and matched_series is None:
                self._logger.warn('No metadata found for %s' % ep['name'])
                return

            try:
                attrs = {
                    FIELD_SERIES_ID: query_by_id(matched_series)['_id'],
                }

                self._logger.info('Saving result to media item')
                self.db.Media.update_one(query_by_id(media_item), attrs_to_db_set(attrs))
            except KeyError as e:
                self._logger.error('Problem saving info to database: %s' % e)
