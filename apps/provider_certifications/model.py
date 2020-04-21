from apps import db
from flask_restful import fields


class ProviderCertifications(db.Model):
    """Class for storing information about certifications of providers table

    Attributes:
        __tablename__: a string of table name
        id: an integer of certifications of provider's id
        certification_id: an integer of a certification's id.
        provider_id: an integer that provider's id.
        certification_number: a string that explain the certification number.
        date_issued: a date that indicates the date of the certificate issued.
        date_expired: a date that indicated the date of the certificate expired.
        details: a string that explains the certification.
        created_at: a datetime that indicates when the row created
        updated_at: a datetime that indicates when the row last updated
        response_field: a dictionary that will be used to be a guide when extracting data from database's field
    """
    __tablename__ = "provider_certifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    certification_id = db.Column(db.Integer, db.ForeignKey('certifications.id'), nullable = False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable = False)
    certification_number = db.Column(db.String(100), nullable=True)
    date_issued = db.Column(db.Date, nullable=True)
    date_expired = db.Column(db.Date, nullable=True)
    details = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    response_fields = {
        'id': fields.Integer,
        'certification_id': fields.Integer,
        'provider_id': fields.Integer,
        'certifcitaion_number': fields.String,
        'date_issued': fields.DateTime,
        'date_expired': fields.DateTime,
        'details': fields.String,
    }

    def __init__(self, data):
        """Inits ProviderCertifications with data that user inputted

        The data already validated on the resources function

        Args:
                certification_id: an integer of a certification's id.
                provider_id: an integer that provider's id.
                certification_number: a string that explain the certification number.
                date_issued: a date that indicates the date of the certificate issued.
                date_expired: a date that indicated the date of the certificate expired.
                details: a string that explains the certification.
        """
        self.certification_id = data['certification_id']
        self.provider_id = data['provider_id']
        self.certification_number = data['certification_number']
        self.date_issued = data['date_issued']
        self.date_expired = data['date_expired']
        self.details = data['details']
