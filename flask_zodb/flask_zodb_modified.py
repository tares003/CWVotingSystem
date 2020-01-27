import flask
import transaction
import zodburi

try:
    from collections import UserDict
except ImportError:  # for Python 2
    from UserDict import IterableUserDict as UserDict

from ZODB.DB import DB
from contextlib import contextmanager, closing
from werkzeug.utils import cached_property

from BTrees.OOBTree import OOBTree as BTree
from persistent import Persistent as Object
from persistent.list import PersistentList as List
from persistent.mapping import PersistentMapping as Dict

# Python 3 compatibility
try:
    basestring
except NameError:
    basestring = str

__all__ = ['ZODB', 'Object', 'List', 'Dict', 'BTree']


class ZODB(UserDict):
    """Extension object.  Behaves as the root object of the storage during
    requests, i.e. a `~persistent.mapping.PersistentMapping`.

    ::

        db = ZODB()

        app = Flask(__name__)
        db.init_app(app)

    As a shortcut if you initiate ZODB after Flask you can do this::

        app = Flask(__name__)
        db = ZODB(app)

    """
    name_of_instance = None

    def __init__(self, db_name, name_of_instance, app=None):
        if app is not None:
            print(name_of_instance)
            self.init_app(app, db_name, name_of_instance)

    def init_app(self, app, db_name, name_of_instance):
        """Configure a Flask application to use this ZODB extension."""
        # assert 'zodb'+self.name_of_instance not in app.extensions, \
        #        'app already initiated for zodb'
        self.name_of_instance = 'zodb' + name_of_instance
        app.extensions[self.name_of_instance] = _ZODBState(self, app, db_name)
        app.teardown_request(self.close_db)

    def close_db(self, exception):
        """Added as a `~flask.Flask.teardown_request` to applications to
        commit the transaction and disconnect ZODB if it was used during
        the request."""
        if self.is_connected:
            if exception is None and not transaction.isDoomed():
                transaction.commit()
            else:
                transaction.abort()
            self.connection.close()

    # Modified to all to specift
    def create_db(self, app, storage):
        """Create a ZODB connection pool from the *app* configuration."""

        # assert 'ZODB_STORAGE' in app.config, \
        #        'ZODB_STORAGE not configured'
        # storage = app.config['ZODB_STORAGE']

        if isinstance(storage, basestring):
            factory, dbargs = zodburi.resolve_uri(storage)
        elif isinstance(storage, tuple):
            factory, dbargs = storage
        else:
            factory, dbargs = storage, {}
        return DB(factory(), **dbargs)

    @property
    def is_connected(self):
        """True if there is a Flask request and ZODB was connected."""
        return (flask.has_request_context() and
                hasattr(flask._request_ctx_stack.top, 'zodb_connection' + self.name_of_instance))

    @property
    def connection(self):
        """Request-bound database connection."""
        assert flask.has_request_context(), \
            'tried to connect zodb outside request'
        if not self.is_connected:
            connector = flask.current_app.extensions['zodb' + self.name_of_instance]
            flask._request_ctx_stack.top['zodb_connection' + self.name_of_instance] = connector.db.open()
            transaction.begin()
        return flask._request_ctx_stack.top['zodb_connection' + self.name_of_instance]

    @property
    def data(self):
        return self.connection.root()


class _ZODBState(object):
    """Adds a ZODB connection pool to a Flask application."""

    def __init__(self, zodb, app, db_name):
        self.zodb = zodb
        self.app = app
        # name of db
        self.db_name = db_name

    @cached_property
    def db(self):
        """Connection pool."""
        return self.zodb.create_db(self.app, self.db_name)
