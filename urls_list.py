###########################
##   PRODUCTION SERVER
###########################
# _info_base_url='http://13.127.50.187:6100'

############################
##    QA
############################
# _info_base_url='http://54.66.133.32:6100'

############################
##    DEV
############################
# _info_base_url='http://52.63.114.210:6100'

_info_base_url='http://13.235.206.195:6100'
# http://13.235.206.195:6100/

############################
##    DEV
############################

# _info_base_url='http://192.168.1.50:8080'


###########################
##             LMS
###########################
_lms_base_url='http://services.test99lms.com'

########################################################
######                Admission API               ######
########################################################
prgm_backendapi=_info_base_url+"/api/gateway/adm_pgm"
prgm_batch_backendapi=_info_base_url+"/api/gateway/adm_pgm_batch"
lists_backendapi=_info_base_url+"/api/gateway/applicantlist"
applicantexistornot_api=_info_base_url+"/api/gateway/checkapplicant"
adminuserlist_api=_info_base_url+"/api/gateway/selectedlist"
allprogrammeuserapplied_api=_info_base_url+"/api/gateway/mycourses"


########################################################
######               INFO_MODULE API              ######
########################################################
change_studentstatus=_info_base_url+"/api/gateway/change_status_as_student"
getquestionaire=_info_base_url+"/api/gateway/questionnaire"
addapplicant=_info_base_url+"/api/gateway/applicantadd"
fetch_course_name=_info_base_url+"/api/gateway/batch_course_name"
fetch_course_teacherbatch=_info_base_url+"/api/gateway/teacher_batch"
token_api=_info_base_url+'/api/gettoken'
backend_home_api=_info_base_url+'/api/gateway/home'

calenderapi=_info_base_url+"/api/gateway/calendar"
programme_api=_info_base_url+"/api/gateway/programme"
search_api_info=_info_base_url+"/api/gateway/search"
allcalendar_api=_info_base_url+"/api/gateway/allcalendar"

getalldepartment_api=_info_base_url+"/api/gateway/department"
adddepartment_api=_info_base_url+"/api/gateway/departmentadd"
editdepartment_api=_info_base_url+"/api/gateway/departmentedit"
deletedepartment_api=_info_base_url+"/api/gateway/departmentdelete"
getdepartment_api=_info_base_url+"/api/gateway/singledepartment"

addevents_api=_info_base_url+"/api/gateway/eventadd"
editevents_api=_info_base_url+"/api/gateway/eventedit"
deleteevents_api=_info_base_url+"/api/gateway/eventdelete"
getevents_api=_info_base_url+"/api/gateway/eventsingle"
#faq
editfaq_api=_info_base_url+"/api/gateway/editfaq"
deletefaq_api=_info_base_url+"/api/gateway/deletefaq"
addfaq_api=_info_base_url+"/api/gateway/addfaq"
getfaq_api=_info_base_url+"/api/gateway/singlefaq"

editaboutus_api=_info_base_url+"/api/gateway/aboutedit"
addaboutus_api=_info_base_url+"/api/gateway/aboutadd"
getaboutus_api=_info_base_url+"/api/gateway/getabout"

#eligibility
add_eligibility_api=_info_base_url+"/api/gateway/addeligibility"
get_eligibility_api=_info_base_url+"/api/gateway/singleeligibility"
edit_eligibility_api=_info_base_url+"/api/gateway/editeligibility"
delete_eligibility_api=_info_base_url+"/api/gateway/deleteeligibility"


add_programme_api=_info_base_url+"/api/gateway/programmeadd"
edit_programme_api=_info_base_url+"/api/gateway/programmeedit"
delete_programme_api=_info_base_url+"/api/gateway/programmedelete"
getallprogramme_and_dept_api=_info_base_url+"/api/gateway/allprg"
programmestatuschange_api=_info_base_url+"/api/gateway/prg_chg_status"

add_batch_api=_info_base_url+"/api/gateway/addbatch"
getsinglebatch_api=_info_base_url+"/api/gateway/singlebatch"
edit_batch_api=_info_base_url+"/api/gateway/editbatch"
delete_batch_api=_info_base_url+"/api/gateway/removebatch"
getallbatch_api=_info_base_url+"/api/gateway/allbatch"
batchstatuschange_api=_info_base_url+"/api/gateway/batch_chg_status"
proramme_courses_api=_info_base_url+"/api/gateway/all_prg_courses"
prgm_semester_backendapi=_info_base_url+"/api/gateway/programme_semester_list"

add_course_api=_info_base_url+"/api/gateway/add_couse"
edit_course_api=_info_base_url+"/api/gateway/edit_couse"
get_all_course_api=_info_base_url+"/api/gateway/getcourse"
get_single_course_api=_info_base_url+"/api/gateway/retrieve_course"
get_teacher_course_api=_info_base_url+"/api/gateway/teacher_course"
course_prgm_mapping=_info_base_url+"/api/gateway/course_pgm_mapping"
prg_course_list=_info_base_url+"/api/gateway/prg_course_list"
course_unlink_api=_info_base_url+"/api/gateway/coursemap_delete"
payment_gateway_backendapi=_info_base_url+"/api/gateway/paymentrequest"
payment_receipt_backendapi=_info_base_url+"/api/gateway/paymentreceipt"
prgm_payment_backendapi=_info_base_url+"/api/gateway/prgm_payment_det"
ongoing_backendapi=_info_base_url+"/api/gateway/ongoing_prgm"
upcoming_backendapi=_info_base_url+"/api/gateway/upcoming_prgmlist"
get_all_events_backendapi=_info_base_url+"/api/gateway/get_all_events"
get_all_faq_backendapi=_info_base_url+"/api/gateway/get_all_faq"
studentlist_backendapi=_info_base_url+"/api/gateway/user_list"
paymenthistory_backendapi=_info_base_url+"/api/gateway/paymenthistory"
student_check_backendapi=_info_base_url+"/api/gateway/student_check"
paymenttracker_backendapi=_info_base_url+"/api/gateway/get_all_payment_details"
# LMS

bulkapi=_lms_base_url+"/BulkEnrollStudentsFromExternal/"
teacher_reg_api=_lms_base_url+"/RegisterCandidateUser/"

lms_teacher_courselist =_info_base_url+"/api/gateway/lms_teacher_courselist"
