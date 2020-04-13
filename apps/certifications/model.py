from apps import db
from flask_restful import fields


class Certifications(db.Model):
    """Class for storing information about certifications table

    Attributes:
        __tablename__: a string of table name
        id: an integer of certification's id
        name: a string of certification's name
        issuer: a string of issuer who issued the certification.
        details: a string that explains the certification.
        created_at: a datetime that indicates when the certification created
        updated_at: a datetime that indicates when the certification last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "certifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    issuer = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'issuer': fields.String,
        'details': fields.String,
    }

    def __init__(self, data):
        """Inits Users with data that user inputted

        The data already validated on the resources function

        Args:
            name: a string of certification's name
            issuer: a string of issuer who issued the certification.
            details: a string that explains the certification.
        """
        self.name = data['name']
        self.issuer = data['issuer']
        self.details = data['details']
