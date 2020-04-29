from apps import db
from flask_restful import fields


class Categories(db.Model):
    """Class for storing information about category table

    Attributes:
        __tablename__: a string of table name
        id: an integer of category's id
        name: a string of a name.
        details: a string that explain details.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'details': fields.String,
    }

    def __init__(self, data):
        """Inits Categories with data that user/admin inputted

        The data already validated on the resources function

        Args:
                name   : a string of a name.
                details: a string that explain details.
        """
        self.name = data['name']
        self.details = data['details']

