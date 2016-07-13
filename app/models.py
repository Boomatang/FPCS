"""
This module holds the database models that are going to be used

There is a reason to have machine class and a log file for them machines, but as I do not know what information that would be required to be logged this has been left out for now.

"""
from datetime import datetime
from flask_login import UserMixin

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """
    The class for the system users
    A User wilkl most likly be part of the Labour class. This is not clear as of yet.
    
    All the informationis the basic that is need to use the flask login manger
    """
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    signup_date = db.Column(db.Date)
    confirmed = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return "<User %s, %s>" % (self.ID, self.username)
    
    
    
class Project():
    """
    The projects are top level jobs. All projects will have a least one job.
    This one job will always have the value of '01'. Will the project will have a key made from the year+month+job number. 
    That job key might not be used as the primary key as a project for tender would not have the job number section.
    """
    
class Job():
    """
    The Job class will be the sub elements that make up the Project class.
    These will share information with the the other jobs in the project but should be able to stand indepentent of other jobs
    """
    
class Company():
    """
    The Company is the client Companies and this should be used for an address book type system.
    A company will have contacts but a company can be set up with out any contacts.
    """
    
class Contact():
    """
    Every company can have a contact. A contact does not need to be part of any company.
    This is like an address book
    """
    
class Labour():
    """
    This is a list of the worker that can be used on jobs. A Labour worker does not need to be part of the User class.
    The Skill class will be liked to each person in the Labour.
    """
    
class Skill():
    """
    Holds the types of skills that the Labour has.
    This is used to help with the planning of time for jobs.
    """
    
class TimeLog():
    """
    A log of the time that a Labour does to a job. 
    This would not be the working hours for the Labour force only the time to the jobs and not slack time.
    """
    
class Material():
    """
    A list of materials that can be ordered.
    This should cover raw materials and machine consumables
    """

@login_manager.user_loader
def load_user(user_id):
    """
    This function is required by the login manger to load users into the session
    """
    return User.query.get(int(user_id))
