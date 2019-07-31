msg_403={"Status" : 403,"message": "Forbidden Access"}
forbiddenAccess={"status" : 403,"message": "Forbidden access","data":{}}
teacherInvalidEmail={'status':400,"message": "Invalid email","data":{}}
badGateway={'status':502,'message':'Bad gateway',"data":{}}
session_invalid={"status":401,"message":"Unauthorised Access"}
error={'status':502,'message':'Bad Gateway'}
unsuccessfulllogin={'status':200,"message": "login UnSuccessful"}
teacherunsuccesslogin={'status':400,"message": "Login unsuccessful","data":{}}
loginSuccess={'status':200,"message": "Login successful"}
pswdChange={'status':200,"message": "First time login,please change your password"}
invalidemail={'status':400,"message": "Invalid Email"}
emailexist={'status':200,"message": "Email already exists"}
nophoto={"status":200,"message":"No photo found"}
mailsent={"status":200,"message":" mail send"}
invaliduser={'status':400,"Message": "Invalid user"}
emailcodeexpired={"status":400,"mesage":"code expired"}
emailcodeverified={"status":200,"mesage":"code verified"}
emailcodeinvalid={"status":400,"mesage":"invalid code"}
pwdupdated={"status":200,"message":"password updated"}
updated={"status":200,"message":"successfully updated"}
deleted={"status":200,"message":"successfully Deleted"}
eligible={"status":200,"message":"You are eligible for this course"}
noteligible={"status":200,"message":"You are not eligible for this course"}
blankemail={'status':400,"Message": "Blank Email"}
blankpassword={'status':400,"Message": "Blank Password"}
noqualificationdetails={"status":200,"message":"No qualification Entered"}
generaluser_id=2
qua_label={
            "SSLC or equivalent":0,
            "10+2 or equivalent":1,
            "Graduation degree or equivalent":2,
            "Masters degree or equivalent":3,
            "Doctoral Studies or equivalent":4,
            "Other":5
        }
profile={"status":201,"message":"Please fill your profile completely"} 
qualification={"status":202,"message":"Please fill your qualification details"}
info_update={"status":200,"message":"Personal details updated successfully"}
address_update={"status":200,"message":"Address updated successfully"}
fail={"status":200,"message":"Failed to Add"}
alreadyassigned={'status':"200", "message":"Already Assigned"}
teacherassigned={'status':"200", "message":"Teacher has been assigned"}
nobatchfound={'status':200,"message":"No Batch Assigned"}
cacheclear={'status':200,"message":"Successfully cleared home cache"}
prgcacheclear={'status':200,"message":"Successfully cleared programme cache"}
quscacheclear={'status':200,"message":"Successfully cleared eligibility question cache"}
alreadyexist={'status':"200", "message":"Qualification Already exist"}
mg_email="noreply.dasp@mgu.ac.in"
mg_password="3p@y@dm!n@)!&"
##############################################
#                 RESPONSE FORMATTIN          #
##############################################

def format_response(success,message,data={},error_code=0):
	if(error_code==0):		
		return({"success":success,"message":message,"data":data})
	else:
		return({"success":success,"errorCode":error_code,"message":message,"data":data})