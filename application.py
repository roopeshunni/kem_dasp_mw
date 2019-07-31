from flask import Flask,jsonify,request
import requests
from flask_restful import Resource, Api
import json
from pymemcache.client import base
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import ast
import redis
from cachetools import cached, LRUCache, TTLCache
from urls_list import *
from constants import *
from random import randint
import smtplib,ssl
from  datetime import datetime,timedelta
from secrets import token_urlsafe
import os
import hashlib,hmac
import base64
import uuid
import ast
import random
from passlib.hash import pbkdf2_sha256
import string
import time
from lms import *
from sqlalchemy import or_
from model import *


# application = Flask(__name__)
# CORS(application)
# api = Api(application)

# # Database for development
application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/dastp_mw_dev'

# # Database for QA
# # application.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root1234@dastp.cq9dav1ixlfr.ap-southeast-1.rds.amazonaws.com/dastp_mw_qa'

# # Database for Production MG Server
# # application.config['SQLALCHEMY_DATABASE_URI']='mysql://mgonlinedb:Mgudb1122@mgu-online.cgtqmgscafyc.ap-south-1.rds.amazonaws.com/dastp_mw'


# application.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# db=SQLAlchemy(application)

cache=TTLCache(1024,86400)
faqcache=TTLCache(1024,86400)
programcache=TTLCache(1024,86400)
singleprogramcache=TTLCache(1024,86400)
cachequestion=TTLCache(1024,86400)
upcomingprogramcache=TTLCache(1024,86400)
ongoingprogramcache=TTLCache(1024,86400)


# ############################# MODEL FILE ###################################
# class User(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     email=db.Column(db.String(200),unique=True,nullable=False)
#     password=db.Column(db.String(200),nullable=False)
#     reg_date=db.Column(db.Date,nullable=True)
#     trans_id=db.Column(db.String(200),nullable=True)
#     exp_date=db.Column(db.Date,nullable=True)
#     trans_req_id=db.Column(db.String(200),nullable=True)
#     status=db.Column(db.String(200),default=0)

# class Session(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     dev_type=db.Column(db.String(1),nullable=True)
#     session_token=db.Column(db.String(200),nullable=False,unique=True)
#     exp_time=db.Column(db.DateTime,nullable=False)
#     IP=db.Column(db.String(256),nullable=False)
#     MAC=db.Column(db.String(256),nullable=False)

# class teacher(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     fname=db.Column(db.String(100),nullable=True)
#     lname=db.Column(db.String(100),nullable=True)
#     description=db.Column(db.String(200),nullable=True)
#     status=db.Column(db.String(100),nullable=True)
#     emailid=db.Column(db.String(200),nullable=True)
#     resumepath=db.Column(db.String(500),nullable=True)
#     phno=db.Column(db.String(100),nullable=True)

# class UserProfile(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     fname=db.Column(db.String(100),nullable=False)
#     lname=db.Column(db.String(100),nullable=False)
#     fullname=db.Column(db.String(300),nullable=True)
#     phno=db.Column(db.String(100),nullable=True)
#     gender=db.Column(db.String(20),nullable=True)
#     photo=db.Column(db.String(100),nullable=True)
#     padd1=db.Column(db.String(200),nullable=True)
#     padd2=db.Column(db.String(200),nullable=True)
#     pcity=db.Column(db.String(200),nullable=True)
#     pstate=db.Column(db.String(200),nullable=True)
#     pcountry=db.Column(db.String(200),nullable=True)
#     ppincode=db.Column(db.String(200),nullable=True)
#     madd1=db.Column(db.String(200),nullable=True)
#     madd2=db.Column(db.String(200),nullable=True)
#     mcity=db.Column(db.String(200),nullable=True)
#     mstate=db.Column(db.String(200),nullable=True)
#     mcountry=db.Column(db.String(200),nullable=True)
#     mpincode=db.Column(db.String(200),nullable=True)
#     religion=db.Column(db.String(200),nullable=True)
#     caste=db.Column(db.String(200),nullable=True)
#     nationality=db.Column(db.String(200),nullable=True)
#     dob=db.Column(db.DateTime,nullable=True)
#     s_caste=db.Column(db.String(200),nullable=True)
#     annualincome=db.Column(db.String(100),nullable=True)
#     aadhar=db.Column(db.String(50),nullable=True)

# class Qualification(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     pid=db.Column(db.Integer,db.ForeignKey('user_profile.id'),nullable=False)
#     qualificationtype=db.Column(db.String(100),nullable=True)
#     stream=db.Column(db.String(100),nullable=True)
#     collegename=db.Column(db.String(500),nullable=True)
#     boarduniversity=db.Column(db.String(100),nullable=True)
#     yearofpassout=db.Column(db.Integer,nullable=True)
#     percentage=db.Column(db.String(6),nullable=True)
#     cgpa=db.Column(db.String(6),nullable=True)
#     description=db.Column(db.String(500),nullable=True)
#     qualificationlevel=db.Column(db.Integer,nullable=True)
#     q_class=db.Column(db.String(45),nullable=True)
#     grade=db.Column(db.String(45),nullable=True)
#     types=db.Column(db.String(100),nullable=True)

# class Transactiontable(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     gateway=db.Column(db.String(100),nullable=True)
#     gateway_id=db.Column(db.Integer,nullable=True)
#     amount=db.Column(db.Integer,nullable=True)
#     service_charge=db.Column(db.Integer,nullable=True)
#     payment_time=db.Column(db.Time,nullable=True)
#     bank_reference=db.Column(db.String(100),nullable=True)
#     payment_status=db.Column(db.String(100),nullable=True)
#     application_no=db.Column(db.Integer,nullable=True)
#     bankname=db.Column(db.String(500),nullable=True)
#     discriminator=db.Column(db.String(500),nullable=True)
#     description=db.Column(db.String(500),nullable=True)
#     purpose=db.Column(db.String(100),nullable=True)


# class Role(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     role_name=db.Column(db.String(100),nullable=False)
#     role_type=db.Column(db.String(100),nullable=False)


# class Permission(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     API_name=db.Column(db.String(100),nullable=False)
#     role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=False)
#     permissionname=db.Column(db.String(100),nullable=False)


# class RoleMapping(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     role_id=db.Column(db.Integer,db.ForeignKey('role.id'),nullable=False)
#     user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


# class Universities(db.Model):    
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(600),nullable=True)
#     pid=db.Column(db.Integer,nullable=True)

# class TeacherCourseMapping(db.Model):    
#     tc_id=db.Column(db.Integer,primary_key=True)
#     teacher_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     course_id=db.Column(db.Integer,nullable=False)
#     batch_id=db.Column(db.Integer,nullable=True)

# class UserExtTokenMapping(db.Model):    
#     uem_id=db.Column(db.Integer,primary_key=True)
#     user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     email_id=db.Column(db.String(100),nullable=False)
#     ext_token=db.Column(db.String(1000),nullable=True)

# class LmsCourseMapping(db.Model):    
#     lcm_id=db.Column(db.Integer,primary_key=True)
#     course_id=db.Column(db.Integer,nullable=False)
#     lms_c_id=db.Column(db.String(100),nullable=False)


# # class PaymentHistory(db.Model):
# #     id=db.Column(db.Integer,primary_key=True)
# #     user_id=db.Column(db.Integer,nullable=True)
# #     prgm_id=db.Column(db.Integer,nullable=True)
# #     applicant_no=db.Column(db.Integer,nullable=True)
# #     order_id=db.Column(db.String(100),nullable=True)
# #     trans_id=db.Column(db.String(100),nullable=True)
# #     trans_amount=db.Column(db.Integer,nullable=True)
# #     trans_date=db.Column(db.DateTime,nullable=False)
# #     res_code=db.Column(db.String(100),nullable=True)
# #     status=db.Column(db.String(100),nullable=True)

    
 
# # class AuditLog(db.Model):
# #     __tablename__ = 'tbl_auditlog'
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer)
# #     created_on = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow)
# #     modified_on = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
# #     table_name= db.Column(db.String(255), nullable=False)
# #     operation = db.Column(db.Enum('INSERT', 'DELETE', 'UPDATE'))
# #     user_id = db.Column(db.Integer)

############################# API Gateway###################################

# def my_after_insert_listener(mapper, connection, target):
#     data = target.__dict__.copy()
#     # print(data)
#     table_name = target.__tablename__
#     data['user_id'] = data.get('id')
#     data['operation'] = 'INSERT'
#     data['table_name'] = table_name
#     #data['id'] = None
#     #log_name = table_name + '_log'
#     log_name='tbl_user_log'
#     print(log_name)
#     auditexecute(log_name, data)


# def auditexecute(log_name, data):
#     print("gg")
#     print(data)
#     for c in db.Model._decl_class_registry.values():
#         if hasattr(c, '__tablename__') and c.__tablename__ == log_name:
           
#             db.session.execute(c.__table__.insert(), data) 

class GetFAQ(Resource):
    def get(self):
        try:
            response = requests.get(faq_api)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except:
            return jsonify(error)



class GetAllEvent(Resource):
    def get(self):
        cache_result=get_all_events()
        DataResponse=json.loads(cache_result.text)
        if(DataResponse.get("status")!=200):
            cache.clear()
            return jsonify(error)
        allevents=DataResponse.get('message').get('events')
        return {"status":200,"message":allevents}


def get_all_events():
    allcalendarData = requests.get(get_all_events_backendapi )      
    return allcalendarData

#  Programmes API Single and all
# class ProgramApiParticularId(Resource):
#     def post(self):
def ProgramApiParticularId(data):
            if 'id' in data:
                a=data.get("id")  
                dtype=data.get("dtype") 
                singleProgrammeData=get_single_programme(a,dtype)                              
                singleProgrammeDataResponse=json.loads(singleProgrammeData.text)                
                return singleProgrammeDataResponse 
            else:
                dtype=data.get("dtype") 
                homeData = get_programmes(dtype)
                homeDataResponse=json.loads(homeData.text)     
                return homeDataResponse   

class GetAllProgrammes(Resource):
    def post(self):
        try:
            data=request.get_json()
            response=ProgramApiParticularId(data)
            return jsonify(response)
        except:
            return jsonify(error)


class GetNews(Resource):
    def get(self):
        try:
            response = requests.get(news_api)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)

        except:
            return jsonify(error)

class GetActs(Resource):
    def get(self):
        try:
            response = requests.get(acts_api)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class GetCalendar(Resource):
    def get(self):
        try:
            response = requests.get(calendar_api)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class GetallCalendar(Resource):
    def get(self):
        try:
            
            response=allcalendar()            
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except:
            return jsonify(error)
