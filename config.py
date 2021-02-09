from decouple import config


class Config:
    """
    Base Config
    """
    YT_KEYS = [i for i in config('YT_KEY', default="").split(" ") if i]
    PAGINATION_LIMIT = 10
    YOUTUBE_RESULT_LIMIT = 10
    YT_PERIODIC_INTERVAL = 20.0

    if len(YT_KEYS) == 0:
        print("No Youtube API keys found")
        exit()


class ProdConfig(Config):
    """
    Production Config
    """
    FLASK_ENV = 'development'  # For testing
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = config("PROD_DATABASE_URL", default=None)
    CELERY_BROKER_URL = config("PROD_BROKER_URL", default=None)
    CELERY_RESULT_BACKEND = config("PROD_RESULT_BACKEND", default=None)

    # TODO: Possible to check by key/value pair of list
    print("DATABASE_URL:", SQLALCHEMY_DATABASE_URI)
    if SQLALCHEMY_DATABASE_URI is None:
        print("Database URL not found")
        exit()
    if CELERY_BROKER_URL is None:
        print("Celery Broker URL not found")
        exit()
    if CELERY_RESULT_BACKEND is None:
        print("Celery Result URL not found")
        exit()


class DevConfig(Config):
    """
    Development Config
    """
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config("DEV_DATABASE_URL", default=None)
    CELERY_BROKER_URL = config("DEV_BROKER_URL", default=None)
    CELERY_RESULT_BACKEND = config("DEV_RESULT_BACKEND", default=None)

    if SQLALCHEMY_DATABASE_URI is None:
        print("Database URL not found")
        exit()
    if CELERY_BROKER_URL is None:
        print("Celery Broker URL not found")
        exit()
    if CELERY_RESULT_BACKEND is None:
        print("Celery Result URL not found")
        exit()
