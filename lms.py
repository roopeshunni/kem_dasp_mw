from flask import Flask,jsonify,request
import requests
from flask_restful import Resource, Api
import json
from pymemcache.client import base
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urls_list import *
from constants import *
from model import *
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
from sqlalchemy import or_

###############################################################
#               BULK BATCH DETAILS ADD TO LMS                  #
###############################################################
def reg_bulkdata(data):                          
    userData = requests.post(
    fetch_course_name,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse

def bulkstud_data(data):                         
    userData = requests.post(
    lists_backendapi,json=data)            
    userDataResponse=json.loads(userData.text) 
    return userDataResponse
def bulk_requestfn(data):
    response=reg_bulkdata(data)
    studresponse1=bulkstud_data(data)
    msg1=studresponse1.get('message')
    list1=[]
    if 'Users' in msg1:
        userdtls=msg1.get('Users')
        for i in userdtls:
            if i.get("status")=='student':
                user1=UserProfile.query.filter_by(uid=i.get("user_id")).first()
                user=User.query.filter_by(id=i.get("user_id")).first()
                stud={"externalId":user.id,"email":user.email,"mobile":user1.phno,"admissionNo":i.get("applicantid"),"firstName":user1.fname,"lastName":user1.lname,"sex":user1.gender,"guardianPhone":"","guardianName":""}
                list1.append(stud)
    msg=response.get('message')
    batchdet=msg.get('batchdetails')
    coursedet=msg.get('coursedetails')
    clist=[]
    for i in coursedet:
        cdic={
            "externalId":i.get("couse_id"),
            "courseDetails": [
                {
                    "removable": False,
                    "title":"Course Benefits",
                    "value": "",
                    "template": "DynamicFields/editor.html",
                    "type": "content",
                    "help": "A short description of the Course(Optional, recommended)"
                }
            ],
            "type": "course",
            "Name":i.get("name"),
            "Duration": {
                "DurationDetails": {
                    "Year(s)": 1
                }
            }
        }
        clist.append(cdic)
        cid=i.get("couse_id")
        cmobj=LmsCourseMapping.query.filter_by(course_id=cid).first()
        if cmobj!=None:
            lms_c_id=cmobj.lms_c_id
            cdic["lmsId"]=lms_c_id

    dic={"external":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJOYW1lIjoiYWRtaW5AbWd1LmNvbSIsImNvbXBhbnlJZCI6IjVjNzY4NmFjNjQ5Nzk2MTQzNTEyMTk1MSIsInJvbGVJZCI6IjIiLCJ1c2VyRGV0YWlsc0lkIjoiNWNlY2RhNjI2NzhjZWYxNjYzZmM0MWQxIiwidXNlckxvZ2luSWQiOiI1Y2VjZGE2MTY3OGNlZjE2NjNmYzQxZDAiLCJwYXNzd29yZCI6Im1ndV9hZG1pbiIsInJvbGVNYXBwaW5nSWQiOiI1Y2VjZGE2MjY3OGNlZjE2NjNmYzQxZDIifX0.AqNwW3EMby9jR_cLBzmtPQWp4N32A00OlxW_rTXKWjY",
    "batch": {
        "batchObj": {
            "externalId":"6",
            "repeats": {
                "excludedDaysRepeat": []
            },
            "Admission": {
                "onBefore": "10",
                "beforeType": "Days",
                "onAfter": "10",
                "afterType": "Days",
                "beforeDaysCount": 10,
                "afterDaysCount": 10
            },
            "batchName":batchdet[0].get("name"),
            "batchMode": "onetime",
            "offline": True,
            "instructorLead": True,
            "startDate":batchdet[0].get("prg_start"),
            "endDate":batchdet[0].get("prg_end"),
            "seats":batchdet[0].get("seats"),
            "materialAssignment": "manual",
            "startTime": "1970-01-01T04:30:00.000Z",
            "endTime": "1970-01-01T11:30:00.000Z",
            "course": [],
            "activeFlag": 1
        }
    },
    "Courses":clist,
    "Students":list1
    }
    # print(dic)
    return dic


def savetoken_todb(response1,batch_id):
    stud_det=response1.get('students')
    for i in stud_det:
        userobj=UserExtTokenMapping.query.filter_by(user_id=i.get('externalId')).all()
        if userobj==[]:
            userres=UserExtTokenMapping(user_id=i.get('externalId'),email_id=i.get('email'),
            ext_token=i.get('external'),batch_id=batch_id)
            db.session.add(userres)
            db.session.commit()
        else:
            print("exist")
            
    course_det=response1.get("courses")
    for i in course_det:
        courobj=LmsCourseMapping.query.filter_by(course_id=i.get('externalId')).all()
        if courobj==[]:
            courseres=LmsCourseMapping(course_id=i.get('externalId'),lms_c_id=i.get('lmsId'))
            db.session.add(courseres)
            db.session.commit()
        else:
            print("exist")
# ############################################################# #
#               BULK BATCH DETAILS ADD TO LMS                   #
# ############################################################# #
class LmsBulkRegistration(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']
            batch_id1=data['batch_id']
            data={"batch_id":batch_id1}
            bulk_request=bulk_requestfn(data)
            # print(bulk_request)
            bulk_request1=json.dumps(bulk_request)
            # print(bulk_request1)
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InR5cGUiOiJjb21wYW55QXV0aCIsImNvbXBhbnlJZCI6IjVjNzY4NmFjNjQ5Nzk2MTQzNTEyMTk1MSJ9fQ.oADmwE7_J81Uo6VQRcPl3UGX08vcKE8mIWqkVLr4cRE"
            headers = {'Content-Type': 'application/json','Authorization':token}
            response1 = requests.post(bulkapi,json=json.loads(bulk_request1),headers=headers)
            if response1=="failed":
                return {"status":200,"message":"LMS Already Enabled"}
            resp=json.loads(response1.text)
            resp=json.loads(resp)
            # print(resp)
            savetoken_todb(resp,batch_id1)
            return {"status":200,"message":"LMS Enabled"}
        except Exception as e:
            return jsonify(error) 

# ############################################################# #
#        Function for fetch LMS id-functionality                #
# ############################################################# #

def fetchlms_id(user_id,course_id):
    user=UserExtTokenMapping.query.filter_by(user_id=user_id).first()
    if user!=None:
        external_token=user.ext_token
    else:
        return {"status":404,"message":"No Access"}
    user1=LmsCourseMapping.query.filter_by(course_id=course_id).first()
    if user1!=None:
        lms_c_id=user1.lms_c_id
    else:
        return {"status":404,"message":"Invalid CourseId"}
    dic={"external_token":external_token,"lms_c_id":lms_c_id}
    return {"status":200,"message":dic}

# ############################################################# #
#               Function for fetch LMS id-API GATEWAY           #
# ############################################################# #

class FetchLmscidandCourseid(Resource):
    def post(self):
        try:
            data=request.get_json()
            user_id=data['user_id']
            session_id=data['session_id']  
            course_id=data['course_id']           
            se=checkSessionValidity(session_id,user_id) 
            if se:
                response=fetchlms_id(user_id,course_id)
                return jsonify(response) 
            else:
                return session_invalid   
        except Exception as e:
            return jsonify(error)



##################################################
#   TEACHER API'S                                #
##################################################



#######################################################################
# TEACHER LOGIN                                                       #
#######################################################################
class TeacherLogin(Resource):
    def post(self):
        try:
            data=request.get_json()
            email=data['email']
            password=data['password']
            dev_type=data['devType']
            ip=data['ip']
            mac=data['mac']
            #####Checking whether user exits#####
            existing_user=User.query.filter_by(email=email).first()
            if(existing_user is None): #User does not exists
                    return format_response(False,"Invalid email",{},400)       
            if(existing_user.password==password):# user exists
                ####Checking whether the user is admin####
                uid=existing_user.id
                status=existing_user.status
                user_roles=RoleMapping.query.filter_by(user_id=uid).add_column('role_id').all() #get all the roles assigned to the user
                user_roles = [r.role_id for r in user_roles] #Converting user roles to a list
                role_list=Role.query.filter(Role.id.in_(user_roles)).filter_by(role_type="Admin").first() # Checking whether the user has admin rights
                if(role_list is None): #user is not admin
                    return format_response(False,"Forbidden access",{},403)  
                ####Checking whether the user is admin####
                #####User is admin ###################################
                IP=get_my_ip()
                new_userprofile=UserProfile.query.filter_by(uid=uid).first()
                name=new_userprofile.fname +' '+new_userprofile.lname             
                Session.query.filter_by(uid=uid,dev_type=dev_type).delete()
                db.session.commit()
                ##creating a new session start 
                curr_time=datetime.now()
                exp_time=curr_time++ timedelta(days=1)
                session_token = token_urlsafe(64)
                new_session=Session(uid=uid,dev_type=dev_type,session_token=session_token,exp_time=exp_time,IP=IP,MAC=IP)
                db.session.add(new_session)
                db.session.commit()
                ##creating a new session end
                data={
                        "uid":uid,
                        "name":name,
                        "status":status,
                        "sessionId":session_token
                    }      
                return format_response(True,"Login successful",data)
            else:
                return format_response(False,"Login failed",{},401)
        except Exception as e:
            return format_response(False, "Bad gateway", {}, 401)

def get_my_ip():
    return  request.remote_addr

##################################################
#   TEACHER ASSIGNED PROGRAMME AND COUSE LIST    #
##################################################

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
                        return format_response(False, "No batch assigned", {}, 400)
                else:
                    return format_response(False,"Forbidden access",{},403)
            else:
                return format_response(False,"Unauthorised access",{},401)
        except Exception as e:

            return format_response(False,"Bad gateway",{},502)


def listcoursebatch(batchlist):                      
    userData = requests.post(lms_teacher_courselist, json=batchlist)
    userDataResponse=json.loads(userData.text) 
    return userDataResponse 


def save_mobile_device_id(user_id, dev_id):
    try:
        dev_type = "m"
        queryset = Session.query.filter_by(uid=user_id, dev_type=dev_type.upper()).first()
        print(queryset)
        dict1 = []
        if queryset == None:
            return format_response(False, "Invalid user", {}, 400)
        else:
            queryset.MAC = dev_id
            db.session.commit()
            return format_response(True, "Successfully updated", {}, 200)
    except Exception as e:
        return format_response(True, "Bad gateway", {}, 502)


class SaveMobileDeviceid(Resource):
    def post(self):
        try:
           
            data = request.get_json()
            
            user_id = data['userId']
            session_id = data['sessionId']
            dev_id = data['devId']
           
            se = checkSessionValidity(session_id, user_id)
            
            
            if se:
                per = checkapipermission(user_id, self.__class__.__name__)
                
                if per:
                   
                    response = save_mobile_device_id(user_id, dev_id)
                    
                    return response
                else:
                    return format_response(False,"Forbidden access",{},403)
                    # return jsonify(noidfound)

            else:
                return format_response(False,"Unauthorised access",{},401)
        except Exception as e:
           
            return format_response(True, "Bad gateway", {}, 502)

################################################################
#####        FUNCTION FOR SESSION CHECKING                 #####
################################################################

def checkSessionValidity(sessionid,userid): 
    chk_user=Session.query.filter(Session.session_token==sessionid,Session.uid==userid,Session.exp_time>datetime.now()).first()
    
    if chk_user:
        return True
    else: 
        return False

################################################################
#####        FUNCTION FOR PERMISSION CHECKING             #####
################################################################

def checkapipermission(user_id,api_name):
    roles=RoleMapping.query.filter_by(user_id=user_id).all()
    roles = [r.role_id for r in roles] 
    perm_list=Permission.query.filter(Permission.role_id.in_(roles)).filter_by(API_name=api_name).first()
    
    if perm_list != None:
        return True
    return False

