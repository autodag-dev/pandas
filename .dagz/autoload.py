from dagz.integ.psycopg import PG_CONFIG
from dagz.integ.pymysql import MYSQL_CONFIG


def setup_adbc_driver():
    """Custom ADBC driver rerouting using DAGZ rerouting framework."""
    import adbc_driver_postgresql.dbapi
    _orig_adbc_connect = adbc_driver_postgresql.dbapi.connect

    def _override_connect(uri, *args, **kwargs):
        uri = PG_CONFIG.maybe_reroute_uri(uri)
        return _orig_adbc_connect(uri, *args, **kwargs)

    adbc_driver_postgresql.dbapi.connect = _override_connect


def setup_parallel_db():
    import dagz.integ.psycopg2
    import dagz.integ.pymysql

    PG_CONFIG.configure(
        rewrite_db_name=PG_CONFIG.default_rewrite_db_name,
        should_reroute=PG_CONFIG.default_should_reroute,
        worker_init=dagz.integ.psycopg2.create_worker_init(["pandas"], host="127.0.0.1", port=5432, user="postgres", password="postgres"),
        prepare=None,
    )
    MYSQL_CONFIG.configure(
        rewrite_db_name=MYSQL_CONFIG.default_rewrite_db_name,
        should_reroute=MYSQL_CONFIG.default_should_reroute,
        worker_init=dagz.integ.pymysql.create_worker_init(["pandas"], host="127.0.0.1", port=3306, user="root", password=""),
        prepare=None,
    )


def init(in_pytest):
    setup_parallel_db()
    setup_adbc_driver()
