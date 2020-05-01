from apps import db
from flask_restful import fields


class UserMedicalRecords(db.Model):
    """Class for storing information about informations of user medical record table

    Attributes:
        __tablename__: a string of table name
        id: an integer of user medical record's id
        order_id: an integer of user's id.
        user_id: an integer of user's id.
        provider_id: an integer of provider's id.
        subjective: a string that shows the subjective of User Medical Record.
        objective: a string that shows the objective of User Medical Record.
        assessment: a string that shows the assessment of User Medical Record.
        planning: a string that shows the planning of User Medical Record.
        date: a string that shows the date that order have been held.
        signature: a string that shows the signature of the provider (midwife).
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "user_medical_records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable = False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable = False)
    subjective = db.Column(db.String(1000), nullable=True)
    objective = db.Column(db.String(1000), nullable=True)
    assessment = db.Column(db.String(1000), nullable=True)
    planning = db.Column(db.String(1000), nullable=True)
    date = db.Column(db.String(30), nullable=False)
    signature = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'user_id': fields.Integer,
        'service_id': fields.Integer,
        'order_id': fields.Integer,
        'subjective': fields.String,
        'objective': fields.String,
        'assessment': fields.String,
        'planning': fields.String,
        'date': fields.String,
        'signature': fields.String,
    }

    def __init__(self, data):
        """Inits Order Details with data that user inputted

        The data already validated on the resources function

        Args:
                order_id: an integer of user's id.
                user_id: an integer of user's id.
                provider_id: an integer of provider's id.
                subjective: a string that shows the subjective of User Medical Record.
                objective: a string that shows the objective of User Medical Record.
                assessment: a string that shows the assessment of User Medical Record.
                planning: a string that shows the planning of User Medical Record.
                date: a string that shows the date that order have been held.
                signature: a string that shows the signature of the provider (midwife).
        """
        self.user_id = data['user_id']
        self.order_id = data['service_id']
        self.provider_id = data['provider_id']
        self.subjective = data['subjective']
        self.objective = data['objective']
        self.assessment = data['assessment']
        self.planning = data['planning']
        self.date = data['date']
        self.signature = data['signature']

