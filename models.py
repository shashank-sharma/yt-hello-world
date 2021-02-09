from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class YTSearch(db.Model):
    """
    Youtube API Search Database
    """
    __tablename__ = 'ytsearch'

    video_id = db.Column(db.String(11), primary_key=True, unique=True)
    title = db.Column(db.String())
    description = db.Column(db.Text())
    channel_title = db.Column(db.String())
    channel_id = db.Column(db.String(24))
    thumbnail = db.Column(db.String())
    published_at = db.Column(db.DateTime())
    published_time = db.Column(db.DateTime())

    # TODO: Possibility of using JSON field and store thumbnail as JSON for all resolution

    def __init__(self, video_id, title, description, channel_title, channel_id, thumbnail, published_at,
                 published_time):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.channel_title = channel_title
        self.channel_id = channel_id
        self.thumbnail = thumbnail
        self.published_at = published_at
        self.published_time = published_time

    def __repr__(self):
        return '<id {}>'.format(self.video_id)

    def serialize(self):
        return {
            'video_id': self.video_id,
            'title': self.title,
            'description': self.description,
            'channel_title': self.channel_title,
            'channel_id': self.channel_id,
            'thumbnail': self.thumbnail,
            'published_at': self.published_at,
            'published_time': self.published_time
        }
