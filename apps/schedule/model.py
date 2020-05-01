from apps import db
from flask_restful import fields


class Schedules(db.Model):
    """Class for storing information about informations of schedule of provider table

    Attributes:
        __tablename__: a string of table name
        id: an integer of order's id
        provider_id: an integer of provider's id.
        day: a string that shows the day of a provider is AVAILABLE/NOT (depends on status).
        date: a string that shows the date of a provider is AVAILABLE/NOT (depends on status).
        time_start: an integer that indicates the time of the day start.
        time_end: an integer that indicates the time of the day end.
        status: an integer that indicate the status of schedule.
        info: a string that indicate any info of schedules.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable = False)
    day = db.Column(db.String(30), nullable=True)
    date = db.Column(db.String(30), nullable=True)
    time_start = db.Column(db.String(30), nullable=False)
    time_end = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    info = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'provider_id': fields.Integer,
        'day': fields.String,
        'date': fields.String,
        'time_start': fields.String,
        'time_end': fields.String,
        'status': fields.Integer,
        'info': fields.String,
    }

    def __init__(self, data):
        """Inits Schedules with data that user inputted

        The data already validated on the resources function

        Args:
                provider_id: an integer of provider's id.
                day: a string that shows the day of a provider is AVAILABLE/NOT (depends on status).
                date: a string that shows the date of a provider is AVAILABLE/NOT (depends on status).
                time_start: an integer that indicates the time of the day start.
                time_end: an integer that indicates the time of the day end.
                status: an integer that indicate the status of schedule.
                info: a string that indicate any info of schedules.
        """
        self.provider_id = data['provider_id']
        self.day = data['day']
        self.date = data['date']
        self.time_start = data['time_start']
        self.time_end = data['time_end']
        self.status = data['status']
        self.info = data['info']
