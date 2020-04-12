from apps import db
from flask_restful import fields


class Conditions(db.Model):
    """Class for storing information about conditions table

    Attributes:
        __tablename__: a string of table name
        id: an integer of condition's id
        condition: a string of a condition.
        details: a string that explain details.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "conditions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'condition': fields.String,
        'details': fields.String,
    }

    def __init__(self, data):
        """Inits Conditions with data that user/admin inputted

        The data already validated on the resources function

        Args:
                id: an integer of condition's id
                condition: a string of a condition.
                details: a string that explain details.
        """
        self.condition = data['condition']
        self.details = data['details']

