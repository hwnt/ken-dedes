from apps import db
from flask_restful import fields
from datetime import date


class Providers(db.Model):
    """Class for storing information about providers table

    Attributes:
        __tablename__: a string of table name
        id: an integer of provider's id
        user_id: a string of provider's user id
        name: a string of provider's name
        birthday: a string of provider's birthday
        experience: a string of provider's experience year/
        almamater: a string of provider's almamater.
        details: a string that explain details.
        role: a string that indicates provider role. such as: doctor, midwife, etc.
        permit_number: a string that shows the provider's legality of permission.
        created_at: a datetime that indicates when the account created
        updated_at: a datetime that indicates when the account last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "providers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(30), nullable=False)
    experience = db.Column(db.String(30), nullable=False)
    almamater = db.Column(db.String(30), nullable=False)
    details = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    permit_number = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'name': fields.String,
        'birthday': fields.String,
        'experience': fields.String,
        'almamater': fields.String,
        'details': fields.String,
        'role': fields.String,
        'permit_number': fields.String,
    }

    def __init__(self, data):
        """Inits Providers with data that user/admin inputted

        The data already validated on the resources function

        Args:
                user_id: a string of provider's user id
                name: a string of provider's name
                birthday: a string of provider's birthday
                experience: a string of provider's experience year/
                almamater: a string of provider's almamater.
                details: a string that explain details.
                role: a string that indicates user role. such as: doctor, midwife, etc.
                permit_number: a string that shows the provider's legality of permission.
        """
        self.user_id = data['user_id']
        self.name = data['name']
        self.birthday = data['birthday']
        self.experience = data['experience']
        self.almamater = data['almamater']
        self.details = data['details']
        self.role = data['role']
        self.permit_number = data['permit_number'] 