class GetAchivements(Resource):
    def get(self):
        try:
            response = requests.get(achivements_api)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class GetAboutUs(Resource):
    def get(self):
        try:
            response = requests.get(aboutus_api)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class GetSearch(Resource):
    def post(self):
        try:            
            data=request.get_json()
            response_json_text=programmesearches(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

################################API GATEWAY####################################


################################MIDDLE WARE####################################

# Homescreen API
class HomeScreenApi(Resource):
    def get(self):
        try:            
            homeData=get_home()
            homeDataResponse=json.loads(homeData.text)
            # print(len(get_home.__dict__)) 
            # print(get_home.__dict__)          
            if(homeDataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            return jsonify(homeDataResponse)            
        except Exception as e:
            return jsonify(error)




def allcalendar():
    allcalendarData = requests.get(allcalendar_api )      
    return allcalendarData


# Caching the all programmes data
@cached(cache=programcache)
def get_programmes(dtype):                
    programmeData = requests.post(programme_api,json={"dtype":dtype} )   
    return programmeData

# Caching the single programme data based on programme id
@cached(cache=singleprogramcache)
def get_single_programme(pid,dtype):
    singleProgrammeData= requests.post(programme_api,json={"pid":pid,"dtype":dtype} )   
    return singleProgrammeData  

#  Calender API for Single month and particular day
class CalenderApi(Resource):
    def post(self):
           
            content=request.get_json()            
            a=content['id']                               
            homeData = requests.post(
            calenderapi,json={"pid":a})            
            homeDataResponse=json.loads(homeData.text) 
            return homeDataResponse        
        
    def get(self):              
            calenderData = requests.get(calenderapi)
            calenderDataResponse=json.loads(calenderData.text)
            return calenderDataResponse 

# Caching the home data
@cached(cache=cache)
def get_home():             
    homeData = requests.get(backend_home_api )    
    return homeData


@cached(cache=TTLCache(maxsize=1024, ttl=72000))
def info_token_fetch():
    response=requests.get(token_api)
    token=json.loads(response.text)['token']
    return token

# Achievments API
class AboutusApi(Resource):
    
    def get(self):
        try:
            cache_result=get_home()        
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)            
            aboutus=DataResponse.get('message').get('about')            
            return jsonify(aboutus)
        except:
            return jsonify(error)

# Achievments API
class Achievments(Resource):

    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            achievments=DataResponse.get('message').get('achievments')
            return jsonify(achievments)
        except:
            return jsonify(error)

# Acts and Regulations API
class Acts(Resource):
    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            acts=DataResponse.get('message').get('acts')
            return jsonify(acts)
        except:
            return jsonify(error)

# Announcements API
class Announcements(Resource):
    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            announcements=DataResponse.get('message').get('announcements')
            return jsonify(announcements)
        except:
            return jsonify(error)

# Directorate API
class Directorate(Resource):
    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            directorate=DataResponse.get('message').get('directorate')
            return jsonify(directorate)
        except:
            return jsonify(error)

# Notifications API
class Notifications(Resource):
    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            notifications=DataResponse.get('message').get('notifications')
            return jsonify(notifications)
        except:
            return jsonify(error)

# Research API
class Research(Resource):
    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            research=DataResponse.get('message').get('research')
            return jsonify(research)
        except:
            return jsonify(error)

# Sliders API
class Sliders(Resource):
    def get(self):
        try:
            cache_result=get_home()
            DataResponse=json.loads(cache_result.text)
            if(DataResponse.get("status")!=200):
                cache.clear()
                return jsonify(error)
            sliders=DataResponse.get('message').get('sliders')
            return jsonify(sliders)
        except:
            return jsonify(error)

# Studycenter API
class Studycenter(Resource):
    def post(self):
        try:
            data=request.get_json()
            session_id=data['session_id']
            user_id=data['user_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    cache_result=get_home()
                    DataResponse=json.loads(cache_result.text)
                    if(DataResponse.get("status")!=200):
                        cache.clear()
                        return jsonify(error)
                    studycenter=DataResponse.get('message').get('studycentre')
                    studycenterdict={"status":200,"message":studycenter}
                    return jsonify(studycenterdict)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)



# FAQ API
class FAQ(Resource):
    def get(self):
        try:
            cache_result=get_FAQ()
            DataResponse=json.loads(cache_result.text)
            # print(DataResponse)
            if(DataResponse.get("status")!=200):
                faqcache.clear()
                return jsonify(error)
            
            return jsonify(DataResponse)
        except Exception as e:
            return jsonify(error)
@cached(cache=faqcache)
def get_FAQ():
    allFaqData = requests.get(get_all_faq_backendapi )      
    return allFaqData


# COURSES LIST API
class GetCourses(Resource):
    def post(self):
        try:            
            data=request.get_json()
            response_json_text=programmecourses(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

def programmecourses(data):   
    prgid=data.get('prg_id')
    try:    
        homeData = requests.post(
        proramme_courses_api,json={"prg_id":prgid})
        homeDataResponse=json.loads(homeData.text)   
        return homeDataResponse
    except Exception as e:
        return homeDataResponse

#################################MIDDLE WARE####################################


#####################################################################
########                 User Management
#####################################################################

#######################GATEWAY#####################################
class GetRegisterUser(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=userregister(data)
            return response_json_text
        except:
            return jsonify(error)

class GetLogin(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=logins(data)
            
            return response_json_text
        except:
            return jsonify(error)

class GetProfileEditDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response=getprofile(data)
            return jsonify(response)
        except:
            return jsonify(error)


#####################################################################

# PROFILE EDIT --EDUCATIONAL DETAILS GET [ID] GATEWAY #

######################################################################

class Usereducationalqualification(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=geteducationid(data)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)

class GetProfileAddressDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=getaddress(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class GetEducationalDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=geteducationall(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class SubmitProfileEditDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=postprofile(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class SubmitProfileAddressDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=postaddress(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)
class SubmitEducationalDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=posteducation(data)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)

class DeleteEducationalDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=deleteeducation(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)    

class EditEducationalDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=editeducation(data)
            return jsonify(response_json_text)
        except Exception as e:
            print(e)
            return jsonify(error) 

class SendCodeForgotPassword(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=forgotcodesend(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)
        
class ForgotPassword(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=newpassword(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class ChangePasswordApiGateway(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=changepassword(data)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)

class VerifyEmail(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=verifyemails(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

class VerifyCode(Resource):
    def post(self):
        try:
            data=request.get_json() 
            response_json_text=emailcodeverification(data)     
            return jsonify(response_json_text)
        except:
            return jsonify(error)        

#######################GATEWAY#####################################


######################MIDDLEWARE#####################################
#### ADMIN MODULE START ##
class AdminLogin(Resource):
    def post(self):
        try:
            data=request.get_json()
            email=data['email']
            password=data['password']
            dev_type=data['dev_type']
            IP=data['IP']
            MAC=data['MAC']            
            try:   
                IP=get_my_ip()
                result=loginAdmin(email,password,dev_type,IP,IP)
                return jsonify(result)
            except Exception as e:
                return error
        except Exception as e:
                return error

class StudentBatchLists(Resource):
    def post(self):        
        try:   
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            batch_id=content["b_id"]
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=appliedlist(batch_id)
                    return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return error

class Applicants(Resource):
    def post(self):
        try:   
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    homeData = requests.get(
                    prgm_backendapi)
                    homeDataResponse=json.loads(homeData.text)
                    # response=applicants()
                    return jsonify(homeDataResponse)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return error

class AdmissionProgramBatch(Resource):
    def post(self):
        try:   
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            pid=content['pid']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=admissionprogrambatch(pid)
                    return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return error



           
def get_my_ip():
    return  request.remote_addr 
#### ADMIN MODULE END ##

def logins(data):
    try:
        
        email=data.get('email')
        password=data.get('password')
        dev_type=data.get('dev_type')
        IP=data.get('IP')
        MAC=data.get('MAC')
        print(MAC)
        if(email.strip()==""):
            return blankemail
        if(password.strip()==""):
            return blankpassword            
        try: 
            IP=get_my_ip()
            result=loginUser(email,password,dev_type,IP,IP)
            
            return jsonify(result)
        except Exception as e:

            return error
    except Exception as e:
            return error


def userregister(data):
        try:
            email=data.get("email")        
            password=data.get("password")       
            fname=data.get("fname")        
            lname=data.get("lname")      
            phone=data.get("phone")
            if (email.strip()==""):
                return blankemail
            if(password.strip()==""):
                return blankpassword        
            try:               
                result=registerUser(email,password,fname,lname,phone)
                return jsonify(result)
            except Exception as e:
                    return error
        except Exception as e:
            return error
####################
def programmesearches(data):
    a=data.get('keyword')
    dtype=data.get('dtype') 
    try:   
        homeData = requests.post(
        search_api_info,json={"keyword":a,"dtype":dtype})
        homeDataResponse=json.loads(homeData.text)
        
        return homeDataResponse
    except Exception as e:
        return homeDataResponse






################################################
#   FORGOT PASSWORD                            #
################################################
def forgotcodesend(data):
        emailid=data.get('emailid')          
        chk_user=User.query.filter_by(email=emailid).first()
        if chk_user!=None:
            number=cache_code(emailid)
            response=send_email(emailid,number)
            if response==0:
                return invalidemail
            else:
                return mailsent
        else:
            return invalidemail



#######################################################
#   FORGOT PASSWORD                                   #
#######################################################
def newpassword(data):
        emailid=data.get('emailid')
        password=data.get('password')
        code=data.get('code')
        chk_user=User.query.filter_by(email=emailid).first()
        if chk_user!=None:
            verify_code_data={"emailid":emailid,"code":code}
            code_response=emailcodeverification(verify_code_data)
            if(code_response.get("status")!=200):
                return emailcodeinvalid
            chk_user.password=password
            db.session.commit()
            return pwdupdated
        else:
            return invalidemail

#####################################################
#  CHANGE PASSWORD                                  #
#####################################################
def changepassword(data):
        emailid=data.get('emailid')
        oldpassword=data.get('oldpassword')
        password1=data.get('password')
        session_id=data.get('session_id')
        user_id=data.get('user_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=User.query.filter_by(email=emailid,password=oldpassword,id=user_id).first()
            if chk_user!=None:
                
                chk_user.password=password1
                chk_user.status="0"
                db.session.commit()
                return pwdupdated
            else:
                return invalidemail
        else:
            return session_invalid
            
#######################################################
#   EMAIL VERIFICATION MAIL                           #
#######################################################
def verifyemails(data):
        emailid=data.get('emailid')
        chk_user=User.query.filter_by(email=emailid).first()
        if chk_user==None:
            number=cache_code(emailid)
            response=send_email(emailid,number)
            if response==0:
                return invalidemail
            else:
                return mailsent
        else:
            return emailexist

#######################################################
#  SEND MAIL                                          #
#######################################################
# def send_email(username,u_id):
#     host='smtp.gmail.com'
#     port=587
#     email='dastpkefi@gmail.com'
#     password="sghsmidkrlxcarmo"
#     subject="Verification  "
#     mail_to=username
#     mail_from=email
#     body="YOUR VERIFICATION CODE IS {id}.".format(id=u_id)
#     message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
#     try:
#         server = smtplib.SMTP(host, port)
#         server.ehlo()
#         server.starttls()
#         server.login(email, password)
#         server.sendmail(mail_from, mail_to, message)
#         server.close()
#         return 1
#     except Exception as ex:
#         return 0

def send_email(username,u_id):
    # For production use enable the ssl server 
    # host='ssl://smtp.gmail.com'
    # port=465
    
    # For web staging
    host='smtp.gmail.com' 
    port=587

    email=mg_email
    password=mg_password
    context = ssl.create_default_context()
    subject="DASP Email Verification "
    mail_to=username
    mail_from=email
    body="Hi,\n\n YOUR EMAIL VERIFICATION CODE IS {id}.  \n \n Team DASP  \n\n\n\n THIS IS A SYSTEM GENERATED EMAIL - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL".format(id=u_id)
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()        
        server.starttls(context=context)
        server.ehlo()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0
#######################################################
#   EMAIL VERIFICATION MAIL                           #
#######################################################
def emailcodeverification(data):
        emailid=data.get('emailid')
        code=data.get('code')
        datas=cache_code(emailid)
        if datas != None:
            datas=int(datas)
        else:
            success=emailcodeexpired
            return success
        if datas==int(code):
            success=emailcodeverified            
        else:
            success=emailcodeinvalid
        return success

# Caching the verification code
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def cache_code(email_id):
    range_start = 10**(4-1)
    range_end = (10**4)-1
    return randint(range_start, range_end)

################################################################################
# PROFILE EDIT --PERSONAL DETAILS GET [from table to getway]                   #
################################################################################
def getprofile(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            personaldetails={"firstname":chk_user.fname,"lastname":chk_user.lname,
                            "full_name":chk_user.fullname,
                            "phonenumber":chk_user.phno,"gender":chk_user.gender,
                            "religion":chk_user.religion,"caste":chk_user.caste,
                            "nationality":chk_user.nationality,"dob":str(chk_user.dob),#due to error object of datetime is not json serialisable
                            "s_caste":chk_user.s_caste,"annualincome":chk_user.annualincome
                            }
            return personaldetails
        else:
            return session_invalid

##########################################################
# PROFILE EDIT --PERSONAL DETAILS  UPDATING              #
##########################################################
def postprofile(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        phonenumber=data.get('phonenumber')
        gender=data.get('gender')
        religion1=data.get('religion')
        full_name=data.get('fullname')
        caste1=data.get('caste')
        nationality1=data.get('nationality')
        s_caste=data.get('s_caste')
        annualincome1=data.get('annualincome')
        dob1=data.get('dob') 
        full=full_name.upper()    
        datetime_object=datetime.strptime(dob1, "%d/%m/%Y").date()
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            chk_user.fname=firstname
            chk_user.lname=lastname
            chk_user.phno=phonenumber
            chk_user.gender=gender
            chk_user.religion=religion1
            chk_user.fullname=full
            chk_user.caste=caste1
            chk_user.nationality=nationality1
            chk_user.s_caste=s_caste
            chk_user.annualincome=annualincome1
            chk_user.dob=datetime_object
            db.session.commit()
            return info_update
        else:
            return session_invalid

################################################################################
# PROFILE EDIT --ADDRESS DETAILS GET [from table to getway]                    #
################################################################################
def getaddress(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            personaldetails={
                "paddress1":chk_user.padd1,
                "paddress2":chk_user.padd2,"pcity":chk_user.pcity,
                "pstate":chk_user.pstate,"pcountry":chk_user.pcountry,
                "ppincode":chk_user.ppincode,"maddress1":chk_user.madd1,
                "maddress2":chk_user.madd2,"mcity":chk_user.mcity,
                "mstate":chk_user.mstate,"mcountry":chk_user.mcountry,
                "mpincode":chk_user.mpincode
            }
            return personaldetails
        else:
            return session_invalid

################################################################################
# PROFILE EDIT --PHOTO DETAILS GET [from table to getway]                    #
################################################################################
class GetPhotoDetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=getphoto(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

################################################################################
# PROFILE EDIT --PHOTO DETAILS POST [from gatway to table  ]                    #
################################################################################

class SubmitPhotodetails(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=postphoto(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)

##########################################################
# PROFILE EDIT --ADDRESS DETAILS  UPDATING               #
##########################################################
def postaddress(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        paddress1=data.get('paddress1')
        paddress2=data.get('paddress2')
        pcity=data.get('pcity')
        pcountry=data.get('pcountry')
        pstate=data.get('pstate')
        ppincode=data.get('ppincode')
        maddress1=data.get('maddress1')
        maddress2=data.get('maddress2')
        mcity=data.get('mcity')
        mcountry=data.get('mcountry')
        mstate=data.get('mstate')
        mpincode=data.get('mpincode')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            chk_user.padd1=paddress1
            chk_user.padd2=paddress2
            chk_user.pcity=pcity
            chk_user.pcountry=pcountry
            chk_user.pstate=pstate
            chk_user.ppincode=ppincode
            chk_user.madd1=maddress1
            chk_user.madd2=maddress2
            chk_user.mcountry=mcountry
            chk_user.mstate=mstate
            chk_user.mcity=mcity
            chk_user.mpincode=mpincode
            db.session.commit()
            return address_update
        else:
            return session_invalid

################################################################################
# PROFILE EDIT --EDUCATIONAL DETAILS GET [from table to getway]                #
################################################################################
def geteducationall(data):
        content=request.get_json()
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            profile_user=UserProfile.query.filter_by(uid=user_id).first()
            profile_id=profile_user.id
            chk_user=Qualification.query.filter_by(pid=profile_id).all()
            if chk_user == None:
                return noqualificationdetails
            else:
                Educationaldetails=[]
                for x in chk_user:
                    Singledetails={"qualification":x.qualificationtype,
                                    "year_of_passing":x.yearofpassout,
                                    "percentage":x.percentage,
                                    "cgpa":x.cgpa,
                                    "class":x.q_class,
                                    "description":x.description,
                                    "id":x.id,
                                    "stream":x.stream,
                                    "board":x.boarduniversity,
                                    "collegename":x.collegename,
                                    "grade":x.grade,
                                    "type":x.types
                                }
                    Educationaldetails.append(Singledetails)
                return Educationaldetails
        else:
            return session_invalid


##############################################################################

# PROFILE EDIT --EDUCATIONAL DETAILS GET [ID] #

################################################################################
def geteducationid(data):
        content=request.get_json()
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        q_id=data.get('q_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            profile_user=UserProfile.query.filter_by(uid=user_id).first()
            profile_id=profile_user.id
            chk_user=Qualification.query.filter_by(id=q_id,pid=profile_id).first()
            if chk_user == None:
                return noqualificationdetails
            else:
                Educationaldetails={
                    "id":chk_user.id,
                    "qualification":chk_user.qualificationtype,
                "year_of_passing":chk_user.yearofpassout,
                "percentage":chk_user.percentage,
                "cgpa":chk_user.cgpa,
                "collegename":chk_user.collegename,
                "stream":chk_user.stream,
                "board":chk_user.boarduniversity,
                "grade":chk_user.grade,
                "description":chk_user.description,
                "type":chk_user.types

                }
                return Educationaldetails
        else:
            return session_invalid


##########################################################
# PROFILE EDIT --EDUCATIONAL DETAILS  ADDING             #
##########################################################
def posteducation(data):
        content=request.get_json()
        user_id=data.get('user_id')
        session_id=data.get('session_id')       
        qua_type=data.get('qualification')
        year=data.get('year')
        percen=data.get('percentage')
        cgpa1=data.get('cgpa')
        q_class=data.get('class')
        description=data.get('description')
        stream=data.get('stream')
        boarduniversity=data.get('board')
        collegename=data.get('collegename')
        grade=data.get('grade')
        types=data.get('type')
        dict1={"qualification":qua_type,"board":boarduniversity,"stream":stream}
        level=qua_label[qua_type]
        # issue in the multiple adding of same qualification,subject and year
        se=checkSessionValidity(session_id,user_id)
        if se:       
               
            
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            chk_user_id=chk_user.id

            

            user1=Qualification.query.filter_by(pid=chk_user_id,qualificationtype=qua_type,stream=stream,yearofpassout=year).first()
            
            if user1!=None:
               return alreadyexist
           
            newqualification=Qualification(pid=chk_user_id,qualificationtype=qua_type,types=types,yearofpassout=year,percentage=percen,cgpa=cgpa1,q_class=q_class,description=description,stream=stream,boarduniversity=boarduniversity,collegename=collegename,qualificationlevel=level,grade=grade)
            
            db.session.add(newqualification)
            db.session.commit()
            universitypost(dict1)
            return updated
        else:
            return session_invalid


##########################################################
# PROFILE EDIT --EDUCATIONAL DETAILS  DELETION           #
##########################################################
def deleteeducation(data):
        content=request.get_json()
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        q_id=data.get('q_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user1=Qualification.query.filter_by(id=q_id).first()
            if chk_user1 != None:
                db.session.delete(chk_user1)
                db.session.commit()
                return deleted
            else:
                return invalidemail
        else:
            return session_invalid

##########################################################
# PROFILE EDIT --EDUCATIONAL DETAILS  UPDATING           #
##########################################################
def editeducation(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        q_id=data.get('q_id')
        qua_type=data.get('qualification')
        year=data.get('year')
        percen=data.get('percentage')
        cgpa1=data.get('cgpa')
        q_class=data.get('class')
        description=data.get('description')
        stream=data.get('stream')
        boarduniversity=data.get('board')
        collegename=data.get('collegename')
        grade=data.get('grade')
        types=data.get('type')
        dict1={"qualification":qua_type,"board":boarduniversity,"stream":stream}
        level=qua_label[qua_type]
        se=checkSessionValidity(session_id,user_id)
        if se:
            
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            chk_user_id=chk_user.id
            user1=Qualification.query.filter(Qualification.pid==chk_user_id,Qualification.id!=q_id,Qualification.qualificationtype==qua_type,Qualification.stream==stream,Qualification.yearofpassout==year).first()
               
            if user1!=None:
               return alreadyexist         
           
            chk_user=Qualification.query.filter_by(id=q_id).first()
            if chk_user != None:
                chk_user.qualificationtype=qua_type
                chk_user.yearofpassout=year
                chk_user.percentage=percen
                chk_user.cgpa=cgpa1
                chk_user.description=description
                chk_user.q_class=q_class
                chk_user.stream=stream
                chk_user.boarduniversity=boarduniversity
                chk_user.collegename=collegename
                chk_user.qualificationlevel=level
                chk_user.grade=grade
                chk_user.types=types
                db.session.commit()
                universitypost(dict1)
                return updated
            else:
                return invalidemail
        else:
            return session_invalid

################################################################################
# PROFILE EDIT --PHOTO DETAILS GET [from table to getway]                      #
################################################################################

def getphoto(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            if chk_user == None:
                return invalidemail
            else:
                if chk_user.photo == None:
                    return nophoto
                else:
                    return {'user_id': user_id,"photo":chk_user.photo}
        else:
            return session_invalid

##########################################################
#       PROFILE EDIT --PHOTO DETAILS  UPDATING           #
##########################################################
def postphoto(data):
        user_id=data.get('user_id')
        session_id=data.get('session_id')      
        photo=data.get('photo')
        se=checkSessionValidity(session_id,user_id)
        if se:
            chk_user=UserProfile.query.filter_by(uid=user_id).first()
            chk_user.photo=photo
            db.session.commit()
            return updated
        else:
            return session_invalid

# profile preview Middleware

class GetProfilePreview(Resource):

    def post(self):
        content=request.get_json()
        sessionid=content['session_id']
        user_id=content['user_id']
        sess_res=checkSessionValidity(sessionid,user_id)
        if not sess_res:
            return session_invalid
        else:
            response=profilepreview(user_id)
            return {"status":200,"message":response}

#function for fetch details for preview page

def profilepreview(user_id):
    user=UserProfile.query.filter_by(uid=user_id).first()
    if user.fullname==None or user.photo==None or user.padd1==None:
        err="Please fill your profile completely"
        return err
    userid=user.uid
    fname=user.fname
    lname=user.lname
    fullname=user.fullname
    phno=user.phno
    gender=user.gender
    photo=user.photo
    padd1=user.padd1
    padd2=user.padd2
    pcity=user.pcity
    pstate=user.pstate
    pcountry=user.pcountry
    ppincode=user.ppincode
    madd1=user.madd1
    madd2=user.madd2
    mcity=user.mcity
    mstate=user.mstate
    mcountry=user.mcountry
    mpincode=user.mpincode
    religion=user.religion
    caste=user.caste
    nationality=user.nationality
    dob=user.dob.date()
    s_caste=user.s_caste
    annualincome=user.annualincome
    aadhar=user.aadhar
    ppid=user.id
    userobj=User.query.filter_by(id=user_id).first()
    email=userobj.email
    quali=Qualification.query.filter_by(pid=ppid).all()
    if quali ==None:
        err="Please fill your profile completely"
        return err
    qualilist=[]
    for i in quali:
        pid=i.pid
        qualificationtype=i.qualificationtype
        stream=i.stream
        boarduniversity=i.boarduniversity
        yearofpassout=i.yearofpassout
        percentage=i.percentage
        cgpa=i.cgpa
        description=i.description
        q_class=i.q_class
        qualificationlevel=i.qualificationlevel
        collegename=i.collegename
        grade=i.grade
        types=i.types
        qualidict={"pid":pid,"qualificationtype":qualificationtype,
        "stream":stream,"boarduniversity":boarduniversity,"yearofpassout":yearofpassout,"type":types,
        "percentage":percentage,"cgpa":cgpa,"description":description,"class":q_class,"qualificationlevel":qualificationlevel,
        "collegename":collegename,"grade":grade} 
        qualilist.append(qualidict)

    userdict={"userid":userid,"firstname":fname,"lastname":lname,"fullname":fullname,"phno":phno,"gender":gender,"photo":photo,

    "paddress1":padd1,"paddress2":padd2,"pcity":pcity,"pstate":pstate,"pcountry": pcountry,

    "ppincode":ppincode,"madd1":madd1,"madd2":madd2,"mcity":mcity,"mstate":mstate,"mcountry":mcountry,

    "mpincode":mpincode,"s_caste":s_caste,"religion":religion,"caste":caste,"nationality":nationality,"dob":str(dob),"aadhar":aadhar,"income":annualincome,

    "email":email, "qualification":qualilist}
    return userdict


# profile preview Gateway

class GetGetProfilePreviewApiGateway(Resource):
    def post(self):
        try:
            data=request.get_json()
            response = requests.post(profile_preview_api,json=data)
            response_json_text = json.loads(response.text)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)


######################MIDDLEWARE#####################################
######################FUNCTION#######################################
def checkapipermission(user_id,api_name):
    roles=RoleMapping.query.filter_by(user_id=user_id).all()
    roles = [r.role_id for r in roles] 
    perm_list=Permission.query.filter(Permission.role_id.in_(roles)).filter_by(API_name=api_name).first()
    
    if perm_list != None:
        return True
    return False


def checkSessionValidity(sessionid,userid): 
    chk_user=Session.query.filter(Session.session_token==sessionid,Session.uid==userid,Session.exp_time>datetime.now()).first()
    
    if chk_user:
        return True
    else: 
        return False

def registerUser(email,password,first_name,last_name,phone):
       chk_user=User.query.filter_by(email=email).first()
       if (chk_user is not None):
            return emailexist
       date=datetime.date(datetime.now())
       exp_date=date+ timedelta(days=365)  
       new_user=User(email=email,password=password,reg_date=date,exp_date=exp_date)       
       db.session.add(new_user)       
       created_user=User.query.filter_by(email=email,password=password).first()       
       uid=created_user.id
       new_user_profile=UserProfile(uid=uid,fname=first_name,lname=last_name,phno=phone)       
       db.session.add(new_user_profile)
       new_role_mapping=RoleMapping(role_id=generaluser_id,user_id=uid)
       db.session.add(new_role_mapping)
       db.session.commit()
       send_confirmation_email(email,first_name,last_name) 
       send_confirmation_sms(phone,first_name,last_name) 
       data={
                "status":200,
                "Message": "Register Successful",
                "uid":uid,
        }
       return data

def send_confirmation_email(useremail,first_name,last_name):
    # For production use enable the ssl server 
    # host='ssl://smtp.gmail.com'
    # port=465
    
    # For web staging
    host='smtp.gmail.com' 
    port=587

    email=mg_email
    password=mg_password
    context = ssl.create_default_context()
    subject="DASP Registration Completed "
    mail_to=useremail
    mail_from=email
    name=first_name+' '+last_name
    body="Hi {name},\n\n Your registration is successful.Kindly use your email id as username and password used during the registration process to login to the system   \n \n Team DASP  \n\n\n\n THIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL".format(name=name)
    # body="Hi {name},\n\n You are successfully registered for the Directorate for Applied Short-term Programmes(DASP) conducted by Mahatma Gandhi University. \n \n Thanks and Regards \n DASP \n Administrator".format(name=name)
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()        
        server.starttls(context=context)
        server.ehlo()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0

def send_confirmation_sms(phone,first_name,last_name):
    sms_url = "http://api.esms.kerala.gov.in/fastclient/SMSclient.php" 
    name=  first_name+' '+last_name

    message="Hi %s \n Your registration is successful.  \n\nTeam DASP"%(name)
    querystring = {"username":"mguegov-mguniv-cer","password":"mguecert","message":message,"numbers":phone,"senderid":"MGEGOV"}
    response = requests.request("GET", sms_url,  params=querystring)



def loginUser(email,password,dev_type,IP,MAC):
    if dev_type.lower()=="w":
        existing_user=User.query.filter_by(email=email).first()      
        if(existing_user is None):
                return invalidemail             
        if(existing_user.password==password):
                print("hjjh")
                ####Checking whether the user is admin####
               
                uid=existing_user.id
                #get all the roles assigned to the user
                user_roles=RoleMapping.query.filter_by(user_id=uid).add_column('role_id').all() 
                #Converting user roles to a list
                user_roles = [r.role_id for r in user_roles]  
                # Checking whether the user has admin rights
                role_list=Role.query.filter(Role.id.in_(user_roles)).filter_by(role_type="User").first()
                ####Checking whether the user is admin start####
                if(role_list is None): 
                    return msg_403   
                ####Checking whether the user is admin end####
                new_userprofile=UserProfile.query.filter_by(uid=uid).first()
                if new_userprofile.fullname!=None:    
                    name=new_userprofile.fullname
                else:
                    name=new_userprofile.fname

                Session.query.filter_by(uid=uid,dev_type=dev_type).delete()
                db.session.commit()                        
                curr_time=datetime.now()
                exp_time=curr_time++ timedelta(days=1)
                session_token = token_urlsafe(64)
                new_session=Session(uid=uid,dev_type=dev_type,session_token=session_token,exp_time=exp_time,IP=IP,MAC=MAC)
                db.session.add(new_session)
                db.session.commit()
                data={
                    "status":200,
                    "Message": "login Successful",
                    "uid":uid,
                    "name":name,

                    "f_name":new_userprofile.fname,
                    "session_id":session_token
                }  
                return (data)
        else:
            return unsuccessfulllogin
    elif dev_type.lower()=="m":
        existing_user=User.query.filter_by(email=email).first()
        if existing_user is None:
            return format_response(False, "Invalid email", {}, 400)
        if(existing_user.password==password):
            ####Checking whether the user is admin####
            
            uid=existing_user.id
            #get all the roles assigned to the user
            user_roles=RoleMapping.query.filter_by(user_id=uid).add_column('role_id').all() 
            #Converting user roles to a list
            user_roles = [r.role_id for r in user_roles]  
            # Checking whether the user has admin rights
            role_list=Role.query.filter(Role.id.in_(user_roles)).filter_by(role_type="User").first()
            ####Checking whether the user is admin start####
            if(role_list is None): 
                return format_response(False,"Forbidden access",{},403)
            ####Checking whether the user is admin end####
            new_userprofile=UserProfile.query.filter_by(uid=uid).first()
            if new_userprofile.fullname!=None:    
                name=new_userprofile.fullname
            else:
                name=new_userprofile.fname

            Session.query.filter_by(uid=uid,dev_type=dev_type).delete()
            db.session.commit()                        
            curr_time=datetime.now()
            exp_time=curr_time++ timedelta(days=1)
            session_token = token_urlsafe(64)
            new_session=Session(uid=uid,dev_type=dev_type,session_token=session_token,exp_time=exp_time,IP=IP,MAC=MAC)
            db.session.add(new_session)
            db.session.commit()
            response=student_check(uid)
            data={
            "uid":uid,
            "name":name,
            "isStudent":response.get('isStud'),
            "fname":new_userprofile.fname,
            "sessionId":session_token
            } 
            return format_response(True,"Login successful",data)
        else:
            return format_response(False,"Login failed",{},401)


def student_check(uid):                         
    userData = requests.post(
    student_check_backendapi,json={"user_id":uid})            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse


################################################################
#####                ADMIN MODULE START                    #####
################################################################
def loginAdmin(email,password,dev_type,IP,MAC):        
        #####Checking whether user exits#####
        existing_user=User.query.filter_by(email=email).first()
        
        if(existing_user is None): #User does not exists
                return invalidemail  
                   
        if(existing_user.password==password):# user exists
                
                ####Checking whether the user is admin####
               
                uid=existing_user.id
                user_roles=RoleMapping.query.filter_by(user_id=uid).add_column('role_id').all() #get all the roles assigned to the user
                user_roles = [r.role_id for r in user_roles] #Converting user roles to a list
                role_list=Role.query.filter(Role.id.in_(user_roles)).filter_by(role_type="Admin").first() # Checking whether the user has admin rights
                
                if(role_list is None): #user is not admin
                    return (msg_403)   
                ####Checking whether the user is admin####
                
                #####User is admin ###################################
                new_userprofile=UserProfile.query.filter_by(uid=uid).first()
                name=new_userprofile.fname                
                Session.query.filter_by(uid=uid,dev_type=dev_type).delete()
                db.session.commit()
                
                ##creating a new session start 
                curr_time=datetime.now()
                exp_time=curr_time++ timedelta(days=1)
                session_token = token_urlsafe(64)
                new_session=Session(uid=uid,dev_type=dev_type,session_token=session_token,exp_time=exp_time,IP=IP,MAC=MAC)
                
                db.session.add(new_session)
                db.session.commit()
                ##creating a new session end
                data={
                        "Status":200,
                        "Message": "login Successful",
                        "uid":uid,
                        "name":name,
                        "session_id":session_token
                    }                
                return data
        else:
            return unsuccessfulllogin


################################################################

# LIST OF APPLICANTS FUNCTIONALITY AND API GATEWAY #

################################################################

def appliedlist(a):
    data1={"batch_id":a}
    homeData = requests.post(
    lists_backendapi,json=data1)
    homeDataResponse=json.loads(homeData.text)
    if homeDataResponse.get("status") == 200:
        userDict=homeDataResponse.get("message") 
        uid=userDict.get("Users")
        batch=userDict.get("batch")
        # print(batch)
        user_list=[]
        if len(uid)!=0:
            for user_ids in uid:
                users_ids=user_ids.get("user_id")
                users_ids=int(users_ids)
                app_date=user_ids.get("applied_date")
                app_time=user_ids.get("applied_time")
                status=user_ids.get("status")
                ispaid=user_ids.get("is_paid")
                applicantid=user_ids.get("applicantid")
                other_batch=user_ids.get("other_batch")
                other_prg_code=user_ids.get("other_prg_code")
                chk_user=UserProfile.query.filter_by(uid=users_ids).first()
                if chk_user!=None:
                        
                    users_id=chk_user.id
                    userqualification=Qualification.query.filter_by(pid=users_id).all()

                    if userqualification!=None:
                        level=[]
                        for i in userqualification:
                            level.append(i.qualificationlevel)
                            levels=max(level)
                        for i in userqualification:
                            
                            if int(i. qualificationlevel)==int(levels):
                                userdetails={"user_id":users_ids,"firstname":chk_user.fname,"lastname":chk_user.lname,"fullname":chk_user.fullname,
                                "qualificationtype":i.qualificationtype,"year_of_passout":i.yearofpassout,"type":i.types,
                                "percentage":i.percentage,"cgpa":i.cgpa,"class":i.q_class,"description":i.description,
                                            "applied_date":app_date,"applied_time":app_time,"grade":i.grade,"status":status,
                                            "ispaid":ispaid,"applicantid":applicantid,"subject":i.stream,"other_batch":other_batch,"other_prg_code":other_prg_code
                                }
                                
                                user_list.append(userdetails)
                                break
                            else:
                                print("elseeee")
        else:
            user_list=[]
        response={"status":200,"batch":batch,"userlist":user_list}
        return response

    else:
        return homeDataResponse



###########################################################

# LIST OF PROGRAMME FUNCTIONALITY AND API GATEWAY #

###########################################################

# def applicants():    
#     homeData = requests.get(
#     prgm_backendapi)
#     homeDataResponse=json.loads(homeData.text)
#     return homeDataResponse

def admissionprogrambatch(pid):
    homeData = requests.post(prgm_batch_backendapi,json={"pid":pid})
    homeDataResponse=json.loads(homeData.text)
    return homeDataResponse

################################################################
#####                 ADMIN MODULE END                     #####
################################################################                

######################FUNCTION#######################################

############################################
#PAYMENT GATEWAY FOR REGISTRATION          #
############################################

def getpayment(data1):
        
        user_id=data1.get('user_id')
        purpose=data1.get('purpose')
        url="https://epay.mgu.ac.in/mguCPMS/Paymentz/index"
        hashkey="081ea7b13162b9a4749f9e6b98d29177"
        hashkey_b=bytearray(hashkey, 'utf-8')
        applicationname="DASTP2018"
        feeheadid="121"
        #user_id=int(user_id)
        # appNo=uuid.uuid1().int>>64
        # transid=uuid.uuid1().int>>64
        applicationNo=user_id
        transactionreqid=uuid.uuid1().int>>64

        chk_user=User.query.filter_by(id=user_id).first()
        email=chk_user.email
        chk_user1=UserProfile.query.filter_by(uid=user_id).first()
        first=chk_user1.fname
        last=chk_user1.lname
        phno=chk_user1.phno
        chk_user.trans_req_id=transactionreqid
        db.session.commit()
        # totalamount=amount
        totalamount="1"
        u_id=uuid.uuid1().int>>64
        registrationNo=u_id
        name=first+last
        requestparameter = applicationname+"|"+ feeheadid+"|"+ str(applicationNo)+"|"+ str(registrationNo)+"|"+ str(transactionreqid)+"|"+ name+"|"+ email+"|"+ str(phno)+"|"+ totalamount+"|"+ purpose+"||||DASTPRegistrationFee"
        skey = "081ea7b13162b9a4749f9e6b98d29177"
        code1 = hmac.new(skey.encode(), requestparameter.encode(), hashlib.sha256).hexdigest()
        code1=code1.upper()
        requestparameter =requestparameter+"|"+code1
        requestparameter={"url":url,"epay_req_params":requestparameter}
        return requestparameter
   

######################################################################
# PAYMENT REQUEST RESPONSE API                                       #
######################################################################
# class Transcationresponse(Resource):
def transactionresponses(data1):
#     def post(self):
        # content=request.get_json()
        user_id=data1.get('user_id')
        transcation_id=data1.get('transcation_id')
        gateway=data1.get('gateway')
        gateway_id=data1.get('gateway_id')
        amount=data1.get('amount')
        purpose=data1.get('purpose')
        service_charge=data1.get('service_charge')
        payment_time=data1.get('payment_time')
        bank_reference=data1.get('bank_reference')
        payment_status=data1.get('payment_status')
        application_no=data1.get('application_no')
        bankname=data1.get('bankname')
        discriminator=data1.get('discriminator')
        description=data1.get('description')
        session_id=data1.get('session_id')
        se=checkSessionValidity(session_id,user_id)
        if se:
            if purpose=="registration":
                if payment_status!="failure":
                    userTable=User.query.filter_by(id=user_id).first()
                    # userTable.trans_id=transcation_id
                    # userTable.reg_date=reg_date
                    # userTable.exp_date=exp_date
                    db.session.commit()
                transactiontable=Transactiontable(uid=user_id,gateway=gateway,gateway_id=gateway_id,amount=amount,purpose=purpose,service_charge=service_charge,payment_time=payment_time,bank_reference=bank_reference,payment_status=payment_status,application_no=application_no,bankname=bankname,discriminator=discriminator,description=description)
                db.session.add(transactiontable)
                db.session.commit()
                return updated
            else:
                if payment_status!="failure":
                    userTable=User.query.filter_by(id=user_id).first()
                    userTable.trans_id=transcation_id
                    # userTable.reg_date=reg_date
                    # userTable.exp_date=exp_date
                    db.session.commit()
                transactiontable=Transactiontable(uid=user_id,gateway=gateway,gateway_id=gateway_id,amount=amount,purpose=purpose,service_charge=service_charge,payment_time=payment_time,bank_reference=bank_reference,payment_status=payment_status,application_no=application_no,bankname=bankname,discriminator=discriminator,description=description)
                db.session.add(transactiontable)
                db.session.commit()
                return updated
        else:
            return session_invalid


######################################################################
# PAYMENT REQUEST RESPONSE FAILURE API                               #
######################################################################
# class TranscationresponseFailed(Resource):
def paymentfailure(data1):
#     def post(self):
        content=request.get_json()
        user_id=data1.get('user_id')
        session_id=data1.get('session_id')
        se=checkSessionValidity(session_id,user_id)
        if se: 
            userTable=User.query.filter_by(id=user_id).first()
            req_id=userTable.trans_req_id
            #API CALLING
            RequestURL = "https://epay.mgu.ac.in/mguCPMS/Paymentzresponse/index"
            hashKey	= "081ea7b13162b9a4749f9e6b98d29177"
            AplicationName = "DASTP2018"
            FeeHeadId = "121"
            missing_id=req_id+","+str(user_id)
            parameters = AplicationName+"|"+FeeHeadId+"|"+missing_id
            code1 = hmac.new(hashKey.encode(), parameters.encode(), hashlib.sha256).hexdigest()
            code1=code1.upper()
            parameters = parameters+"|"+code1
            return {"url":RequestURL,"epay_req_params":parameters}
        else:
            return session_invalid

            
            
###########################################
#GATEWAY API FOR GET THE REQUEST PARAMETER#
###########################################
class PaymentGateway1(Resource):
    def post(self):
        try:
            data=request.get_json()
            purpose=data["purpose"]
            user_id=data["user_id"]
            session_id=data["session_id"]
            if purpose=="registration":
                data1={"user_id":user_id,"purpose":purpose}
                # response=requests.post(paymentGatewayApi,json=data1)
                # response_json_text = json.loads(response.text)
                response_json_text=getpayment(data1)
                return jsonify(response_json_text)
            else:
               
                se=checkSessionValidity(session_id,user_id)
                if se:
                    data1={"user_id":user_id,"purpose":purpose}
                    # response=requests.post(paymentGatewayApi,json=data1)
                    # response_json_text = json.loads(response.text)
                    response_json_text=getpayment(data1)
                    return jsonify(response_json_text)
                else:
                    return session_invalid
        except Exception as e:
            return jsonify(error)
#############################################
#GATEWAY API FOR GET THE TRANSCATION DETAILS#
#############################################
class PayTransactionResponse(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=transactionresponses(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)
######################################################################
# PAYMENT REQUEST RESPONSE FAILURE API                               #
######################################################################
class PayTransactionResponseFailure(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=paymentfailure(data)
            return jsonify(response_json_text)
        except:
            return jsonify(error)
################################################################
# UNIVERSITY API                                               #
################################################################
def universityget():
    
    chk_user=Universities.query.all()
    lists=[]
    for i in chk_user:
        dicts={
            "id":i.id,
            "name":i.name,
            "pid":i.pid
        }
        lists.append(dicts)
    successresponse={"status":200,"list":lists}
    return successresponse
################################################################
# UNIVERSITY API  GATEWAY                                      #
################################################################
class University(Resource):
    def get(self):
        try:
            data=universityget()
            return jsonify(data)
        except:
            return jsonify(error)
################################################################
# UNIVERSITY API POST                                          #
################################################################

def universitypost(dict1):
        board=dict1["board"]
        stream=dict1["stream"]
        qualification=dict1["qualification"]
        chk_user=Universities.query.filter_by(name=board).first()
        if chk_user == None:
            chk_user1=Universities.query.filter_by(name=qualification).first()
            ids=chk_user1.id
            newqualification=Universities(name=board,pid=ids)
            db.session.add(newqualification)
            db.session.commit()
            chk_user2=Universities.query.filter_by(name=board).first()
            id1=chk_user2.id
            chk_user3=Universities.query.filter_by(name=stream,pid=id1).first()
            if chk_user3==None:
                newqualification2=Universities(name=stream,pid=id1)
                db.session.add(newqualification2)
                db.session.commit()
        else:
            # chk_user1=Universities.query.filter_by(name=board).first()
            ids=chk_user.id
            chk_user2=Universities.query.filter_by(name=stream,pid=ids).first()
            if chk_user2 == None:
                newqualification=Universities(name=stream,pid=ids)
                db.session.add(newqualification)
                db.session.commit()
            
            

#############################################################################
#################### WORK ENGINE FOR ADMISSION MODULE #######################
#############################################################################

# Cache token for admission module 
@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def gettoken():
    token_res = requests.get(getToken)
    token=json.loads(token_res.text)['token']    
    return token

# Cache token for info module 
@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def gettoken_info_module():
    token_res= requests.get(getToken_info_module)
    token=json.loads(token_res.text)['token']    
    return token
# Cache for questionaire
@cached(cache=cachequestion)
def cache_question(pgm_id):
    questionaireData = requests.post(
    getquestionaire,json={"pid":pgm_id})
    questionaireResponse=json.loads(questionaireData.text)
    return questionaireResponse

#Function for checking userprofile,qualification completion
def is_emptyprofile_qualification(user_id):
    session_exist=UserProfile.query.filter_by(uid=user_id).first()
    if session_exist.fullname==None or session_exist.photo==None or session_exist.padd1==None:
        return profile
    ppid=session_exist.id
    quali=Qualification.query.filter_by(pid=ppid).first()
    if quali==None:
        return qualification
    else:
        return {"status":200}

#function for fetching user details 
def applicantdet(user_id):
    user=UserProfile.query.filter_by(uid=user_id).first()
    userid=user.uid
    name=user.fullname
    phno=user.phno
    gender=user.gender
    photo=user.photo
    religion=user.religion
    caste=user.caste
    s_caste=user.s_caste
    nationality=user.nationality
    dob=user.dob.date()
    aadhar=user.aadhar
    income=user.annualincome
# premanant address 
    padd1=user.padd1
    padd2=user.padd2
    pcity=user.pcity
    pcountry=user.pcountry
    ppincode=user.ppincode
    pstate=user.pstate
# mailing address
    madd1=user.madd1
    madd2=user.madd2
    mcity=user.mcity
    mcountry=user.mcountry
    mpincode=user.mpincode
    mstate=user.mstate

    ppid=user.id
    
    userobj=User.query.filter_by(id=user_id).first()
    email=userobj.email
    quali=Qualification.query.filter_by(pid=ppid).all()
    qualilist=[]
    for i in quali:
        pid=i.pid
        qualificationtype=i.qualificationtype
        stream=i.stream
        boarduniversity=i.boarduniversity
        yearofpassout=i.yearofpassout
        percentage=i.percentage
        cgpa=i.cgpa
        description=i.description
        q_class=i.q_class
        qualificationlevel=i.qualificationlevel
        collegename=i.collegename
        grade=i.grade 
        types=i.types
        qualidict={"pid":pid,"qualificationtype":qualificationtype,
   "stream":stream,"boarduniversity":boarduniversity,"yearofpassout":yearofpassout,"type":types,
    "percentage":percentage,"cgpa":cgpa,"description":description,"class":q_class,"qualificationlevel":qualificationlevel,
    "collegename":collegename,"grade":grade} 

        qualilist.append(qualidict)
    userpermanantaddress={"padd1":padd1,"padd2":padd2,"pcity":pcity,"pcountry":pcountry,"ppincode":ppincode,"pstate":pstate}
    usermailingaddress={"madd1":madd1,"madd2":madd2,"mcity":mcity,"mcountry":mcountry,"mpincode":mpincode,"mstate":mstate}
    userdict={"userid":userid,"name":name,"phno":phno,"gender":gender,"photo":photo,"religion":religion,"caste":caste,"s_caste":s_caste,
    "nationality":nationality,"dob":str(dob),"aadhar":aadhar,"income":income,"email":email, "qualification":qualilist,
    "userpermanantaddress":userpermanantaddress,"usermailingaddress":usermailingaddress}
    return userdict

###################################################################
#  APPLICANT DETAIL PREVIEW PAGE----API GATEWAY                   #          
###################################################################
# class Applicantpreview(Resource):
#     def post(self):
#         content=request.get_json()
#         sessionid=content['session_id']
#         user_id=content['user_id']
#         prgm_id=content['pgm_id']
#         batch_id=content['batch_id']
#         student_id=content['student_id']
#         sess_res=checkSessionValidity(sessionid,user_id)  
#         if sess_res:
#             per=checkapipermission(user_id,self.__class__.__name__)
#             if per:
#                 questionaireResp=cache_question(prgm_id)
#                 prg_details=questionaireResp.get('message').get('ProgramDetails')
#                 batch_details=questionaireResp.get('message').get('BatchDetails').get(str(batch_id))
#                 userdetails=applicantdet(student_id)
#                 return{"status":200,"userdetails":userdetails,"batchdetails":batch_details,"programme_details":prg_details}
                
#             else:
#                 return msg_403
#         else:
#             return session_invalid     

def prgm_fetch(pgm_id,student_id,batch_id):
    questionaireData = requests.post(
    prgm_payment_backendapi,json={"pid":pgm_id,"student_id":student_id,"batch_id":batch_id})
    questionaireResponse=json.loads(questionaireData.text)
    return questionaireResponse


class Applicantpreview(Resource):
    def post(self):
        try:
            content=request.get_json()
            sessionid=content['session_id']
            user_id=content['user_id']
            prgm_id=content['pgm_id']
            batch_id=content['batch_id']
            student_id=content['student_id']
            sess_res=checkSessionValidity(sessionid,user_id)  
            if sess_res:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    questionaireResp=prgm_fetch(prgm_id,student_id,batch_id)
                    prg_details=questionaireResp.get('message').get('ProgramDetails')
                    batch_details=questionaireResp.get('message').get('BatchDetails').get(str(batch_id))
                    payment_details=questionaireResp.get('message').get('paymentDetails')
                    userdetails=applicantdet(student_id)
                    
                    return{"status":200,"userdetails":userdetails,"batchdetails":batch_details,"programme_details":prg_details,"paymentDetails":payment_details}
                    
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error) 


#############################################################################
 #STUDENT LIST                                                              #
#############################################################################

class Studentlist(Resource):
    def post(self):
        try:
            content=request.get_json()
            sessionid=content['session_id']
            user_id=content['user_id']
            purpose=content['purpose']
            start_date=content['start_date']
            end_date=content['end_date']
            sess_res=checkSessionValidity(sessionid,user_id)  
            if sess_res:
                per=checkapipermission(user_id,self.__class__.__name__)
                
                if per:
                    if purpose.lower()=="r":
                        userList=[]
                        user=db.session.query(User,UserProfile,RoleMapping,Role).with_entities(User.id.label("user_id"),UserProfile.fname.label("name"),UserProfile.lname.label("last_name"),UserProfile.phno.label("phno"),User.email.label("email"),UserProfile.nationality.label("nationality")).filter(User.reg_date>=start_date,User.reg_date<=end_date,User.id==UserProfile.uid,Role.role_name=="Student",RoleMapping.role_id==Role.id,RoleMapping.user_id==UserProfile.uid).order_by(UserProfile.fname).all()
                        
                        userData=list(map(lambda n:n._asdict(),user))
                        
                        if userData!=[]:
                            return {"status":200,"message":userData,"purpose":purpose.lower()}
                        
                            # studentResp=studentlist(userData,purpose)
                            # return jsonify(studentResp)
                        else:
                            return jsonify({"status":404,"message":"No data found"})
                    elif purpose.lower()=="a" or purpose.lower()=="c":
                       
                        t=datetime.now()
                        studentResp=studentlist(purpose,start_date,end_date)
                       
                        usr_list=studentResp.get("message")
                       
                        userList=[]
                        for usr in usr_list:
                            user=db.session.query(User,UserProfile).with_entities(User.id.label("user_id"),UserProfile.fullname.label("name"),UserProfile.phno.label("phno"),User.email.label("email"),UserProfile.nationality.label("nationality")).filter(User.id==usr.get("user_id"),User.id==UserProfile.uid).order_by(UserProfile.fname).all()
                            if user!=[]:
                                userData=list(map(lambda n:n._asdict(),user))
                                userData[0]['prg_name']=usr.get("prg_name")
                                userData[0]['batch_name']=usr.get("batch_name")
                                userList.append(userData[0])
                        return {"status":200,"message":userList,"purpose":purpose.lower()}
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
                         
    

def studentlist(purpose,start_date,end_date):         
    studdata = requests.post(studentlist_backendapi,json={"purpose":purpose,"start_date":start_date,"end_date":end_date})
    studdataResponse=json.loads(studdata.text)
    return studdataResponse








       
#############################################################################
 # ONGOING PRGM                   -----API FUNCTIONALITY                   #
#############################################################################
# Caching the ongoing programme 
@cached(cache=ongoingprogramcache)
def ongoing_prgm_cache(dtype):         
    studdata = requests.post(ongoing_backendapi,json={"dtype":dtype})
    return studdata
def ongoing_prgm(dtype):         
    studdata = requests.post(ongoing_backendapi,json={"dtype":dtype})
    studdataResponse=json.loads(studdata.text)
    return studdataResponse


class OngoingProgram(Resource):
    def post(self):
        try:
            content=request.get_json()
            dtype=content['dtype']
            data=ongoing_prgm_cache(dtype)
            resData=json.loads(data.text)
            return resData
        except Exception as e:
            return jsonify(error) 
            

#############################################################################
 # ONGOING PRGM                   -----API FUNCTIONALITY                   #
#############################################################################
# Caching the upcoming programme 
@cached(cache=upcomingprogramcache)
def upcoming_prgm_cache(dtype):         
    studdata = requests.post(upcoming_backendapi,json={"dtype":dtype})

    return studdata

def upcoming_prgm(dtype):         
    studdata = requests.post(upcoming_backendapi,json={"dtype":dtype})
    studdataResponse=json.loads(studdata.text)
    return studdataResponse


class UpcomingProgram(Resource):
    def post(self):
        try:
            content=request.get_json()
            dtype=content['dtype']
            data=upcoming_prgm_cache(dtype)
            resData=json.loads(data.text)
            return resData
        except Exception as e:
            return jsonify(error) 

#############################################################################
 # APPLICANT ALREADY EXIST OR NOT  -----API FUNCTIONALITY                   #
#############################################################################
def applicantexistornot(user_id,prgm_id,batch_id):         
    studdata = requests.post(applicantexistornot_api,json={"batchid":batch_id,"userid":user_id,
    "prgid":prgm_id} )
    studdataResponse=json.loads(studdata.text)
    return studdataResponse

#############################################################################
# APPLICANT ALREADY EXIST OR NOT  -----API GATEWAY                          #
#############################################################################
class Applicantexistornot(Resource):
    def post(self):
        content=request.get_json()
        sessionid=content['session_id']
        user_id=content['user_id']
        prgm_id=content['pgm_id']
        batch_id=content['batch_id']
       
        sess_res=checkSessionValidity(sessionid,user_id)  
        if sess_res:
            data=applicantexistornot(user_id,prgm_id,batch_id)
            return data
            
        else:
            return session_invalid 
            



# Getting the questionair
# class GetQuestionaire(Resource):
def getquestionaires(data):    
        sessionid=data.get('session_id')
        user_id=data.get('user_id')
        prgm_id=data.get('pgm_id')
        batch_id=data.get('batch_id')
        #Calling the session validation function
        sess_res=checkSessionValidity(sessionid,user_id) 
        if not sess_res:
            return session_invalid        
        else:            
            questionaireResp=cache_question(prgm_id)            
            if questionaireResp.get('status')==200:
                questions=questionaireResp.get('message').get('questions')
                pgm_id=questionaireResp.get('message').get('prgid')
                status=questionaireResp.get('message')
                message={'questions':questions,'prgm_id':pgm_id}  
                questionaireResponse={'status':200,'message':message}
                return questionaireResponse
            else:
                return error

class GetQuestionaireApiGateway(Resource):
    def post(self):
        try:
            data=request.get_json()            
            response_json_text=getquestionaires(data)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)

# api.add_resource(GetQuestionaire, '/getquestionaire')
api.add_resource(GetQuestionaireApiGateway, '/api/getquestionaire')


############ ANSWER VALIDATION #############

# Answer validation Middleware
def getanswer(data):
        pgm_id=data.get('pgm_id')
        batch_id=data.get('batch_id')
        user_answer=data.get('answer')
        sessionid=data.get('session_id')
        user_id=data.get('user_id')
        sess_res=checkSessionValidity(sessionid,user_id)        
        if not sess_res:
            return session_invalid
        else:      
            questionaireResp=cache_question(pgm_id)
            answers=questionaireResp.get('message').get('answer')        
            ans=user_answer.items() == answers.items()
        if ans:
            fun_res=is_emptyprofile_qualification(user_id)
            result=fun_res.get("status")
            prg_details=questionaireResp.get('message').get('ProgramDetails')
            batch_details=questionaireResp.get('message').get('BatchDetails').get(str(batch_id))
                        
            if result==202:
                return {"status":200,"message":"Please fill your qualification details","batchdetails":batch_details,"programdetails":prg_details}
            if result==201:
                return {"status":200,"message":"Please fill your profile completely","batchdetails":batch_details,"programdetails":prg_details} 
            else:
                userdetails=applicantdet(user_id)  
                return {"status":200,"message":"You are eligible for this course","batchdetails":batch_details,"programdetails":prg_details,"userdetails":userdetails}
        else:
            return noteligible

# Answer validation Gateway
class GetQuestionaireAnswersApiGateway(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=getanswer(data)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)

################# STUDENT ADD ###################

# Student details add to student_applicant table
# Student details add to student_applicant table
# class StudentAdd(Resource):
def studentapply(data):
        content=request.get_json()
        batch_id=data.get('batchid')
        user_id=data.get('user_id')
        pgm_id=data.get('pgm_id')
        pgm_fee="-1"
        trans_id="-1"
        sessionid=content['session_id']
        dept_code=content['deptcode']
        sess_res=checkSessionValidity(sessionid,user_id)
        
        if  sess_res:
            curr_date=datetime.now()
            studdata = requests.post(addapplicant,json={"batchid":batch_id,"userid":user_id,
            "prgid":pgm_id,"applieddate":str(curr_date),"fees":pgm_fee,"transid":trans_id,"deptcode":dept_code} )
            studdataResponse=json.loads(studdata.text)
            if studdataResponse.get('message')=="successfully added student details":
                return {"status":200,"message":"Success"}
                  
            else:
                return studdataResponse

        else:
            return session_invalid
        
        

# student add Gateway
class StudentApplyApiGateway(Resource):
    def post(self):
        try:
            data=request.get_json()
            response_json_text=studentapply(data)
            return jsonify(response_json_text)
        except Exception as e:
            return jsonify(error)
################################################################
#                        SECOND SPRINT API                     #
################################################################

#######################################################################
# TEACHER APPLY COURSES   ----API FUNCTIONALITY                       #
#######################################################################

def teacherapply(dict1):
    userprofile=teacher.query.filter_by(emailid=dict1.get('emailid')).first()
    if userprofile==None:
        teachers=teacher(fname=dict1.get('fname'),lname=dict1.get('lname'),description=dict1.get('description'),resumepath=dict1.get('resumepath'),emailid=dict1.get('emailid'),status="applied",phno=dict1.get('phno'))
        db.session.add(teachers)
        db.session.commit()
        return updated
    else:
        return emailexist 

#######################################################################
# TEACHER APPLY COURSES   ----API GATEWAY CLASS                       #
#######################################################################
class Teacherapply(Resource):
    def post(self):
        try:
            data=request.get_json()
            fname=data['fname']
            lname=data['lname']
            description=data['description']
            resumepath=data['resumepath']
            emailid=data['emailid']
            phno=data['phno']
            dict1={"fname":fname,"lname":lname,"description":description,"resumepath":resumepath,"emailid":emailid,"phno":phno}            
            response = teacherapply(dict1)
            return jsonify(response)
        except Exception as e:
            return jsonify(error)
        
#######################################################################
# ADDING TEACHER BY ADMIN ----API FUNCTIONALITY                       #
#######################################################################
def lmsteacherfetch(userid,email,fname,phone):
    data={  
    "externalId":userid,
    "role":{  
        "roleId":2,
        "secondaryRoleId":7
    },
    "regAsAdmin":True,
    "mandatoryData":{  
        "eMail":email,
        "mobile":phone,
        "firstName":fname
    },
    "external":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJOYW1lIjoiYWRtaW5AbWd1LmNvbSIsImNvbXBhbnlJZCI6IjVjNzY4NmFjNjQ5Nzk2MTQzNTEyMTk1MSIsInJvbGVJZCI6IjIiLCJ1c2VyRGV0YWlsc0lkIjoiNWNlY2RhNjI2NzhjZWYxNjYzZmM0MWQxIiwidXNlckxvZ2luSWQiOiI1Y2VjZGE2MTY3OGNlZjE2NjNmYzQxZDAiLCJwYXNzd29yZCI6Im1ndV9hZG1pbiIsInJvbGVNYXBwaW5nSWQiOiI1Y2VjZGE2MjY3OGNlZjE2NjNmYzQxZDIifX0.AqNwW3EMby9jR_cLBzmtPQWp4N32A00OlxW_rTXKWjY"
    }
    data=json.dumps(data)
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InR5cGUiOiJjb21wYW55QXV0aCIsImNvbXBhbnlJZCI6IjVjNzY4NmFjNjQ5Nzk2MTQzNTEyMTk1MSJ9fQ.oADmwE7_J81Uo6VQRcPl3UGX08vcKE8mIWqkVLr4cRE"
    headers = {'Content-Type': 'application/json','Authorization':token}
    response1 = requests.post(teacher_reg_api,json=json.loads(data),headers=headers)
    resp=json.loads(response1.text)
    resp=json.loads(resp)
    print(resp)
    if resp.get("statuscode")==412:
        return 0
    # print(resp)
    userobj=UserExtTokenMapping.query.filter_by(user_id=resp.get('externalId')).all()
    if userobj==[]:
        userres=UserExtTokenMapping(user_id=resp.get('externalId'),email_id="null",ext_token=resp.get('external'))
        db.session.add(userres)
        db.session.commit()
        return 1
    else:
        return 0

def adminteacher(dict1):
    date=datetime.date(datetime.now())
    users=User(email=dict1.get('emailid'),password=dict1.get('password'),reg_date=date,status="1")
    db.session.add(users)
    useridss=User.query.filter_by(email=dict1.get('emailid')).first()
    u_id=useridss.id
    userprofile=UserProfile(fname=dict1.get('fname'),lname=dict1.get('lname'),phno=dict1.get('phno'),uid=u_id)
    db.session.add(userprofile)
    rolemap_userprofile=RoleMapping(role_id=13 ,user_id=u_id)
    db.session.add(rolemap_userprofile)
    # db.session.commit()
    lms_res=lmsteacherfetch(u_id,dict1.get('emailid'),dict1.get('fname'),dict1.get('phno'))
    if lms_res==1:
        db.session.commit()
        return updated
    else:
        return emailexist


    
#######################################################################
# ADDING TEACHER BY ADMIN ----API GATEWAY CLASS                       #
#######################################################################

class AdminTeacher(Resource):
    def post(self):
        try:
            data=request.get_json()
            fname=data['fname']
            lname=data['lname']
            phno=data['phno']
            user_id=data['user_id']
            session_id=data['session_id']
            emailid=data['emailid']
            password=pwdGen()
            m = hashlib.sha512(password.encode('utf8')).hexdigest()
            body="Hi %s %s, \nCongratulations your profile has been created as a Teacher in Directorate for Applied Short-term Programmes (DASP).Please login with the given credentials \nusername: %s \npassword: %s \n \n Team DASP  \n\n\n\n THIS IS A SYSTEM GENERATED EMAIL - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL" % (fname,lname,emailid,password)
            
            dict1={"fname":fname,"lname":lname,"phno":phno,"password":m,"emailid":emailid,"userid":user_id}
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    userprofile=User.query.filter_by(email=emailid).first()
                    
                    if userprofile==None:
                        responsemail=adminsendemail1(emailid,body) 
                        
                        if responsemail==0:
                            return invaliduser
                        else:
                            response = adminteacher(dict1)
                            
                            return jsonify(response)
                    else:
                        return emailexist
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)
################################################################################
# SENDING MAIL TO APPLIED USERS BY ADMIN----MAIL SENDING FUNCTIONALITY         #
################################################################################

def adminsendemail1(username,body):
    #################################################################################
    # HERE USING A TEMPORARY MAIL ID FOR SENDING MAIL TO THE USER                   #
    #################################################################################
    # For production use enable the ssl server 
    # host='ssl://smtp.gmail.com'
    # port=465
    
    # For web staging
    host='smtp.gmail.com' 
    port=587

    email=mg_email
    password=mg_password
    context = ssl.create_default_context()
    subject="DASP Teacher profile creation"
    mail_to=username
    mail_from=email
    body=body
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0
######################################################################
# PASSWORD GENERATION                                                #
######################################################################
def pwdGen():
    pwd = ""
    password=''
    count = 0
    sym=['@','$','#']
    
    while count != 10:
        
        upper = [random.choice(string.ascii_uppercase)]
        lower = [random.choice(string.ascii_lowercase)]
        num = [random.choice(string.digits)]
        symbol = [random.choice(sym)]
        everything = upper + lower + num + symbol
        pwd += random.choice(everything)
        count += 1
    if count == 10:
       
        password=pwd
        pwd1=pbkdf2_sha256.encrypt(pwd, rounds=200000,
        salt_size=16)
        result={'password':password,'pwd':pwd1}
        return password

#######################################################################
# TEACHER LOGIN                                                       #
#######################################################################
# class TeacherLogin(Resource):
#     def post(self):
#         try:
#             data=request.get_json()
#             email=data['email']
#             password=data['password']
#             dev_type=data['devType']
#             ip=data['ip']
#             mac=data['mac']
#             #####Checking whether user exits#####
#             existing_user=User.query.filter_by(email=email).first()
#             if(existing_user is None): #User does not exists
#                     return format_response(False,"Invalid email",{},400)       
#             if(existing_user.password==password):# user exists
#                 ####Checking whether the user is admin####
#                 uid=existing_user.id
#                 status=existing_user.status
#                 user_roles=RoleMapping.query.filter_by(user_id=uid).add_column('role_id').all() #get all the roles assigned to the user
#                 user_roles = [r.role_id for r in user_roles] #Converting user roles to a list
#                 role_list=Role.query.filter(Role.id.in_(user_roles)).filter_by(role_type="Admin").first() # Checking whether the user has admin rights
#                 if(role_list is None): #user is not admin
#                     return format_response(False,"Forbidden access",{},403)  
#                 ####Checking whether the user is admin####
#                 #####User is admin ###################################
#                 IP=get_my_ip()
#                 new_userprofile=UserProfile.query.filter_by(uid=uid).first()
#                 name=new_userprofile.fname +' '+new_userprofile.lname             
#                 Session.query.filter_by(uid=uid,dev_type=dev_type).delete()
#                 db.session.commit()
#                 ##creating a new session start 
#                 curr_time=datetime.now()
#                 exp_time=curr_time++ timedelta(days=1)
#                 session_token = token_urlsafe(64)
#                 new_session=Session(uid=uid,dev_type=dev_type,session_token=session_token,exp_time=exp_time,IP=IP,MAC=IP)
#                 db.session.add(new_session)
#                 db.session.commit()
#                 ##creating a new session end
#                 data={
#                         "uid":uid,
#                         "name":name,
#                         "status":status,
#                         "sessionId":session_token
#                     }      
#                 return format_response(True,"Login successful",data)
#             else:
#                 return format_response(False,"Login failed",{},401)
#         except Exception as e:
#             return format_response(False, "Bad gateway", {}, 401)




#######################################################################
# LISTING ADMIN PERMISSIONS----API FUNCTIONALITY                      #
#######################################################################

def adminpermission(user_id):
    roles=RoleMapping.query.filter_by(user_id=user_id).all()
    roles = [r.role_id for r in roles] 
    perm_list=Role.query.filter(Role.id.in_(roles)).order_by("role_name").all()
    permissionlist=[]
    for i in perm_list:
        if i.role_type=="Admin":
            permissionlist.append(i.role_name)
    return {"status":200,"permissionlist":permissionlist}

#######################################################################
# LISTING ADMIN PERMISSIONS----API GATEWAY CLASS                      #
#######################################################################

class Adminpermission(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=adminpermission(user_id)
                    return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)
################################################################################
# SENDING MAIL TO APPLIED USERS BY ADMIN----MAIL SENDING FUNCTIONALITY         #
################################################################################

def adminsendemail(username,body):
    # if mail_from is None: mail_from = username
    # if reply_to is None: reply_to = mail_to
    #################################################################################
    # HERE USING A TEMPORARY MAIL ID FOR SENDING MAIL TO THE USER                   #
    #################################################################################
    # For production use enable the ssl server 
    # host='ssl://smtp.gmail.com'
    # port=465
    # For web staging
    host='smtp.gmail.com' 
    port=587

    email=mg_email
    password=mg_password
    context = ssl.create_default_context()    
    subject="DASP Payment Intimation"
    mail_to=username
    mail_from=email
    body="Hi,\n\n"+body+"\n \n Team DASP  \n\n\n\n THIS IS A SYSTEM GENERATED EMAIL - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL"
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls(context=context)
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0

################################################################################
# SENDING SMS TO APPLIED USERS BY ADMIN----SMS SENDING FUNCTIONALITY         #
################################################################################

def adminsendsms(user_list,smsData):
    sms_url = "http://api.esms.kerala.gov.in/fastclient/SMSclient.php"

    pgm_code=smsData.get("p_code")
    fee=smsData.get("p_fee")

    message="You are shortlisted for the Programme:%s.Check email for details  \n\nTeam DASP"%(pgm_code)

    for singleUser in user_list:
        querystring = {"username":"mguegov-mguniv-cer","password":"mguecert","message":message,"numbers":singleUser,"senderid":"MGEGOV"}
        response = requests.request("GET", sms_url,  params=querystring)

    # print(response.text)

#######################################################################
# SENDING MAIL TO APPLIED USERS BY ADMIN----API FUNCTIONALITY         #
#######################################################################

def adminuserlist(userlist,body,smsData):
    email=[]
    mobile_list=[]
    for i in userlist:
        useridss=User.query.filter_by(id=i).first()
        if useridss != None:
            if useridss.email not in email:
                email.append(useridss.email)
            user_det=UserProfile.query.filter_by(uid=i).first()

            mobile_list.append(user_det.phno)
    response=adminsendemail(email,body)
    sms_response=adminsendsms(mobile_list,smsData) 
    if response==0:
        return invaliduser
    else:
        return mailsent

#######################################################################
# SENDING MAIL TO APPLIED USERS BY ADMIN----API GATEWAY CLASS         #
#######################################################################
        
class Adminuserlist(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            userlist=data['userlist']
            batch_id=data['batch_id']
            body=data['body']
            userlist=list(set(userlist))
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    userlistData = requests.post(
                    adminuserlist_api,json={"userlist":userlist,"batch_id":batch_id})            
                    homeDataResponse=json.loads(userlistData.text)
                    if homeDataResponse.get("status")==200:
                        response=adminuserlist(userlist,body,homeDataResponse.get("data"))
                        return jsonify(response)
                    else:
                        return error
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)


##################################################################################
# SENDING REMINDER MAIL TO SELECTED USERS BY ADMIN----API GATEWAY CLASS         #
##################################################################################
        
class ReminderMail(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            userlist=data['userlist']
            batch_id=data['batch_id']
            mail_body=data['mail_body']
            sms_body=data['sms_body']
            subject=data['subject']
            userlist=list(set(userlist))
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=remindermail(userlist,mail_body,sms_body,subject)
                    return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)


def remindermail(userlist,mail_body,sms_body,subject):
    email=[]
    mobile_list=[]
    for i in userlist:
        useridss=User.query.filter_by(id=i).first()
        if useridss != None:
            if useridss.email not in email:
                email.append(useridss.email)
            user_det=UserProfile.query.filter_by(uid=i).first()

            mobile_list.append(user_det.phno)
    response=reminderemail(email,mail_body,subject)
    sms_response=remindersms(mobile_list,sms_body) 
    if response==0:
        return invaliduser
    else:
        return mailsent




    
################################################################################
# SENDING MAIL TO APPLIED USERS BY ADMIN----MAIL SENDING FUNCTIONALITY         #
################################################################################

def reminderemail(username,body,subject):
    # if mail_from is None: mail_from = username
    # if reply_to is None: reply_to = mail_to
    #################################################################################
    # HERE USING A TEMPORARY MAIL ID FOR SENDING MAIL TO THE USER                   #
    #################################################################################
    # For production use enable the ssl server 
    # host='ssl://smtp.gmail.com'
    # port=465
    
    # For web staging
    host='smtp.gmail.com' 
    port=587

    email=mg_email
    password=mg_password
    context = ssl.create_default_context()
    # subject="DASP Payment Reminder Intimation"
    mail_to=username
    mail_from=email
    body="Hi,\n\n"+body+"\n \n Team DASP  \n\n\n\n THIS IS A SYSTEM GENERATED EMAIL - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL"
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls(context=context)
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0


def remindersms(user_list,sms_body):
    sms_url = "http://api.esms.kerala.gov.in/fastclient/SMSclient.php"

    # pgm_code=smsData.get("p_code")
    # fee=smsData.get("p_fee")
    message=sms_body+"\n\nTeam DASP"
    # message="You are shortlisted for the Programme:%s.Check email for details  \n\nTeam DASP"%(pgm_code)

    for singleUser in user_list:
        querystring = {"username":"mguegov-mguniv-cer","password":"mguecert","message":message,"numbers":singleUser,"senderid":"MGEGOV"}
        response = requests.request("GET", sms_url,  params=querystring)

#######################################################################
# ALL PROGRAMME DETAILS APPLIED BY A USER----API FUNCTIONALITY        #
#######################################################################

def allprogrammeuserapplied(user_id):                          
    userData = requests.post(allprogrammeuserapplied_api,json={"userid":user_id} )       
    userDataResponse=json.loads(userData.text) 
    
    prlist=[]
    for x in userDataResponse.get("message"):
        prlist.append(int(x.get("programid")))       
    data1={"pid":prlist,"dtype":"w"}                           
    userData1 = requests.post(prg_course_list,json=data1 )       
    userDataResponse1=json.loads(userData1.text) 
    
    for x in userDataResponse.get("message"):
        for p in userDataResponse1.get("message"):
            if (int(x.get("programid")) == p.get("id")):
                x["description"]=p.get("description")
                x["courses"]=p.get("courses")
                x["thumbnail"]=p.get("thumbnail")
    userDataResponse["imgpath"]=userDataResponse1.get("imgpath")
    return userDataResponse

###########################################################################
#    ALL PROGRAMME DETAILS APPLIED BY A USER----API GATEWAY CLASS         #
###########################################################################

class Allprogrammeuserapplied(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            se=checkSessionValidity(session_id,user_id)
            if se:
                userData = requests.post(allprogrammeuserapplied_api,json={"userid":user_id} )       
                userDataResponse=json.loads(userData.text)
                msg=userDataResponse.get("message")
                for i in msg:
                    if i.get("status")=="student":
                        lmsDet=UserExtTokenMapping.query.filter_by(user_id=user_id).first()
                        if lmsDet!=None:
                            i["lms_token"]=lmsDet.ext_token
                        else:
                            i["lms_token"]="null"
                        for j in (i.get("courses")):
                            lmsCourseDet=LmsCourseMapping.query.filter_by(course_id=j.get("id")).first()
                            if lmsCourseDet!=None:
                                j["lms_c_id"]=lmsCourseDet.lms_c_id
                            else:
                                j["lms_c_id"]="null"


                    # print(i)
                return jsonify(userDataResponse)    
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)



#######################################################################
# ALL PROGRAMME DETAILS APPLIED BY A USER----API FUNCTIONALITY        #
#######################################################################

def teacherlist():
    user=db.session.query(teacher).with_entities(teacher.id.label("id"),teacher.fname.label("fname"),teacher.lname.label("lname"),teacher.description.label("description"),teacher.emailid.label("emailid"),teacher.status.label("status"),teacher.resumepath.label("resumepath")).all()   
    userData=list(map(lambda n:n._asdict(),user))
    teacherlist={"status":200,"teacherlist":userData}
    return teacherlist





###########################################################################
#  LIST OF TEACHERS-----API GATEWAY CLASS                                 #
###########################################################################

class Teacherlist(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=teacherlist()
                    return jsonify(response)
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)




######################################################################################
#                                     SPRINT 3                                       #
######################################################################################

######################################################################
#        ADMIN ADD DEPARTMENT--API FUNCTIONALITY                     #
######################################################################
def adddepartment(dept_name,dept_desc,dept_code):                          
    userData = requests.post(
    adddepartment_api,json={"dept_name":dept_name,"dept_desc":dept_desc,"dept_code":dept_code})            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN ADD DEPARTMENT--API GATEWAY                          #
######################################################################
    
class Adddepartment(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            dept_name=data['dept_name']
            dept_desc=data['dept_desc']
            dept_code=data['dept_code']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=adddepartment(dept_name,dept_desc,dept_code)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN EDIT DEPARTMENT--API FUNCTIONALITY                    #
######################################################################
def getalldepartment():               
    DepartmentData = requests.get(getalldepartment_api )        
    DataResponse=json.loads(DepartmentData.text) 
    return DataResponse

######################################################################
#        ADMIN EDIT DEPARTMENT--API GATEWAY                          #
######################################################################
#     
class Getalldepartment(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=getalldepartment()
                    return jsonify(response)  
                else:
                    return msg_403
            else:
                return session_invalid  
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN EDIT DEPARTMENT--API FUNCTIONALITY                    #
######################################################################
def editdepartment(dept_name,dept_desc,dept_id):                          
    userData = requests.post(
    editdepartment_api,json={"dept_name":dept_name,"dept_desc":dept_desc,"dept_id":dept_id})            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN EDIT DEPARTMENT--API GATEWAY                          #
######################################################################
#     
class Editdepartment(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            dept_name=data['dept_name']
            dept_desc=data['dept_desc']
            dept_id=data['dept_id']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editdepartment(dept_name,dept_desc,dept_id)
                    return jsonify(response)  
                else:
                    return msg_403
            else:
                return session_invalid  
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN DELETE DEPARTMENT--API FUNCTIONALITY                  #
######################################################################
# def deletedepartment(dept_id):
     
#     token=info_token_fetch()
#     headers = {'content-type': 'application/json','authorization':token}                            
#     userData = requests.post(
#     deletedepartment_api,json={"dept_id":dept_id},
#     headers=headers)            
#     userDataResponse=json.loads(userData.text) 
#     if userDataResponse.get('message')=="successfully deleted department":
#         cache.clear() 
#         #home api should call or not--not decided
#     return userDataResponse

# ######################################################################
# #        ADMIN DELETE DEPARTMENT--API GATEWAY                        #
# ######################################################################
# #     
# class Deletedepartment(Resource):
#     def post(self):
#         try:
#             data=request.get_json()
#             user_id=data['user_id']
#             session_id=data['session_id']
#             dept_id=data['dept_id']
#             print("heloooo")
#             se=checkSessionValidity(session_id,user_id) 
#             if se:
#                 per=checkapipermission(user_id,self.__class__.__name__)
#                 print(per)
#                 if per:
#                     response=deletedepartment(dept_id)
#                     return jsonify(response)    
#         except Exception as e:
#             return jsonify(error)
######################################################################
#        ADMIN GET  DEPARTMENT--API FUNCTIONALITY                  #
######################################################################
def getdepartment(did):                           
    userData = requests.post(
    getdepartment_api,json={"did":did})            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

######################################################################
#        ADMIN GET DEPARTMENT--API GATEWAY                        #
######################################################################
   
class Getdepartment(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            did=data['did']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=getdepartment(did)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)


######################################################################
#        ADMIN ADD EVENTS--API FUNCTIONALITY                     #
######################################################################
def addevents(data):                          
    userData = requests.post(
    addevents_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN ADD EVENTS--API GATEWAY                          #
######################################################################
    
class Addevents(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            title=data['title']
            desc=data['desc']
            start_date=data['start_date']
            end_date=data['end_date']
            pic=data['pic']
            data={"title":title,"desc":desc,"start_date":start_date,"end_date":end_date,"pic":pic}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=addevents(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN EDIT EVENTS--API FUNCTIONALITY                    #
######################################################################
def editevents(data):                           
    userData = requests.post(
    editevents_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    
    return userDataResponse

######################################################################
#        ADMIN EDIT EVENTS--API GATEWAY                          #
######################################################################
#     
class Editevents(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            title=data['title']
            desc=data['desc']
            start_date=data['start_date']
            end_date=data['end_date']
            ids=data['id']
            pic=data['pic']
            data={"title":title,"desc":desc,"start_date":start_date,"end_date":end_date,"pic":pic,"id":ids}
            
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editevents(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN DELETE EVENTS--API FUNCTIONALITY                  #
######################################################################
def deleteevents(ids):                           
    userData = requests.post(
    deleteevents_api,json={"id":ids})            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN DELETE EVENTS--API GATEWAY                        #
######################################################################
   
class Deleteevents(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            ids=data['id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=deleteevents(ids)
                    return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid    
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN GET EVENTS--API FUNCTIONALITY                  #
######################################################################
def getevents(data):                           
    userData = requests.post(
    getevents_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

######################################################################
#        ADMIN GET EVENTS--API GATEWAY                        #
######################################################################
   
class Getevents(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            dtype=data['dtype']
            eventid=data['eventid']
            data={"dtype":dtype,"eventid":eventid}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=getevents(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

#FAQ

######################################################################
#        ADMIN ADD FAQ--API FUNCTIONALITY                     #
######################################################################
def add_faq(data):
                             
    userData = requests.post(
    addfaq_api,json=data)            
    userDataResponse=json.loads(userData.text)
     
    if userDataResponse.get('status')==200: 
        faqcache.clear()
        
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN ADD FAQ--API GATEWAY                          #
######################################################################
    
class Addfaq(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            answer=data['answer']
            question=data['question']
            data={"question":question,"answer":answer}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=add_faq(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN EDIT FAQ--API FUNCTIONALITY                           #
######################################################################
def editfaq(data):                           
    userData = requests.post(
    editfaq_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        faqcache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN EDIT FAQ--API GATEWAY                          #
######################################################################
#     
class Editfaq(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            answer=data['answer']
            question=data['question']
            f_id=data['f_id']
            data={"question":question,"answer":answer,"f_id":f_id}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editfaq(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN DELETE FAQ--API FUNCTIONALITY                  #
######################################################################
def deletefaq(f_id):                          
    userData = requests.post(
    deletefaq_api,json={"f_id":f_id})            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        faqcache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN DELETE FAQ--API GATEWAY                        #
######################################################################
   
class Deletefaq(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            f_id=data['f_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=deletefaq(f_id)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN GET FAQ--API FUNCTIONALITY                  #
######################################################################
def getfaq(f_id):                         
    userData = requests.post(
    getfaq_api,json={"f_id":f_id})            
    userDataResponse=json.loads(userData.text)
    # home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN GET FAQ--API GATEWAY                        #
######################################################################
   
class Getsfaq(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            f_id=data['f_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=getfaq(f_id)
                    return jsonify(response)  
                else:
                    return msg_403
            else:
                return session_invalid  
        except Exception as e:
            return jsonify(error)


#ABOUT US

######################################################################
#        ADMIN ADD ABOUT US--API FUNCTIONALITY                     #
######################################################################
def addaboutus(data):                          
    userData = requests.post(
    addaboutus_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN ADD ABOUT US--API GATEWAY                          #
######################################################################
    
class Addaboutus(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            desc=data['desc']
            data={"desc":desc}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=addaboutus(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN EDIT ABOUT US--API FUNCTIONALITY                    #
######################################################################
def editaboutus(data):                          
    userData = requests.post(
    editaboutus_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        # responses=get_home() 
        #home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN EDIT ABOUT US--API GATEWAY                          #
######################################################################
#     
class Editaboutus(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            abt_id=data['abt_id']
            desc=data['desc']
            
            data={"abt_id":abt_id,"desc":desc}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editaboutus(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)



######################################################################
#        ADMIN GET ABOUT US--API FUNCTIONALITY                  #
######################################################################
def getaboutus(abt_id):                        
    userData = requests.post(
    getaboutus_api,json={"abt_id":abt_id})            
    userDataResponse=json.loads(userData.text)
    # home api should call or not--not decided
    return userDataResponse

######################################################################
#        ADMIN GET ABOUT US--API GATEWAY                        #
######################################################################
   
class Getsaboutus(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            abt_id=data['abt_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=getaboutus(abt_id)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
######################################################################
#        ADMIN ADD ELIGIBILITY----API FUNCTIONALITY                  #
######################################################################
def addeligibility(data):                          
    userData = requests.post(
    add_eligibility_api,json=data)        
    userDataResponse=json.loads(userData.text)
    if userDataResponse.get('status')==200:
        
        cachequestion.clear()
        return userDataResponse       
    
    return userDataResponse
######################################################################
#        ADMIN ADD ELIGIBILITY----API GATEWAY                        #
######################################################################
class Addeligibility(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            pid=data['pid']
            question=data['question']
            answer=data['answer']
            is_mandatory=data['is_mandatory']
            data={"pid":pid,"question":question,"answer":answer,"is_mandatory":is_mandatory}
            
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=addeligibility(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN GET ELIGIBILITY----API FUNCTIONALITY                  #
######################################################################
def geteligibility(data):                           
    userData = requests.post(
    get_eligibility_api,json=data)            
    userDataResponse=json.loads(userData.text)
    return userDataResponse
######################################################################
#        ADMIN GET ELIGIBILITY----API GATEWAY                        #
######################################################################
class Geteligibility(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            pid=data['pid']
            if 'elg_id' in data:
                elg_id=data['elg_id']
                data={"pid":pid,"elg_id":elg_id}
            else:
                data={"pid":pid}
            
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=geteligibility(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
######################################################################
#        ADMIN EDIT ELIGIBILITY----API FUNCTIONALITY                  #
######################################################################
def editeligibility(data):                        
    userData = requests.post(
    edit_eligibility_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        cachequestion.clear()
        return userDataResponse
    return userDataResponse
######################################################################
#        ADMIN EDIT ELIGIBILITY----API GATEWAY                        #
######################################################################
class Editeligibility(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            pid=data['pid']
            elg_id=data['elg_id']
            question=data['question']
            answer=data['answer']
            is_mandatory=data['is_mandatory']
            data={"pid":pid,"elg_id":elg_id,"question":question,"answer":answer,"is_mandatory":is_mandatory}
            
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editeligibility(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
######################################################################
#        ADMIN DELETE ELIGIBILITY----API FUNCTIONALITY                  #
######################################################################
def deleteeligibility(data):                           
    userData = requests.post(
    delete_eligibility_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear() 
        cachequestion.clear()
        return userDataResponse
    return userDataResponse
######################################################################
#        ADMIN DELETE ELIGIBILITY----API GATEWAY                        #
######################################################################
class Deleteeligibility(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            pid=data['pid']
            elg_id=data['elg_id']
          
            data={"pid":pid,"elg_id":elg_id}
            
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=deleteeligibility(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
######################################################################
#        ADMIN ADD PROGRAMME----API FUNCTIONALITY                  #
######################################################################
def addprogramme(data,dtype):                                 
    userData = requests.post(
    add_programme_api,json=data)            
    userDataResponse=json.loads(userData.text)
    if userDataResponse.get('status')==200:
        programcache.clear()            
        responses=get_programmes(dtype) 
        homeDataResponse=json.loads(responses.text)
        return userDataResponse        
    else:
        return userDataResponse
##########################################################
#DELETE
###########################################################
def deleteaddprogramme_admission(data):                         
    userData = requests.post(
    delete_programme_api,json={"pid":data})            
    userDataResponse=json.loads(userData.text)
    return userDataResponse

######################################################################
#        ADMIN ADD PROGRAMME----API FUNCTIONALITY  Admission         #
######################################################################
def addprogramme_admission(data):                           
    userData = requests.post(
    add_programme_api_adm,json=data)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        print(userDataResponse)
    return userDataResponse

######################################################################
#       ADMIN ADD PROGRAMME----API GATEWAY                        #
######################################################################
class Addprogramme(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            prg_code=data['prg_code']
            title=data['title']
            desc=data['desc']
            dept_id=data['dept_id']
            structure=data['structure']
            syllabus=data['syllabus']
            brochure=data['brochure']
            dtype=data['dtype']
            thumbnail=data['thumbnail']
            eligibility=data['eligibility'] 
            prgtype=data['prgtype'] 
            no_of_semester=data['no_of_semester']     
            data={"prg_code":prg_code,"title":title,"desc":desc,"dept_id":dept_id,
            "structure":structure,"syllabus":syllabus,"brochure":brochure,"thumbnail":thumbnail,"eligibility":eligibility,
            "prgtype":prgtype,"no_of_semester":no_of_semester}             
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=addprogramme(data,dtype)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
######################################################################
#       PROGRAMME SPECIFIC SEMESTER COUNT----API  GATEWAY             #
######################################################################
class ProgramSemesterList(Resource):
    def post(self):
        try:   
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            pid=content['pid']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=prgm_semester(pid)
                    return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return error


def prgm_semester(pid):
    homeData = requests.post(prgm_semester_backendapi,json={"pid":pid})
    homeDataResponse=json.loads(homeData.text)
    return homeDataResponse  

api.add_resource(ProgramSemesterList, '/api/prgm_semester_list')

######################################################################
#       PAYMENT GATEWAY IMPLEMENTATION  ----API  GATEWAY             #
######################################################################


class PaymentGateway(Resource):
    def post(self):
        try:   
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            pid=content['pid']
            batch_id=content['batch_id']
            amount=content['amount']
            se=checkSessionValidity(session_id,user_id)
            if se:
                # per=checkapipermission(user_id,self.__class__.__name__)
                # if per
                userPrfl=UserProfile.query.filter_by(uid=user_id).first()
                name=userPrfl.fullname
                response=payment_gateway(amount,user_id,pid,batch_id,name)
                return jsonify(response)
                # else:
                #     return msg_403
            else:
                return session_invalid
        except Exception as e:
            return error


def payment_gateway(data,user_id,pid,batch_id,name):
    # homeData = requests.get(payment_gateway_backendapi)
    # homeDataResponse=json.loads(homeData.text)
    homeData = requests.post(payment_gateway_backendapi,json={"amount":data,"user_id":user_id,"pid":pid,"batch_id":batch_id,"user_name":name})
    homeDataResponse=json.loads(homeData.text)
    return homeDataResponse  

api.add_resource(PaymentGateway, '/api/payment')



class PaymentReceipt(Resource):
    def post(self):        
        try:   
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            txn_id=content['txn_id']
            batch_id=content['batch_id']
            prgm_id=content['prgm_id']
            
            se=checkSessionValidity(session_id,user_id)
            if se:
                # per=checkapipermission(user_id,self.__class__.__name__)
                # if per:
                response=payment_receipt(txn_id,prgm_id,user_id,batch_id)
                
                return jsonify(response)
                # else:
                #     return msg_403
            else:
                return session_invalid
        except Exception as e:
            
            return error



# def payment_receipt(txn_id,prgm_id,user_id,batch_id):
    # # homeData = requests.get(payment_gateway_backendapi)
    # # homeDataResponse=json.loads(homeData.text)
    # data={"txn_id":txn_id,"prgm_id":prgm_id,"user_id":user_id,"batch_id":batch_id}
    # homeData = requests.post(payment_receipt_backendapi,json=data)
    # homeDataResponse=json.loads(homeData.text)
    # return homeDataResponse


def payment_receipt(txn_id,prgm_id,user_id,batch_id):
    
    userPrfl=UserProfile.query.filter_by(uid=user_id).first()
    name=userPrfl.fullname
    
    # userName={"name":name}
    data={"txn_id":txn_id,"prgm_id":prgm_id,"user_id":user_id,"name":name,"batch_id":batch_id}
    homeData = requests.post(payment_receipt_backendapi,json=data)
    homeDataResponse=json.loads(homeData.text)
    # print(homeData)
    # paymentResult=homeDataResponse.get("message")
    # paymentResult.append(userName)
    # print(paymentResult)
    if len(homeDataResponse.get('message'))==0:
        return homeDataResponse

    if homeDataResponse.get('status')==200 and homeDataResponse.get('message')[0].get('res_code')=="01":
        send_transaction_successemail(user_id)
        send_transaction_successsms(user_id)

    return homeDataResponse


class TestGateway(Resource):
    def post(self):
        send_transaction_successemail()
        return "true"

def send_transaction_successsms(user_id):
    sms_url = "http://api.esms.kerala.gov.in/fastclient/SMSclient.php" 
    user_details=UserProfile.query.filter_by(uid=user_id).first()
    name= user_details.fullname
    phone=user_details.phno
    message="Hi %s \n Your payment has been successfully completed.  \n\nTeam DASP"%(name)
    querystring = {"username":"mguegov-mguniv-cer","password":"mguecert","message":message,"numbers":phone,"senderid":"MGEGOV"}
    response = requests.request("GET", sms_url,  params=querystring)
    

def send_transaction_successemail(user_id):

    user_details=User.query.filter_by(id=user_id).first()
    # mail_data=txn_data
    host='smtp.gmail.com' 
    port=587

    email=mg_email
    password=mg_password
    context = ssl.create_default_context()
    subject="DASP Payment Successfull "
    mail_to=user_details.email
    mail_from=email
    body="Hi,\n\n Your payment has been successfully completed.  \n \n Team DASP  \n\n\n\n THIS IS A SYSTEM GENERATED EMAIL - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL"
    message = """From: %s\nTo:  %s\nSubject: %s\n\n%s""" % (mail_from, mail_to,  subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()        
        server.starttls(context=context)
        server.ehlo()
        server.login(email, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return 1
    except Exception as ex:
        return 0
    
api.add_resource(TestGateway, '/api/testmail')

api.add_resource(PaymentReceipt, '/api/receipt')

# def payment_response(user_id,prgm_id,response):
#     cur_date=datetime.now()
    
#     for i in response:
#         paymentdata=PaymentHistory(user_id=user_id,prgm_id=prgm_id,applicant_no=i.get("applicant_no"),order_id=i.get("ORDERID"),
#         trans_id=i.get("TXNID"),trans_amount=i.get("TXNAMOUNT"),trans_date=cur_date,res_code=i.get("RESPCODE"),status=i.get("STATUS"))
#         db.session.add(paymentdata)
#         db.session.commit()
#         if (i.get("RESPCODE"))=="01":
#             data={"userid":user_id,"transid":i.get("TXNID"),"prgid":prgm_id}
#             response=transaction(data)
#             return response
            

class Paymenthistory(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            batch_id=data['batch_id']
            prgm_id=data['prgm_id']
            student_id=data['student_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
               
                response=stud_payment(batch_id,prgm_id,student_id)
                msg=response.get("message")
                paymentdic=msg.get("paymentDetails")
                for i in paymentdic:
                    user=db.session.query(User,UserProfile).with_entities(User.id.label("user_id"),UserProfile.fullname.label("name"),User.email.label("email")).filter(User.id==i.get("user_id"),User.id==UserProfile.uid).order_by(UserProfile.fname).all()
                    userData=list(map(lambda n:n._asdict(),user))
                    i['user_dtls']=userData
                return jsonify(response)

              
            else:
                return session_invalid
        except Exception as e:
            print(e)
            return jsonify(error)

def stud_payment(batch_id,prgm_id,student_id):                       
    userData = requests.post(
    paymenthistory_backendapi,json={"batch_id":batch_id,"pid":prgm_id,"student_id":student_id})            
    userDataResponse=json.loads(userData.text)
    return userDataResponse  
######################################################################
#        ADMIN PAYMENT HISTORY----API FUNCTIONALITY                  #
######################################################################

class Adminpaymenthistory(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            batch_id=data['batch_id']
            student_id=data['student_id']
            prgm_id=data['prgm_id']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=admin_payment(batch_id,prgm_id,student_id)
                    msg=response.get("message")
                    paymentdic=msg.get("paymentDetails")
                    
                    if paymentdic!=[]:
                        for i in paymentdic:
                            user=db.session.query(User,UserProfile).with_entities(User.id.label("user_id"),UserProfile.fullname.label("name"),UserProfile.phno.label("phno"),User.email.label("email"),UserProfile.nationality.label("nationality")).filter(User.id==i.get("user_id"),User.id==UserProfile.uid).order_by(UserProfile.fname).all()
                            userData=list(map(lambda n:n._asdict(),user))
                            i['user_dtls']=userData
                            # print(userData)
                            # i['user_name']=userData[0]['name']
                            # i['email']=userData[0]['email']
                            # i['phno']=userData[0]['phno']
                            # i['nationality']=userData[0]['nationality']

                        return jsonify(response)
                    else:
                        return jsonify(response)
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)

def admin_payment(batch_id,prgm_id,student_id):                       
    userData = requests.post(
    paymenthistory_backendapi,json={"batch_id":batch_id,"pid":prgm_id,"student_id":student_id})            
    userDataResponse=json.loads(userData.text)
    return userDataResponse 

######################################################################
#        PAYMENT TRACKER----API FUNCTIONALITY                  #
######################################################################

class PaymentTracker(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['userId']
            session_id=data['sessionId']
            trans_date=data['transDate']
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    paymentResp=payment_tracker(trans_date)
                    # print(paymentResp)
                    userList=[]
                    usr_list=paymentResp.get("data")
                    if usr_list!=[]:
                        for usr in usr_list:
                            user=db.session.query(User,UserProfile).with_entities(User.id.label("user_id"),UserProfile.fullname.label("name")).filter(User.id==usr.get("userId"),User.id==UserProfile.uid).order_by(UserProfile.fname).all()
                            
                            userData=list(map(lambda n:n._asdict(),user))
                            usr['userName']=userData[0].get('name')
                            userList.append(usr)
                            print(userList)
                        return format_response(True,"Successfully fetched",userList)
                else:
                    return format_response(False,"Forbidden access",{},403)
            else:
                return format_response(False,"Unauthorised access",{},401)
        except Exception as e:
            print(e)
            return format_response(False,"Bad gateway",{},502)
  
######################################################################
#     PAYMENT TRACKER    ----API FUNCTIONALITY                       #
######################################################################         

def payment_tracker(trans_date):                     
    userData = requests.post(
    paymenttracker_backendapi,json={"date":trans_date})            
    userDataResponse=json.loads(userData.text)
    return userDataResponse 



######################################################################
#        ADMIN ADD Batch----API FUNCTIONALITY                  #
######################################################################
def addbatch(data,pid,dtype):   
                                
    userData = requests.post(
    add_batch_api,json=data)            
    userDataResponse=json.loads(userData.text)
    if userDataResponse.get('status')==200:
        cache.clear()
        programcache.clear()
        singleprogramcache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse        
            
    else:
        return userDataResponse
##########################################################
#DELETE
###########################################################
def deleteaddbatch_admission(pid,bid):                       
    userData = requests.post(
    delete_batch_api,json={"pgm_id":pid,"b_id":bid})            
    userDataResponse=json.loads(userData.text)
    return userDataResponse

######################################################################
#        ADMIN ADD batch----API FUNCTIONALITY  Admission         #
######################################################################
def addbatch_admission(data):                           
    userData = requests.post(
    add_batch_api_adm,json=data)            
    userDataResponse=json.loads(userData.text)
    return userDataResponse

######################################################################
#       ADMIN ADD PROGRAMME----API GATEWAY                        #
######################################################################
class Addbatch(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            pgm_id=data['pgm_id']
            dtype=data['dtype']

            std_id=data['std_id']
            pgm_fee=data['pgm_fee']
            no_seats=data['no_seats']
            appl_start_date=data['appl_start_date']
            appl_end_date=data['appl_end_date']
            class_start_date=data['class_start_date']
            class_end_date=data['class_end_date']  
            batch_dis_name=data['batch_dis_name']         
            data={
                        "pgm_id":pgm_id,"std_id":std_id,"pgm_fee":pgm_fee,
                    "no_seats":no_seats,"appl_start_date":appl_start_date,"appl_end_date":appl_end_date,
                    "class_start_date":class_start_date,"class_end_date":class_end_date,"batch_dis_name":batch_dis_name
            }        
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=addbatch(data,pgm_id,dtype)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

######################################################################
#        ADMIN EDIT Batch----API FUNCTIONALITY                  #
######################################################################
def editbatch(data,pid,dtype):                          
    userData = requests.post(
    edit_batch_api,json=data)            
    userDataResponse=json.loads(userData.text)
    if userDataResponse.get('status')==200:
        cache.clear()
        programcache.clear()
        singleprogramcache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse
        
    else:
        return userDataResponse
##########################################################
#DELETE
###########################################################
def deleteeditbatch_admission(pid,bid):                          
    userData = requests.post(
    delete_batch_api,json={"pgm_id":pid,"b_id":bid})            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

######################################################################
#        ADMIN EDIT batch----API FUNCTIONALITY  Admission         #
######################################################################
def editbatch_admission(data):   
    # token=gettoken() 
    # print(data)
    # # data=jsonify(data)
    # # data1={"status":"abcd","message":"hai"}
    # print(type(data))
    # headers = {'content-type': 'application/json','authorization':token}                            
    userData = requests.post(
    edit_batch_api_adm,json=data)            
    userDataResponse=json.loads(userData.text) 
    # print(userDataResponse)
    return userDataResponse

######################################################################
#       ADMIN EDIT BATCH----API GATEWAY                        #
######################################################################
class Editbatch(Resource):
    def post(self):
        try:
            # print("hello")
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            pgm_id=data['pgm_id']
            dtype=data['dtype']
            std_id=data['std_id']
            b_id=data['b_id']
            b_name=data['b_name']
            pgm_fee=data['pgm_fee']
            no_seats=data['no_seats']
            appl_start_date=data['appl_start_date']
            appl_end_date=data['appl_end_date']
            class_start_date=data['class_start_date']
            class_end_date=data['class_end_date']
            batch_dis_name=data['batch_dis_name']
            data={
                        "pgm_id":pgm_id,"std_id":std_id,"pgm_fee":pgm_fee,
                    "no_seats":no_seats,"appl_start_date":appl_start_date,"appl_end_date":appl_end_date,
                    "class_start_date":class_start_date,"class_end_date":class_end_date,"b_name":b_name,"b_id":b_id,
                    "batch_dis_name":batch_dis_name
            }           
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editbatch(data,pgm_id,dtype)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)

#######################################################
#     GET ALL  BATCH-API FUNCTIONALITY
#######################################################
def getallbatch():                            
    userData = requests.get(
    getallbatch_api)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#     GET ALL BATCH-API GATEWAY
#######################################################
class Getallbatch(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                
                
                
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=getallbatch()
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)

######################################################################
#        ADMIN EDIT PROGRAMME----API FUNCTIONALITY                  #
######################################################################
def editprogramme(data,dtype,pid):                          
    userData = requests.post(
    edit_programme_api,json=data)          
    userDataResponse=json.loads(userData.text)
    if userDataResponse.get('status')==200:
        programcache.clear()
        singleprogramcache.clear()
        cache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse        
        
    else:
        return userDataResponse
##########################################################
#DELETE
###########################################################
def deleteprogramme_admission(data):                         
    userData = requests.post(
    delete_programme_api,json={"pid":data})            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse
######################################################################
#        ADMIN EDIT PROGRAMME----API FUNCTIONALITY  Admission         #
######################################################################
def editprogramme_admission(data):                           
    userData = requests.post(
    edit_programme_api_adm,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse



######################################################################
#       ADMIN EDIT PROGRAMME----API GATEWAY                        #
######################################################################
class Editprogramme(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            prg_code=data['prg_code']
            title=data['title']
            desc=data['desc']
            dept_id=data['dept_id']
            dtype=data['dtype']
            structure=data['structure']
            syllabus=data['syllabus']
            brochure=data['brochure']
            thumbnail=data['thumbnail']
            eligibility=data['eligibility']          
            pid=data['pid']
            #no_of_semester=data['no_of_semester']
           
            
            data={"prg_code":prg_code,"title":title,"desc":desc,"dept_id":dept_id,
            "structure":structure,"syllabus":syllabus,"brochure":brochure,
            "thumbnail":thumbnail,"eligibility":eligibility,"pid":pid}
 
            
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=editprogramme(data,dtype,pid)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
#######################################################
#     GET SINGLE BATCH-API FUNCTIONALITY
#######################################################
def getsinglebatch(data):
   
                              
    userData = requests.post(
    getsinglebatch_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    
    return userDataResponse

#######################################################
#     GET SINGLE BATCH-API GATEWAY
#######################################################
class Getsinglebatch(Resource):
    def post(self):
            try:
                
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                pgm_id=data['pgm_id']
                b_id=data['b_id']
                
                data={"pgm_id":pgm_id,"b_id":b_id}
                
                se=checkSessionValidity(session_id,user_id)
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=getsinglebatch(data)
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)

#######################################################
#     CHANGE BATCH STATUS-API FUNCTIONALITY
#######################################################
def batchstatuschange(data):                       
    userData = requests.post(
    batchstatuschange_api,json=data)            
    userDataResponse=json.loads(userData.text)
    if userDataResponse.get('status')==200:
        cache.clear()
        programcache.clear()
        singleprogramcache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse        
            
    else:
        return userDataResponse 
#######################################################
#     CHANGE BATCH STATUS-API FUNCTIONALITY--admmission
#######################################################
def batchstatuschange_admission(data):
   
    # token=gettoken()
    
    # data1={"bid":data.get('bid'),"batch_status":data.get('batch_status')}

    # headers = {'content-type': 'application/json','authorization':token}                            
    userData1 = requests.post(
    batchstatuschange_admission_api,json=data1)            
    userDataResponse1=json.loads(userData1.text) 
    if userDataResponse1.get('status')==200:
        # print(userDataResponse1)
        cache.clear()
        programcache.clear()
        singleprogramcache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse1
       
    else:
        # token=info_token_fetch()
        infodata={"bid":data.get('bid'),"status":data.get('old_status')}
        # print(infodata)
        # headers = {'content-type': 'application/json','authorization':token}                            
        userData = requests.post(
        batchstatuschange_api,json=infodata)            
        userDataResponse=json.loads(userData.text)
        return {"status":304,"message":"something went wrong!.."}
       
        #home api should call or not--not decided
    # print(userDataResponse)
    return userDataResponse1
#######################################################
#     CHANGE BATCH STATUS-API GATEWAY
#######################################################
class Batchstatuschange(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                bid=data['bid']
                status=data['status']
                
                data={"bid":bid,"status":status}
                
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=batchstatuschange(data)
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)


#######################################################
#     CHANGE BATCH STATUS-API FUNCTIONALITY
#######################################################
def programmestatuschange(data):                          
    userData = requests.post(
    programmestatuschange_api,json=data) 

    userDataResponse=json.loads(userData.text)

    if userDataResponse.get('status')==200:
        cache.clear()
        programcache.clear()
        singleprogramcache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse
    else:
        return  userDataResponse
   
#######################################################
#     CHANGE BATCH STATUS-API FUNCTIONALITY--admmission
#######################################################
def programmestatuschange_admission(data):
    data1={"pid":data.get('pid'),"prg_status":data.get('prg_status')}                         
    userData = requests.post(
    programmestatuschange_admission_api,json=data1)            
    userDataResponse=json.loads(userData.text) 
    if userDataResponse.get('status')==200:
        cache.clear()
        programcache.clear()
        singleprogramcache.clear()
        upcomingprogramcache.clear()
        ongoingprogramcache.clear()
        return userDataResponse
    else:
        infodata={"pid":data.get('pid'),"status":data.get('old_status')}                          
        userData = requests.post(
        programmestatuschange_api,json=infodata)            
        userDataResponse=json.loads(userData.text)
        return {"status":304,"message":"something went wrong!.."}
       
        #home api should call or not--not decided
    
    # return userDataResponse
#######################################################
#     CHANGE BATCH STATUS-API GATEWAY
#######################################################
class Programmestatuschange(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                pid=data['pid']
                status=data['status']
                
                data={"pid":pid,"status":status}
               
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=programmestatuschange(data)
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)


#######################################################
#     GET SINGLE BATCH-API FUNCTIONALITY
#######################################################
def getallprogramme_and_dept():                           
    userData = requests.get(
    getallprogramme_and_dept_api)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#     GET SINGLE BATCH-API GATEWAY
#######################################################
class Getallprogramme_and_dept(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
               
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=getallprogramme_and_dept()
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)
#######################################################
# LIST OF ALL TEACHERS----API FUNCTIONALITY           #
#######################################################
def allteacherlist():
    user=db.session.query(RoleMapping,UserProfile,User).with_entities(RoleMapping.user_id.label("user_id"),UserProfile.fname.label("fname"),UserProfile.lname.label("lname"),User.email.label("email"),UserProfile.phno.label("phone")).filter(RoleMapping.role_id==13,UserProfile.uid==RoleMapping.user_id,User.id==RoleMapping.user_id).all()
   
    userData=list(map(lambda n:n._asdict(),user))
    userDictList={"status":200,"teacher_list":userData}
    return userDictList

#####################################################
# LIST OF ALL TEACHERS----API GATEWAY
#######################################################   

class Allteacherlist(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
               
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=allteacherlist()
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)


####################################################################
# TEACHER REJECT  -API FUNCTIONALITY                               #
####################################################################


class TeacherReject(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                teacher_id=data['teacher_id']
                status=data['status']
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=teacher_reject(teacher_id,status)
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)


def teacher_reject(teacher_id,status):
    teacherObj=teacher.query.filter_by(id=teacher_id).first()
    if teacherObj!=None:
        teacherObj.status=status
        db.session.commit()
        return format_response(True,"Updated successfully",{},200)
    else:
        return format_response(False, "Invalid techer_id", {}, 400)

###################################################################
# PAYMENT RESPONSE -API FUNCTIONALITY
####################################################################
def transaction(data):
    homeData = requests.post(
    addapplicant,json=data)
    homeDataResponse=json.loads(homeData.text)
    return homeDataResponse
###################################################################
# PAYMENT RESPONSE -API GATEWAY
###############################################################
class Transaction(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                transaction_id=data['transaction_id']
                prgid=data['prgid']
                data1={"userid":user_id,"transid":transaction_id,"prgid":prgid}
                se=checkSessionValidity(session_id,user_id) 
                if se:
                   
                    response=transaction(data1)
                    return jsonify(response) 
                
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)


#######################################################
# LIST OF ALL TEACHERS----API GATEWAY
#######################################################   

def assignteacher(course_id,teacher_id,batch_id):
    roles=RoleMapping.query.filter_by(user_id=teacher_id).all()
    roles = [r.role_id for r in roles] 
    perm_list=Role.query.filter(Role.id.in_(roles)).all()
    flag=0
    for i in perm_list:
        if i.role_name=="Teacher" or i.role_name=="LMS":
            flag=1
            break
    if flag==1:  
        tc_map=TeacherCourseMapping.query.filter_by(teacher_id=teacher_id,course_id=course_id,batch_id=batch_id).first()    
        if tc_map==None:
            teach_course_map=TeacherCourseMapping(teacher_id=teacher_id,course_id=course_id,batch_id=batch_id)
            db.session.add(teach_course_map)
            db.session.commit()
            return teacherassigned
        else:
            return alreadyassigned
    else:
        return invaliduser

class Assignteacher(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']  
            course_id=data['course_id']
            teacher_id=data['teacher_id'] 
            batch_id=data['batch_id']           
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=assignteacher(course_id,teacher_id,batch_id)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)
################################################################
#####               Listing teachers_name                 #####
################################################################


class Listingteachersname(Resource):
    def post(self):
        try:
            content=request.get_json()
            user_id=content['user_id']
            session_id=content['session_id']
            teacherlist=[]
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    roles=Role.query.filter_by(role_name="LMS").first()
                    role_map=RoleMapping.query.filter_by(role_id=roles.id).all()
                    for i in role_map:
                        usrprfl=UserProfile.query.filter_by(uid=i.user_id).first()
                        teacherdic={"user_id":usrprfl.uid,"first_name":usrprfl.fname,"last_name":usrprfl.lname}
                        teacherlist.append(teacherdic)
                    return {"status":200,"teachersname":teacherlist}
                else:
                    return msg_403
            else:
                return session_invalid  
        except Exception as e:
            return jsonify(error)


###########################################################################
#   function for  Fetching course name_underbatch                         #
###########################################################################

def fetch_course(batch_id1):                          
    userData = requests.post(fetch_course_name,json={"batch_id":batch_id1})            
    userDataResponse=json.loads(userData.text)
    return userDataResponse 

###########################################################################
#    Fetching course name_underbatch                                      #
###########################################################################

class Fetchcoursename(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            batch_id=data['batch_id']
            se=checkSessionValidity(session_id,user_id)
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=fetch_course(batch_id)
                    print(response)
                    msg=response.get("message")
                    for i in msg.get("coursedetails"):
                        # teacherDet=TeacherCourseMapping.query.filter_by(batch_id=batch_id,course_id=i.get("couse_id").all()
                        teacherDet=db.session.query(TeacherCourseMapping,UserProfile,User).with_entities(UserProfile.fname.label("fname"),UserProfile.lname.label("lname")).filter(TeacherCourseMapping.batch_id==batch_id,TeacherCourseMapping.course_id==i.get("couse_id"),User.id==TeacherCourseMapping.teacher_id,UserProfile.uid==User.id).all()
                        teacherDet=list(map(lambda n:n._asdict(),teacherDet))
                        i["teacherDet"]=teacherDet
                    return jsonify(response)
                else:
                    return msg_403    
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)
 
 ###########################################################################
#   function for    list courses_assigned for techer                        #
###########################################################################

def listteacherforcourse(teacheridlist):
    teacher=[]
    for i in teacheridlist:  
        teacherdata=UserProfile.query.filter_by(uid=i).first()
        tdata={"uid":teacherdata.uid,"fname":teacherdata.fname,"lname":teacherdata.lname}
        teacher.append(tdata)
    userDataResponse={"status":200,"teachersname":teacher}
    return userDataResponse 
           
###########################################################################
#                   list Teachers assigned for course                     #
###########################################################################

class Listteacherassignedforcourse(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            course_id=data['course_id']
            batch_id=data['batch_id']
            se=checkSessionValidity(session_id,user_id)
            teacheridlist=[]
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    teacherlist=TeacherCourseMapping.query.filter_by(course_id=course_id,batch_id=batch_id).all()
                    if teacherlist!=[]:
                        for i in teacherlist: 
                            teacheridlist.append(i.teacher_id)
                        response=listteacherforcourse(teacheridlist)
                        return jsonify(response) 
                    else:
                        return {"status":200,"teachersname":[]}
                else:
                    return msg_403 
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)

###########################################################################
#   function for    list courses_assigned for techer                      #
###########################################################################

def listcourse(batchlist):                         
    userData = requests.post(
    fetch_course_teacherbatch,json={"batch_id":batchlist})            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse 

###########################################################################
#    list courses_assigned for techer                                     #
###########################################################################

class Listcourseassignedforteacher(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            teacher_id1=data['teacher_id']
            se=checkSessionValidity(session_id,user_id)
            batchlist=[]
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    batch=TeacherCourseMapping.query.filter_by(teacher_id=teacher_id1).all()
                    if batch!=[]:
                        for i in batch: 
                            batchlist.append(i.batch_id)
                        response=listcourse(batchlist)
                        return jsonify(response) 
                    else:
                        return nobatchfound
                else:
                    return msg_403 
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)

#######################################################
#     ADD COURSE STRUCTURE-API FUNCTIONALITY          #
#######################################################
def addcourse(data):                           
    userData = requests.post(
    add_course_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#     ADD COURSE STRUCTURE-API GATEWAY                #
#######################################################
class AddCoursestucture(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                c_code=data['c_code']
                c_name=data["cname"]
                credit=data['credit']
                intmark=data["internal_mark"]
                extmark=data["external_mark"]
                tmark=data["total_mark"]
                data={"course_code":c_code,"course_name":c_name,
                "credit":credit,"internal_mark":intmark,"external_mark":extmark,"total_mark":tmark} 
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=addcourse(data) 
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)
#######################################################
#     EDIT  COURSE STRUCTURE-API FUNCTIONALITY        #
#######################################################
def editcourse(data):                        
    userData = requests.post(
    edit_course_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#      EDIT  COURSE STRUCTURE-API GATEWAY       #
#######################################################
class EditCourseStucture(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                c_id=data['c_id']
                c_name=data["cname"]
                credit=data['credit']
                intmark=data["internal_mark"]
                extmark=data["external_mark"]
                tmark=data["total_mark"] 
                data={"course_id":c_id,"course_name":c_name,
                "credit":credit,"internal_mark":intmark,"external_mark":extmark,"total_mark":tmark} 
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=editcourse(data)                        
                        singleprogramcache.clear()
                        cache.clear()
                        upcomingprogramcache.clear()
                        ongoingprogramcache.clear()
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)
#######################################################
#     GET ALL COURSE STRUCTURE-API FUNCTIONALITY      #
#######################################################
def getallcourse():                          
    userData = requests.get(get_all_course_api )            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#     GET ALL COURSE STRUCTURE-API FUNCTIONALITY      #
#######################################################
class GetAllCourseStucture(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=getallcourse()
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)
#######################################################
#     GET SINGLE COURSE STRUCTURE-API FUNCTIONALITY   #
#######################################################
def getsinglecourse(data):                        
    userData = requests.post(
    get_single_course_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#    GET SINGLE COURSE STRUCTURE-API FUNCTIONALITY    #
#######################################################
class GetSingleCourseStucture(Resource):
    def post(self):
            try:
                data=request.get_json()
                user_id=data['user_id']
                session_id=data['session_id']
                c_id=data['c_id']
                data={"course_id":c_id} 
                se=checkSessionValidity(session_id,user_id) 
                if se:
                    per=checkapipermission(user_id,self.__class__.__name__)
                    if per:
                        response=getsinglecourse(data)
                        return jsonify(response) 
                    else:
                        return msg_403
                else:
                    return session_invalid   
            except Exception as e:
                return jsonify(error)

###################################################################################################################
#######                                           Teacher dashboard                                   #############
###################################################################################################################

###########################################################
#      COURSES ASSIGNED FOR A TEACHER-API FUNCTIONALITY   #
###########################################################
def get_assigned_courses(data):                           
    userData = requests.post(
    get_teacher_course_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

#######################################################
#     COURSES ASSIGNED FOR A TEACHER-API GATEWAY      #
#######################################################
class GetTeacherCourses(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            batch_id=data['batch_id']
            trbatchobj=TeacherCourseMapping.query.filter_by(teacher_id=user_id,batch_id=batch_id).all()
            course_id_list=[]
            for i in trbatchobj:
                course_id_list.append(i.course_id)
            data={"course_id":course_id_list} 
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=get_assigned_courses(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)


###########################################################
#      COURSES PRGM MAPPING-API FUNCTIONALITY             #
###########################################################
def course_prgm(data):                          
    userData = requests.post(
    course_prgm_mapping,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse


#######################################################
#    COURSE PRGM MAPPING                              #
#######################################################

class Course_pgm_mapping(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            course_id1=data['course_id']
            prg_id1=data['prg_id']
            data={"course_id":course_id1,"prg_id":prg_id1}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=course_prgm(data)                      
                    singleprogramcache.clear()
                    cache.clear()
                    upcomingprogramcache.clear()
                    ongoingprogramcache.clear()
                    return response
                else:
                    return msg_403
            else:
                return session_invalid   

        except Exception as e:
            return jsonify(error)

###########################################################
#      COURSES UNLINK-API FUNCTIONALITY             #
###########################################################
def course_unlink(data):                           
    userData = requests.post(
    course_unlink_api,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse
#######################################################
#    COURSE UNLINK API                                 #
#######################################################
class CourseUnlink(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            course_id1=data['course_id']
            prg_id1=data['program_id']
            data={"course_id":course_id1,"program_id":prg_id1}
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=course_unlink(data)                 
                    singleprogramcache.clear()
                    cache.clear()
                    upcomingprogramcache.clear()
                    ongoingprogramcache.clear()
                    return response
                else:
                    return msg_403
            else:
                return session_invalid   

        except Exception as e:
            return jsonify(error)

# ############################################################# #
#               BULK BATCH DETAILS ADD TO LMS                   #
# ############################################################# #
# def reg_bulkdata(data):                          
#     userData = requests.post(
#     fetch_course_name,json=data)            
#     userDataResponse=json.loads(userData.text) 
#     return userDataResponse

# def bulkstud_data(data):                         
#     userData = requests.post(
#     lists_backendapi,json=data)            
#     userDataResponse=json.loads(userData.text) 
#     return userDataResponse
# def bulk_requestfn(data):
#     response=reg_bulkdata(data)
#     studresponse1=bulkstud_data(data)
#     msg1=studresponse1.get('message')
#     list1=[]
#     if 'Users' in msg1:
#         userdtls=msg1.get('Users')
#         for i in userdtls:
#             if i.get("status")=='student':
#                 user1=UserProfile.query.filter_by(uid=i.get("user_id")).first()
#                 user=User.query.filter_by(id=i.get("user_id")).first()
#                 stud={"externalId":user.id,"email":user.email,"mobile":user1.phno,"admissionNo":i.get("applicantid"),"firstName":user1.fname,"lastName":user1.lname,"sex":user1.gender,"guardianPhone":"","guardianName":""}
#                 list1.append(stud)
#     msg=response.get('message')
#     batchdet=msg.get('batchdetails')
#     coursedet=msg.get('coursedetails')
#     clist=[]
#     for i in coursedet:
#         cdic={
#             "externalId":i.get("couse_id"),
#             "courseDetails": [
#                 {
#                     "removable": False,
#                     "title":"Course Benefits",
#                     "value": "",
#                     "template": "DynamicFields/editor.html",
#                     "type": "content",
#                     "help": "A short description of the Course(Optional, recommended)"
#                 }
#             ],
#             "type": "course",
#             "Name":i.get("name"),
#             "Duration": {
#                 "DurationDetails": {
#                     "Year(s)": 1
#                 }
#             }
#         }
#         clist.append(cdic)
#         cid=i.get("couse_id")
#         cmobj=LmsCourseMapping.query.filter_by(course_id=cid).first()
#         if cmobj!=None:
#             lms_c_id=cmobj.lms_c_id
#             cdic["lmsId"]=lms_c_id

#     dic={"external":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJOYW1lIjoiYWRtaW5AbWd1LmNvbSIsImNvbXBhbnlJZCI6IjVjNzY4NmFjNjQ5Nzk2MTQzNTEyMTk1MSIsInJvbGVJZCI6IjIiLCJ1c2VyRGV0YWlsc0lkIjoiNWNlY2RhNjI2NzhjZWYxNjYzZmM0MWQxIiwidXNlckxvZ2luSWQiOiI1Y2VjZGE2MTY3OGNlZjE2NjNmYzQxZDAiLCJwYXNzd29yZCI6Im1ndV9hZG1pbiIsInJvbGVNYXBwaW5nSWQiOiI1Y2VjZGE2MjY3OGNlZjE2NjNmYzQxZDIifX0.AqNwW3EMby9jR_cLBzmtPQWp4N32A00OlxW_rTXKWjY",
#     "batch": {
#         "batchObj": {
#             "externalId":"6",
#             "repeats": {
#                 "excludedDaysRepeat": []
#             },
#             "Admission": {
#                 "onBefore": "10",
#                 "beforeType": "Days",
#                 "onAfter": "10",
#                 "afterType": "Days",
#                 "beforeDaysCount": 10,
#                 "afterDaysCount": 10
#             },
#             "batchName":batchdet[0].get("name"),
#             "batchMode": "onetime",
#             "offline": True,
#             "instructorLead": True,
#             "startDate":batchdet[0].get("prg_start"),
#             "endDate":batchdet[0].get("prg_end"),
#             "seats":batchdet[0].get("seats"),
#             "materialAssignment": "manual",
#             "startTime": "1970-01-01T04:30:00.000Z",
#             "endTime": "1970-01-01T11:30:00.000Z",
#             "course": [],
#             "activeFlag": 1
#         }
#     },
#     "Courses":clist,
#     "Students":list1
#     }
#     # print(dic)
#     return dic


# def savetoken_todb(response1):
#     stud_det=response1.get('students')
#     for i in stud_det:
#         userobj=UserExtTokenMapping.query.filter_by(user_id=i.get('externalId')).all()
#         if userobj==[]:
#             userres=UserExtTokenMapping(user_id=i.get('externalId'),email_id=i.get('email'),
#             ext_token=i.get('external'))
#             db.session.add(userres)
#             db.session.commit()
#         else:
#             print("exist")
#     course_det=response1.get("courses")
#     for i in course_det:
#         courobj=LmsCourseMapping.query.filter_by(course_id=i.get('externalId')).all()
#         if courobj==[]:
#             courseres=LmsCourseMapping(course_id=i.get('externalId'),lms_c_id=i.get('lmsId'))
#             db.session.add(courseres)
#             db.session.commit()
#         else:
#             print("exist")
# ############################################################# #
#               BULK BATCH DETAILS ADD TO LMS                   #
# ############################################################# #
# class LmsBulkRegistration(Resource):
#     def post(self):
#         try:
#             data=request.get_json()
#             user_id=data['user_id']
#             session_id=data['session_id']
#             batch_id1=data['batch_id']
#             data={"batch_id":batch_id1}
#             bulk_request=bulk_requestfn(data)
#             bulk_request1=json.dumps(bulk_request)
#             token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InR5cGUiOiJjb21wYW55QXV0aCIsImNvbXBhbnlJZCI6IjVjNzY4NmFjNjQ5Nzk2MTQzNTEyMTk1MSJ9fQ.oADmwE7_J81Uo6VQRcPl3UGX08vcKE8mIWqkVLr4cRE"
#             headers = {'Content-Type': 'application/json','Authorization':token}
#             response1 = requests.post(bulkapi,json=json.loads(bulk_request1),headers=headers)
#             if response1=="failed":
#                 return {"status":200,"message":"LMS Already Enabled"}
#             resp=json.loads(response1.text)
#             resp=json.loads(resp)
#             savetoken_todb(resp)
#             return {"status":200,"message":"LMS Enabled"}
#         except Exception as e:
#             print(e)
#             return jsonify(error) 

# ############################################################# #
#        Function for fetch LMS id-functionality                #
# ############################################################# #

# def fetchlms_id(user_id,course_id):
#     user=UserExtTokenMapping.query.filter_by(user_id=user_id).first()
#     if user!=None:
#         external_token=user.ext_token
#     else:
#         return {"status":404,"message":"No Access"}
#     user1=LmsCourseMapping.query.filter_by(course_id=course_id).first()
#     if user1!=None:
#         lms_c_id=user1.lms_c_id
#     else:
#         return {"status":404,"message":"Invalid CourseId"}
#     dic={"external_token":external_token,"lms_c_id":lms_c_id}
#     return {"status":200,"message":dic}

# ############################################################# #
#               Function for fetch LMS id-API GATEWAY           #
# ############################################################# #

# class FetchLmscidandCourseid(Resource):
#     def post(self):
#         try:
#             data=request.get_json()
#             user_id=data['user_id']
#             session_id=data['session_id']  
#             course_id=data['course_id']           
#             se=checkSessionValidity(session_id,user_id) 
#             if se:
#                 response=fetchlms_id(user_id,course_id)
#                 return jsonify(response) 
#             else:
#                 return session_invalid   
#         except Exception as e:
#             return jsonify(error)

###########################################################
#      CHANGE STUDENT STATUS-API FUNCTIONALITY            #
###########################################################
def change_status(data):                         
    userData = requests.post(
    change_studentstatus,json=data)           
    userDataResponse=json.loads(userData.text)
    return userDataResponse

#######################################################
#     CHANGE STUDENT STATUS-API GATEWAY               #
#######################################################
class Changestudentstatus(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            student_id=data['student_id']
            session_id=data['session_id']
            batch_id=data['batch_id']
            prgm_id=data['prgm_id']
            data={
            "batchid":batch_id,
            "userid":student_id,
            "prgid":prgm_id
            }
            se=checkSessionValidity(session_id,user_id) 
            if se:
                per=checkapipermission(user_id,self.__class__.__name__)
                if per:
                    response=change_status(data)
                    return jsonify(response) 
                else:
                    return msg_403
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)


##############################################
#                  CACHE CLEAR API           #
##############################################

class Cacheclear(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            optype=data['op_type']
            # se=checkSessionValidity(session_id,user_id) For Testing purpose it is commented
            se=True 
            if se:               
                if optype=="h":
                    cache.clear()
                    return jsonify(cacheclear)
                elif optype=="p":
                    programcache.clear()
                    return jsonify(prgcacheclear)
                elif optype=="s":
                    singleprogramcache.clear()
                    return jsonify(prgcacheclear)
                elif optype =="q":
                    cachequestion.clear()
                    return jsonify(quscacheclear)
                else:
                    return jsonify(error) 
            else: 
                return session_invalid   
        except Exception as e:
            return jsonify(error) 

##############################################
#                  CACHE CLEAR API           #
##############################################

##############################################
#                 RESPONSE FORMATTIN          #
##############################################

# def format_response(success,message,data={},error_code=0):
# 	if(error_code==0):		
# 		return({"success":success,"message":message,"data":data})
# 	else:
# 		return({"success":success,"errorCode":error_code,"message":message,"data":data})

###############################################
#                  LMS Teacher List           #
###############################################

def listcoursebatch(batchlist):
                             
    userData = requests.post(lms_teacher_courselist, json=batchlist)
    userDataResponse=json.loads(userData.text) 
    return userDataResponse 


class Lmslteacherlist(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_id = data['userId']
            session_id = data['sessionId']
            se = checkSessionValidity(session_id, user_id)
            batchlist = []
            if se:
                per = checkapipermission(user_id, self.__class__.__name__)
                if per:
                    batch = TeacherCourseMapping.query.filter_by(
                        teacher_id=user_id).all()
                    if batch != []:
                        for i in batch:
                            
                            batchlist.append(
                                {"batch_id": i.batch_id, "course_id": i.course_id, "teacher_id": i.teacher_id})
                        response = listcoursebatch(batchlist)
                     
                        return jsonify(response)
                    else:
                        return nobatchfound
                else:
                    return msg_403
            else:
                return session_invalid
        except Exception as e:
            return jsonify(error)

 
##############################################
#                   LMS MODULE API           #
##############################################

api.add_resource(LmsBulkRegistration,"/api/lmsbulkreg")
api.add_resource(FetchLmscidandCourseid, '/api/fetch_lms_courseid') 

################################################################
#####                ADMIN MODULE START                    #####
################################################################
api.add_resource(AdminLogin,"/api/adminlogin")
api.add_resource(StudentBatchLists,"/api/stud_batch_list")
api.add_resource(Applicants, '/api/student_applicant_list')
api.add_resource(AdmissionProgramBatch, '/api/admission_program_batch_list')

api.add_resource(Applicantpreview, '/api/applicantpreview')

################################################################
#####                 ADMIN MODULE END                     #####
################################################################

################################################################
#####                   PORTAL MODULE                      #####
################################################################
# api.add_resource(StudentAdd, '/student_apply')
api.add_resource(StudentApplyApiGateway, '/api/student_apply')
api.add_resource(GetQuestionaireAnswersApiGateway, '/api/answer')
# api.add_resource(Paymentgateway, '/Paymentgateway')
# api.add_resource(Transcationresponse, '/Transcationresponse')
# api.add_resource(TranscationresponseFailed, '/TranscationresponseFailed')
api.add_resource(PaymentGateway1, '/api/PaymentGatewayApi')
api.add_resource(PayTransactionResponse, '/api/PayTransactionResponse')
api.add_resource(PayTransactionResponseFailure, '/api/PayTransactionResponseFailure')

# Transcation
api.add_resource(Transaction, '/api/transaction')

api.add_resource(GetLogin,"/api/login")
api.add_resource(GetRegisterUser,"/api/register")
api.add_resource(ChangePasswordApiGateway,"/api/changepassword")

################### GATEWAY API URL ###################
api.add_resource(GetProfileEditDetails,"/api/profileeditdetails")
api.add_resource(SubmitProfileEditDetails,"/api/submitprofileeditdetails")
api.add_resource(GetProfileAddressDetails,"/api/profileaddressdetails")
api.add_resource(SubmitProfileAddressDetails,"/api/submitprofileaddressdetails")
api.add_resource(GetEducationalDetails,"/api/profileeducationaldetails")
api.add_resource(Usereducationalqualification, '/api/usereducationalqualification')
api.add_resource(SubmitEducationalDetails,"/api/submitprofileeducationaldetails")
api.add_resource(EditEducationalDetails,"/api/editprofileeducationaldetails")
api.add_resource(DeleteEducationalDetails,"/api/deleteprofileeducationaldetails")
api.add_resource(ForgotPassword,"/api/forgotpassword")
api.add_resource(SendCodeForgotPassword,"/api/sendcodetoemail")
api.add_resource(VerifyEmail,"/api/verifyemail")
api.add_resource(VerifyCode,"/api/verifycode")
api.add_resource(GetPhotoDetails,"/api/profilephotodetails")
api.add_resource(SubmitPhotodetails,"/api/submitprofilephotodetails")
# api.add_resource(GetGetProfilePreviewApiGateway,'/api/profile_preview')
# api.add_resource(HomeScreenApiGateway, '/api/home')
# api.add_resource(GetAboutUs, '/api/aboutus') 
# api.add_resource(GetOneProgramme, '/api/singleprogramme')
# api.add_resource(GetNews, '/api/news')

# api.add_resource(Studycenter, '/api/studycenter')
# api.add_resource(GetCalendar,'/api/calendar')
# api.add_resource(GetFAQ,'/api/faq')
api.add_resource(GetAllEvent,'/api/allevents')
api.add_resource(GetSearch,"/api/search")
api.add_resource(University, '/api/universityget')
api.add_resource(GetCourses,"/api/getcourses")
# Admission module
api.add_resource(GetActs,"/api/acts")
api.add_resource(Teacherapply,"/api/teacherapply")
api.add_resource(AdminTeacher,"/api/adminteacher")
api.add_resource(Adminpermission,"/api/adminpermission")
api.add_resource(Adminuserlist,"/api/adminuserlist")
api.add_resource(Allprogrammeuserapplied,"/api/allprogrammeuserapplied")
api.add_resource(Teacherlist,"/api/teacherlist")
################MIDDLEWARE API###################
# api.add_resource(Login,"/login")
# api.add_resource(Register,"/register")
# api.add_resource(EmailVerificationCodeGeneration, '/emailverification')
# api.add_resource(EmailVerificationCodeVerification, '/codeverification')
# api.add_resource(SearchApi, '/searchApi')
# api.add_resource(ProfileeditPersonalGet, '/Profileedit')
# api.add_resource(ProfileeditpersonalPostTable, '/ProfileeditpersonalPost')
# api.add_resource(ProfileeditAddressGet, '/ProfileeditAddressGet')
# api.add_resource(ProfileeditAddressPost, '/ProfileeditAddressPost')
# api.add_resource(ProfileeditEducatinalGet, '/ProfileeditEducatinalGet')
# api.add_resource(ProfileeditEducatinalGetID, '/ProfileeditEducatinalGetID')
# api.add_resource(ProfileeditEducatinalPost, '/ProfileeditEducatinalPost')
# api.add_resource(ProfileeditEducatinalDelete, '/ProfileeditEducatinalDelete')
# api.add_resource(ProfileeditEducatinalEdit, '/ProfileeditEducatinalEdit')
# api.add_resource(ProfileeditPhotoGet,'/profileeditphotoGet')
# api.add_resource(ProfileeditPhotoPost,'/profileeditphotoPost')
api.add_resource(GetProfilePreview,'/api/profile_preview')
# api.add_resource(ForgotPassword_m, '/ForgotPassword')
# api.add_resource(NewPassword, '/NewPassword')
# api.add_resource(ChangePassword, '/ChangePassword')
api.add_resource(Acts,"/acts")
# api.add_resource(GetQuestionaireAnswers, '/questionaire_answer')

api.add_resource(Applicantexistornot, '/api/applicantexistornot')

# Middleware
api.add_resource(HomeScreenApi, '/api/home')
api.add_resource(AboutusApi, '/api/aboutus') 
api.add_resource(GetAllProgrammes, '/api/programme')
# api.add_resource(ProgramApiParticularId,'/programme')
api.add_resource(CalenderApi,'/api/calendar')

api.add_resource(GetallCalendar,'/api/allcalendar')
api.add_resource(FAQ,'/api/faq')

#sprint 3
api.add_resource(Adddepartment, '/api/add_department')
api.add_resource(Getalldepartment, '/api/getall_department')
# api.add_resource(Deletedepartment, '/api/delete_department')
api.add_resource(Editdepartment, '/api/edit_department')
api.add_resource(Getdepartment, '/api/get_department')
api.add_resource(Addevents, '/api/add_events')
api.add_resource(Deleteevents, '/api/delete_events')
api.add_resource(Editevents, '/api/edit_events')
api.add_resource(Getevents, '/api/get_events')
api.add_resource(Addfaq, '/api/add_faq')
api.add_resource(Deletefaq, '/api/delete_faq')
api.add_resource(Editfaq, '/api/edit_faq')
api.add_resource(Getsfaq, '/api/get_faq')
api.add_resource(Addaboutus, '/api/add_aboutus')
# api.add_resource(Deleteaboutus, '/api/delete_aboutus')
api.add_resource(Editaboutus, '/api/edit_aboutus')
api.add_resource(Getsaboutus, '/api/get_aboutus')
api.add_resource(Addeligibility, '/api/addeligibility')
api.add_resource(Geteligibility, '/api/geteligibility')
api.add_resource(Editeligibility, '/api/editeligibility')
api.add_resource(Deleteeligibility, '/api/deleteeligibility')

api.add_resource(Addprogramme, '/api/addprogramme')
api.add_resource(Editprogramme, '/api/editprogramme')

api.add_resource(Addbatch, '/api/addbatch')
api.add_resource(Getsinglebatch, '/api/singlebatch')
api.add_resource(Editbatch, '/api/editbatch')
api.add_resource(Getallbatch, '/api/getallbatch')
api.add_resource(Batchstatuschange, '/api/changebatchstatus')
api.add_resource(Programmestatuschange, '/api/programmestatuschange')

api.add_resource(Getallprogramme_and_dept, '/api/getallprogramme_and_dept')
# api.add_resource(PaymentResponse, '/api/payment_response')
api.add_resource(OngoingProgram, '/api/ongoing_prgmslist')
api.add_resource(UpcomingProgram, '/api/upcoming_prgmslist')
api.add_resource(Allteacherlist, '/api/allteacherlist')
# api.add_resource(Editprogramme, '/api/editprogramme')

########    LMS    #######

api.add_resource(Assignteacher,'/api/assignteacher')
api.add_resource(Listingteachersname, '/api/listingteachers_name')
api.add_resource(Fetchcoursename, '/api/listingcourse_name')
api.add_resource(Listcourseassignedforteacher, '/api/listingcourse_teacherbatch') #list of batches assigned for a teacher
api.add_resource(Listteacherassignedforcourse,'/api/listteacherassignedforcourse') #list of teacher assigned for a course

api.add_resource(AddCoursestucture, '/api/addcourse')
api.add_resource(EditCourseStucture, '/api/editcourse')
api.add_resource(GetAllCourseStucture, '/api/getallcourse')
api.add_resource(GetSingleCourseStucture, '/api/getsinglecourse')

api.add_resource(Course_pgm_mapping,'/api/course_pgm_mapping')

api.add_resource(GetTeacherCourses, '/api/get_teacher_courses') #list all courses assigned to teacher under a batch
api.add_resource(CourseUnlink, '/api/course_unlink')
api.add_resource(Changestudentstatus, '/api/change_student_status')
api.add_resource(Cacheclear, '/api/cache_clear')
api.add_resource(Studentlist, '/api/student_list')
api.add_resource(Paymenthistory, '/api/stud_payment_history')
api.add_resource(Adminpaymenthistory, '/api/admin_payment_history')
api.add_resource(ReminderMail, '/api/reminder_email')
api.add_resource(TeacherLogin, '/api/teacher_login')
api.add_resource(Lmslteacherlist, '/api/lmsteacherlist')
api.add_resource(SaveMobileDeviceid, '/api/add_mob_deviceid')
api.add_resource(PaymentTracker, '/api/payment_tracker')
api.add_resource(TeacherReject, '/api/teacher_reject')
########    LMS    #######
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()





