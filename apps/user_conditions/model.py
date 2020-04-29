from apps import db
from flask_restful import fields


class UserConditions(db.Model):
    """Class for storing information about conditions of users table

    Attributes:
        __tablename__: a string of table name
        id: an integer of certifications of provider's id
        user_id: an integer of a user's id.
        condition_id: an integer that condition's id.
        condition: a string that indicate the term of a condition.
        condition_details: a string that explain the condition.
        user_answer: a string that explain the user answer of a condition.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "user_conditions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), nullable = False)
    condition = db.Column(db.String(100), nullable=True)
    condition_details = db.Column(db.String(100), nullable=True)
    user_answer = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'condition_id': fields.Integer,
        'condition': fields.String,
        'condition_detail': fields.String,
        'user_answer': fields.String,
    }

    def __init__(self, data):
        """Inits UserConditions with data that user inputted

        The data already validated on the resources function

        Args:
                user_id: an integer of a user's id.
                condition_id: an integer that condition's id.
                condition: a string that indicate the term of a condition.
                condition_details: a string that explain the condition.
                user_answer: a string that explain the user answer of a condition.
        """
        self.user_id = data['user_id']
        self.condition_id = data['condition_id']
        self.condition = data['condition']
        self.condition_details = data['condition_details']
        self.user_answer = data['user_answer']
