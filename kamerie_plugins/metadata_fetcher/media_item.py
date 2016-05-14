from kamerie.utilities.consts import MEDIA_PATH, MEDIA_TYPE, TYPE_SERIES
from kamerie.utilities.db import db, ObjectId, query_by_id, attrs_to_db_set, sanitize_name, \
                                 FIELD_ID, FIELD_NAME, FIELD_SEASON, FIELD_EPISODE, \
                                 FIELD_SANITIZED_NAME
from os import path
import re

SEASON_EP_PATTERN = r's?([0-9]+)[ex]([0-9]+)'
CLEANUP_PATTERN = r'^\W+|\W+$'


class MediaItem(object):

    def __init__(self, **media_info):
        self.path = media_info[MEDIA_PATH]
        self.type = media_info[MEDIA_TYPE]
        self.db_info = media_info
        self.db = db

        if self.type == TYPE_SERIES:
            self.name = None
            self.season = None
            self.episode = None

            self.get_series_info()

    def get_series_info(self):
        if self.name is None or self.episode is None or self.season is None:
            basename = path.basename(self.path)
            matches = re.compile(SEASON_EP_PATTERN, re.IGNORECASE).match(basename)

            if matches is None:
                raise AttributeError("Couldn't find series information for %s." %
                                     path.join(path.basename(path.dirname(self.path)), basename))

            self.season = matches.group(1).zfill(2)
            self.episode = matches.group(2).zfill(2)

            ep_index = basename.index(matches.group(0))

            if (ep_index > 0):
                self.name = self.trim_name(basename[0:ep_index])
            else:
                name = path.basename(path.dirname(self.path))

                if "season" in name.lower():
                    idx = name.lower().index("season")
                    if idx > 0:
                        self.name = self.trim_name(name[0:idx])
                    else:
                        self.name = self.trim_name(path.dirname(name))
                else:
                    self.name = self.trim_name(path.basename(path.dirname(path.dirname(self.path))))

        full_attrs = self.dump_attributes()
        keys = [key for key in full_attrs.keys() if key not in [MEDIA_PATH, MEDIA_TYPE, '_id']]
        attrs = {key: full_attrs[key] for key in keys}

        self.db.Media.update_one(query_by_id(self), attrs_to_db_set(attrs))

        return {
            FIELD_NAME: self.name,
            FIELD_SEASON: self.season,
            FIELD_EPISODE: self.episode,
        }

    def trim_name(self, name):
        return re.sub(CLEANUP_PATTERN, '', name)

    def dump_attributes(self):
        return {
            MEDIA_PATH: self.path,
            MEDIA_TYPE: self.type,
            FIELD_NAME: self.name,
            FIELD_SANITIZED_NAME: sanitize_name(self.name),
            FIELD_SEASON: self.season,
            FIELD_EPISODE: self.episode,
            FIELD_ID: ObjectId(self.db_info['_id']['$oid'])
        }
