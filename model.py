from flask import Flask,jsonify,request
import requests
from flask_restful import Resource, Api
import json
from pymemcache.client import base
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)
CORS(application)
api = Api(application)

# Database for development
# application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/dastp_mw_dev'

# Database for QA
# application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/dastp_mw_qa'

# Database for Production MG Server
# application.config['SQLALCHEMY_DATABASE_URI']='mysql://mgonlinedb:Mgudb1122@mgu-online.cgtqmgscafyc.ap-south-1.rds.amazonaws.com/dastp_mw'

# Database for Production kerala university demo
application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/kem_dasp_mw'


application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(application)


############################# MODEL FILE ###################################
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    reg_date=db.Column(db.Date,nullable=True)
    trans_id=db.Column(db.String(200),nullable=True)
    exp_date=db.Column(db.Date,nullable=True)
    trans_req_id=db.Column(db.String(200),nullable=True)
    status=db.Column(db.String(200),default=0)

class Session(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    dev_type=db.Column(db.String(1),nullable=True)
    session_token=db.Column(db.String(200),nullable=False,unique=True)
    exp_time=db.Column(db.DateTime,nullable=False)
    IP=db.Column(db.String(256),nullable=False)
    MAC=db.Column(db.String(256),nullable=False)

class teacher(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(100),nullable=True)
    lname=db.Column(db.String(100),nullable=True)
    description=db.Column(db.String(200),nullable=True)
    status=db.Column(db.String(100),nullable=True)
    emailid=db.Column(db.String(200),nullable=True)
    resumepath=db.Column(db.String(500),nullable=True)
    phno=db.Column(db.String(100),nullable=True)

class UserProfile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    fname=db.Column(db.String(100),nullable=False)
    lname=db.Column(db.String(100),nullable=False)
    fullname=db.Column(db.String(300),nullable=True)
    phno=db.Column(db.String(100),nullable=True)
    gender=db.Column(db.String(20),nullable=True)
    photo=db.Column(db.String(100),nullable=True)
    padd1=db.Column(db.String(200),nullable=True)
    padd2=db.Column(db.String(200),nullable=True)
    pcity=db.Column(db.String(200),nullable=True)
    pstate=db.Column(db.String(200),nullable=True)
    pcountry=db.Column(db.String(200),nullable=True)
    ppincode=db.Column(db.String(200),nullable=True)
    madd1=db.Column(db.String(200),nullable=True)
    madd2=db.Column(db.String(200),nullable=True)
    mcity=db.Column(db.String(200),nullable=True)
    mstate=db.Column(db.String(200),nullable=True)
    mcountry=db.Column(db.String(200),nullable=True)
    mpincode=db.Column(db.String(200),nullable=True)
    religion=db.Column(db.String(200),nullable=True)
    caste=db.Column(db.String(200),nullable=True)
    nationality=db.Column(db.String(200),nullable=True)
    dob=db.Column(db.DateTime,nullable=True)
    s_caste=db.Column(db.String(200),nullable=True)
    annualincome=db.Column(db.String(100),nullable=True)
    aadhar=db.Column(db.String(50),nullable=True)

class Qualification(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('user_profile.id'),nullable=False)
    qualificationtype=db.Column(db.String(100),nullable=True)
    stream=db.Column(db.String(100),nullable=True)
    collegename=db.Column(db.String(500),nullable=True)
    boarduniversity=db.Column(db.String(100),nullable=True)
    yearofpassout=db.Column(db.Integer,nullable=True)
    percentage=db.Column(db.String(6),nullable=True)
    cgpa=db.Column(db.String(6),nullable=True)
    description=db.Column(db.String(500),nullable=True)
    qualificationlevel=db.Column(db.Integer,nullable=True)
    q_class=db.Column(db.String(45),nullable=True)
    grade=db.Column(db.String(45),nullable=True)
    types=db.Column(db.String(100),nullable=True)

class Transactiontable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    gateway=db.Column(db.String(100),nullable=True)
    gateway_id=db.Column(db.Integer,nullable=True)
    amount=db.Column(db.Integer,nullable=True)
    service_charge=db.Column(db.Integer,nullable=True)
    payment_time=db.Column(db.Time,nullable=True)
    bank_reference=db.Column(db.String(100),nullable=True)
    payment_status=db.Column(db.String(100),nullable=True)
    application_no=db.Column(db.Integer,nullable=True)
    bankname=db.Column(db.String(500),nullable=True)
    discriminator=db.Column(db.String(500),nullable=True)
    description=db.Column(db.String(500),nullable=True)
    purpose=db.Column(db.String(100),nullable=True)


class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(100),nullable=False)
    role_type=db.Column(db.String(100),nullable=False)


class Permission(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    API_name=db.Column(db.String(100),nullable=False)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=False)
    permissionname=db.Column(db.String(100),nullable=False)


class RoleMapping(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


class Universities(db.Model):    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(600),nullable=True)
    pid=db.Column(db.Integer,nullable=True)

class TeacherCourseMapping(db.Model):    
    tc_id=db.Column(db.Integer,primary_key=True)
    teacher_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    course_id=db.Column(db.Integer,nullable=False)
    batch_id=db.Column(db.Integer,nullable=True)

class UserExtTokenMapping(db.Model):    
    uem_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    email_id=db.Column(db.String(100),nullable=False)
    ext_token=db.Column(db.String(1000),nullable=True)
    batch_id=db.Column(db.Integer,nullable=True)
    status=db.Column(db.String(100),default=0)

class LmsCourseMapping(db.Model):    
    lcm_id=db.Column(db.Integer,primary_key=True)
    course_id=db.Column(db.Integer,nullable=False)
    lms_c_id=db.Column(db.String(100),nullable=False)


# class PaymentHistory(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     user_id=db.Column(db.Integer,nullable=True)
#     prgm_id=db.Column(db.Integer,nullable=True)
#     applicant_no=db.Column(db.Integer,nullable=True)
#     order_id=db.Column(db.String(100),nullable=True)
#     trans_id=db.Column(db.String(100),nullable=True)
#     trans_amount=db.Column(db.Integer,nullable=True)
#     trans_date=db.Column(db.DateTime,nullable=False)
#     res_code=db.Column(db.String(100),nullable=True)
#     status=db.Column(db.String(100),nullable=True)

    
 
# class AuditLog(db.Model):
#     __tablename__ = 'tbl_auditlog'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     created_on = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow)
#     modified_on = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
#     table_name= db.Column(db.String(255), nullable=False)
#     operation = db.Column(db.Enum('INSERT', 'DELETE', 'UPDATE'))
#     user_id = db.Column(db.Integer)