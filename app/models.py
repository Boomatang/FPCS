"""
This module holds the database models that are going to be used

There is a reason to have machine class and a log file for them machines, 
but as I do not know what information that would be required to be logged this has been left out for now.

"""
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager
# link tables
labour_skills = db.Table('labour_skills',
                         db.Column('labour_force.id', db.Integer, db.ForeignKey('labour_force.id')),
                         db.Column('skills.id', db.Integer, db.ForeignKey('skills.id')))

company_contacts = db.Table('company_contacts',
                            db.Column('companies.id', db.Integer, db.ForeignKey('companies.id')),
                            db.Column('contacts.id', db.Integer, db.ForeignKey('contacts.id')))


class Permission:
    """
    Currenty the max number of roles that can be created is 8,
    ADMINISTER most be the highist level
    """
    LOOK = 0x01
    SALES = 0x02
    PLANNING = 0x04
    RWC = 0x08
    ADMINISTER = 0x80


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


class Project(db.Model):
    """
    The projects are top level jobs. All projects will have a least one job.
    This one job will always have the value of '01'. Will the project will have a key made from the year+month+job number. 
    That job key might not be used as the primary key as a project for tender would not have the job number section.
    
    The number value is the number that of that project in a year and this is rest every year
    
    The status value will be similiar to the permission system
    
    The active can only be set to default when all the sub jobs are set to false.
    """
    
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    number = db.Column(db.Integer)
    due_date = db.Column(db.DateTime)
    entry_date = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    status = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    location = db.Column(db.String) #  This may need to be an address function
    
    
    company = db.Column(db.Integer, db.ForeignKey('companies.id'))
    contact = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    jobs = db.relationship('Job', backref='project', lazy='dynamic')
    
    @property
    def project_number(self):
        """
        This builds the project number in the format yyyy-mm-##
        The leading zeros are added to the month if required
        An exampe is 2016-05-167
        """
        
    def convert_number(self, number):
        """
        This function will convert a string based project number back to its basic elements.
        """
    
    def __repr__(self):
        return "<ID: %r, Project Number: %r>" % (self.id, self.project_number)


class TimeLog(db.Model):
    """
    A log of the time that a Labour does to a job. 
    This would not be the working hours for the Labour force only the time to the jobs and not slack time.
    Also this time log is of the hours worked not the start to end time. 
    If starting and end time is required some kind of interface needs to be set up to allow the labour force login to set their own times
    
    Question does there need to be an entry method to allow time been given to the entire project and not just one job.
    """

    __tablename__ = 'time_log'

    labour_id = db.Column(db.Integer, db.ForeignKey('labour_force.id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    time = db.Column(db.DateTime())


class Job(db.Model):
    """
    The Job class will be the sub elements that make up the Project class.
    These will share information with the the other jobs in the project but should be able to stand indepentent of other jobs
    
    The number value is the number which is a sub part of the job number.
    An example of this is 2016-05-167-03 <- the last 03 is the number value.
    
    
    The active is if the job has not been complete or taken of the books. 
    A job been tendered would still be active
    
    For the status value I am thinking some thing like how the permissions are done.
    
    """
    
    __tablename__ = "jobs"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    number = db.Column(db.Integer) #  This is the number given in order o the project
    due_date = db.Column(db.DateTime)
    enrty_date = db.Column(db.DateTime, default=datetime.utcnow())
    quantity = db.Column(db.Integer)
    exexution = db.Column(db.String) 
    structural = db.Column(db.Boolean)
    active = db.Column(db.Boolean, default=True)
    status = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))
    
    
    @property
    def job_number(self):
        """
        This function returns a job number that is formated in the manner that is required.
        If the project has only one job then the project number is return aka 2016-05-167
        else the full number is returned 2016-05-167-03
        """
        
    def convert_number(self, number):
        """
        This function will convert a string based job number back to its basic elements.
        It does allow for input of 2016-05-167 and 2016-05-167-03
        """

    def __repr__(self):
        return "<ID: %r, Job Number: %r>" % (self.id, self.job_number)

class Company(db.Model):
    """
    The Company is the client Companies and this should be used for an address book type system.
    A company will have contacts but a company can be set up with out any contacts.
    """

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    main_contact = db.Column(db.Integer)  # links to a Contact.id
    default_email = db.Column(db.String)
    default_phone_1 = db.Column(db.String)
    default_phone_2 = db.Column(db.String)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    address_city = db.Column(db.String)
    address_county = db.Column(db.String)
    address_country = db.Column(db.String)
    address_postcode = db.Column(db.String)

    contact = db.relationship('Contact', secondary=company_contacts,
                              backref=db.backref('company', lazy='dynamic'))
    projects = db.relationship('Porject', backref='company', lazy='dynamic')

    def __repr__(self):
        return "<Company: %r>" % self.name


class Contact(db.Model):
    """
    Every company can have a contact. A contact does not need to be part of any company.
    This is like an address book
    """

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    position = db.Column(db.String)  # may need to allow for multi
    mobile = db.Column(db.String)  # may need to allow for multi
    land_line = db.Column(db.String)  # may need to allow for multi
    email = db.Column(db.String)  # may need to allow for multi
    entry_date = db.Column(db.DateTime(), default=datetime.utcnow)
    last_contacted = db.Column(db.DateTime())
    
    
    projects = db.relationship('Porject', backref='contact', lazy='dynamic')

    def __repr__(self):
        return "<Contact %r: %r %r>" % (self.id, self.first_name, self.last_name)


class Labour(db.Model):
    """
    This is a list of the worker that can be used on jobs. A Labour worker does not need to be part of the User class.
    The Skill class will be liked to each person in the Labour.
    
    The hourly rate is used over having a sarly to make it easier to calulate values later
    """

    __tablename__ = 'labour_force'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    position = db.Column(db.String)  # may need to allow for multi
    mobile = db.Column(db.String)  # may need to allow for multi
    land_line = db.Column(db.String)  # may need to allow for multi
    email = db.Column(db.String)  # may need to allow for multi
    entry_date = db.Column(db.DateTime(), default=datetime.utcnow)

    skill = db.relationship('Skill', secondary=labour_skills,
                            backref=db.backref('labour', lazy='dynamic'))

    def __repr__(self):
        return "<Labour %r: %r %r>" % (self.id, self.first_name, self.last_name)


class Skill(db.Model):
    """
    Holds the types of skills that the Labour has.
    This is used to help with the planning of time for jobs.
    
    
    Here the value is the level to which the skill is worth to the company
    The difficulty is how hard it is regard to carry out that skill
    """

    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    value = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)

    def __repr__(self):
        return "<Skill: %r>" % self.name


class Material():
    """
    A list of materials that can be ordered.
    This should cover raw materials and machine consumables
    """


class AnonymousUser(AnonymousUserMixin):
    """
    This class should never be needed but can't hurt to have in place from the start
    """

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    This function is required by the login manger to load users into the session
    """
    return User.query.get(int(user_id))
