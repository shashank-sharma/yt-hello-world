from decouple import config
from flask import Flask, jsonify, request
from middleware import is_required
from models import db, YTSearch
import datetime
from flask_celery import make_celery
from util import YTBuilder
from sqlalchemy import or_, desc
from errors import NoTokenFound
from sqlalchemy.dialects.postgresql import insert
from dateutil import tz
import logging

# TODO: Didn't used logger, should have used
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

celery = make_celery(app)
yt_builder = YTBuilder(app.config["YT_KEYS"])


class YoutubePeriodicTask(celery.Task):
    """
    Class Celery Task to handle scheduler
    """

    def schedule(self):
        # Use India timezone for results
        india_tz = tz.gettz('Asia/Kolkata')

        # Get datetime object in past by 10 seconds
        before = datetime.datetime.now(india_tz) - datetime.timedelta(seconds=10)
        past_time = before.strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            results = yt_builder.search("anime",
                                        app.config['YOUTUBE_RESULT_LIMIT'],
                                        past_time)
        except NoTokenFound:
            return "FAILED: No Token Found"
        except:
            return "FAILED"
        data = []
        print("Data fetched = ", len(results['items']))

        # Create List of YTSearch model object from given response
        for result in results['items']:
            if result['id']['kind'] == "youtube#video":
                data.append({
                    "video_id": result['id']['videoId'],
                    "title": result['snippet']['title'],
                    "description": result['snippet']['description'],
                    "channel_title": result['snippet']['channelTitle'],
                    "channel_id": result['snippet']['channelId'],
                    "thumbnail": result['snippet']['thumbnails']['default']['url'],
                    "published_at": result['snippet']['publishedAt'],
                    "published_time": result['snippet']['publishTime']
                })

        # Make upsert operation
        stmt = insert(YTSearch).values(data)
        stmt = stmt.on_conflict_do_update(
            constraint="ytsearch_video_id_key",
            set_={
                "title": stmt.excluded.title,
                "description": stmt.excluded.description,
                "thumbnail": stmt.excluded.thumbnail
            }
        )
        db.session.execute(stmt)
        db.session.commit()

        # Strange this method doesn't work
        # db.session.bulk_save_objects(data)
        # db.session.commit()
        return "SUCCESS"


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(app.config['YT_PERIODIC_INTERVAL'], async_get.s(), name='yt-search-scheduler')


@celery.task(name='celery_example.async_get', base=YoutubePeriodicTask)
def async_get():
    """
    Celery task to call Youtube Periodic Scheduler
    :return:
    """
    print("Updating YT Search Database")
    status = async_get.schedule()
    return status


@app.route("/ping", methods=['GET'])
def ping():
    """
    Testing endpoint if flask is working
    :return: JSON with response pong for health check
    """
    return jsonify({'response': 'pong'}), 200


@app.route("/search", methods=['POST'])
@is_required(parameters=['search', 'page'])
def search():
    """
    Search given string in ytsearch table in title and description column (case-insensitive)
    :parameters search: <string>
    :parameters page: <string>
    :return: JSON with list of results, next and previous page status
    """
    content = request.json
    page_limit = app.config['PAGINATION_LIMIT']
    search_param = content['search']
    page = content['page']
    per_page = content['per_page'] if 'per_page' in content else page_limit
    if per_page > page_limit:
        per_page = page_limit

    # Word tokenize given sentence and remove any extra spaces
    # TODO: Possibility of special characters handling with spaces and focus on words
    word_list = [word.lower() for word in search_param.strip().replace("  ", " ").split(" ")]

    # Create array of conditions with given words and search it in title and description column
    clauses = [YTSearch.title.ilike('%{0}%'.format(i)) for i in word_list] + \
              [YTSearch.description.ilike('%{0}%'.format(i)) for i in word_list]

    # Filter all rows with OR condition, order by published datetime and paginate by page count and per_page
    posts = YTSearch.query.filter(or_(*clauses)).order_by(desc(YTSearch.published_at)) \
        .paginate(page, per_page, error_out=True)

    # Get JSON data from list of objects
    result = [i.serialize() for i in posts.items]
    return jsonify({'data': result, 'has_next': posts.has_next, 'next_page': posts.next_num,
                    'has_prev': posts.has_prev, 'prev_page': posts.prev_num, 'length': len(result)}), 200


@app.route("/list", methods=['GET'])
def list():
    """
    Get list of YT Search result from database in desc order by published_at field
    :return: JSON with list of results, next and previous page status
    """

    page_limit = app.config['PAGINATION_LIMIT']
    page = request.args.get('page') if 'page' in request.args else 1
    per_page = request.args.get('per_page') if 'per_page' in request.args else page_limit

    # TODO: Can be done in much more elegant way
    try:
        page = int(page)
    except:
        page = 1

    try:
        per_page = int(per_page)
    except:
        per_page = page_limit
    if per_page > page_limit:
        per_page = page_limit

    # Get all rows and order by published datetime and paginate by page count and per_page
    posts = YTSearch.query.order_by(desc(YTSearch.published_at)) \
        .paginate(page, per_page, error_out=True)

    # Get JSON data from list of objects
    result = [i.serialize() for i in posts.items]
    return jsonify({'data': result, 'has_next': posts.has_next, 'next_page': posts.next_num,
                    'has_prev': posts.has_prev, 'prev_page': posts.prev_num, 'length': len(result)}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
