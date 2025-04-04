from flask import Blueprint, current_app as app, jsonify, request
from flask_restful import Api, reqparse, Resource
from flask_security import auth_required, current_user, login_user, roles_required, roles_accepted
import re
from werkzeug.security import generate_password_hash, check_password_hash
from controller.extensions import db
from model.models import User, Role, UserDetails, ProfessionalQualification
from .utils import Utility

auth_api_bp = Blueprint("auth_api","__name__")
auth_api = Api(auth_api_bp)

class ValidateUserDetails(): 
  def validateEmail(self, email):
    pattern = r'^(?!.*\.\.)[a-zA-Z\d._%+-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
  
  def validateUserName(self, user_name):
    pattern = r"^[a-zA-Z\d]([a-zA-Z\d-]{1,7}[a-zA-Z0-9])$"
    return bool(re.match(pattern, user_name))
  
  def validatePassword(self, password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[\W_]).{4,8}'
    return bool(re.match(pattern, password))
  
  def validateName(self, name):
    return len(name) < 30
    
  def validateContactNumber(self, contact_number):
    pattern = r'^[6789]\d{9}$'
    return bool(re.match(pattern, contact_number))

  def validatePinCode(self, pin_code):
    pattern = r'^[\d]{6}$'
    return bool(re.match(pattern, pin_code))
    
  def validateAddress(self, address):
    return len(address) < 50
  
  def validatedExperience(self, experience):
    return 0 < int(experience) < 50
    
  def validateImage(self, image):
    allowed_extensions = ['jpg', 'png']
    max_size = 2 * 1024 * 1024
    file_extension = image.filename.split(".")[-1].lower()
    file_size = image.content_length
    if(file_extension not in allowed_extensions):
      return "Extension Error"
    elif(file_size > max_size):
      return "Size Error"
    else:
        return True
      
  def validateResume(self, resume):
    allowed_extensions = ['pdf']
    max_size = 10 * 1024 * 1024
    file_extension = resume.filename.split(".")[-1].lower()
    file_size = resume.content_length
    if(file_extension not in allowed_extensions):
      return "Extension Error"
    elif(file_size > max_size):
      return "Size Error"
    else:
      return True
      
  def validateUserRegistration(self, args):
    if(args["email"] == ""):
      return ("EmailError", "Email is not blank")
    elif(not self.validateEmail(args["email"])):
      return ("EmailError", "Please enter a valid email address. It must contain an '@' symbol, a period (.) after the '@', and no consecutive dots (e.g., 'test..example@example.com' is invalid).")
    
    if(args["password"] == ""):
      return ("PasswordError", "Password is not blank")
    elif(not self.validatePassword(args["password"])):
      return ("PasswordError", "Password must be between 4 and 8 characters long, include at least one symbol, one uppercase letter, one lowercase letter, and one number.")
    
    if(args["user_name"] == ""):
      return ("UserNameError", "Username is not blank")
    elif(not self.validateUserName(args["user_name"])):
      return ("UserNameError", "Username must be between 3 and 9 characters long and can only contain letters, numbers, hyphens, and underscores. It cannot start or end with a hyphen.")
    
    if(args["role"] == ""):
      return ("RoleError","Role is not blank")
    
    return ("Success", "Registration Successful")
    
  
  def validatedetails(self, data, method = "POST"):
    if(data["image_file"] != ""):
      image_response = self.validateImage(data["image_file"])
    if(current_user.roles[0] == "Professional" and data["resume_file"] != ""):
      resume_response = self.validateResume(data["resume_file"])
      
    if(data["name"] == ""):
      return ("NameError", "Name is not blank")
    elif(not self.validateName(data["name"])):
      return ("NameError", "Name must be less than 30 characters.")
    
    elif(data["contact_number"] == ""):
      return ("ContactNumberError", "Contact Number is not blank")
    elif(not self.validateContactNumber(data["contact_number"])):
      return ("ContactNumberError", "Please enter a valid phone number. It should start with 6, 7, 8, or 9 and have 10 digits.")      
    
    elif(data["city"] == ""):
      return ("CityError", "City is not blank")
    
    elif(data["state"] == ""):
      return ("StateError", "State is not blank")
    
    elif(data["pin_code"] == ""):
      return ("PinCodeError", "Pin code is not blank")
    elif(not self.validatePinCode(data["pin_code"])):
      return ("PinCodeError", "Please enter a valid pin code. It should be 6 digits long and contain only numbers.")
    
    elif(data["address"] == ""):
      return ("AddressError", "Address is not blank")
    elif(not self.validateAddress(data["address"])):
      return ("AddressError", "Address must be less than 50 characters.")
    
    elif(current_user.roles[0].name == "Professional" and data["experience"] == ""):
      return ("ExperienceError", "Experience is not blank")
    elif(current_user.roles[0].name == "Professional" and not self.validatedExperience(data["experience"])):
      return ("ExperienceError", "Please enter your years of experience (between 0 and 50).")
    
    elif(current_user.roles[0] == "Professional" and data["service_type"] == ""):
      return ("ServiceTypeError", "Service type is not blank")
    
    elif(method == "POST"):
      if(data["image_file"] == ""):
        return ("ImageError", "Image is not blank")
      elif(image_response == "Extension Error"):
        return ("ImageError", image_response)
      elif(image_response == "Size Error"):
        return ("ImageError", image_response)
      elif(current_user.roles[0].name == "Professional" and data["resume_file"] == ""):
        return ("ResumeError", "Resume is not blank")
      elif(current_user.roles[0].name == "Professional" and resume_response == "Extension Error"):
        return ("ResumeError", resume_response)
      elif(current_user.roles[0].name == "Professional" and resume_response == "Size Error"):
        return ("ResumeError", resume_response)
      else:
        return ("Success", "Profile completed successfully")
      
    elif(method == "PUT"):
      if(current_user.roles[0].name == "Customer"):
        if(data["image_file"] == ""):
          return ("Success", "Profile updated successfully")
        elif(image_response == "Extension Error"):
          return ("ImageError", image_response)
        elif(image_response == "Size Error"):
          return ("ImageError", image_response)
        else:
          return ("Success", "Profile updated successfully")
        
      if(current_user.roles[0].name == "Professional"):
        if(data["image_file"] == "" and data["resume_file"] == ""):
          return ("Success", "Profile updated successfully")
        elif(data["image_file"] !="" and data["resume_file"] == ""):
          if(image_response == "Extension Error"):
            return ("ImageError", image_response)
          elif(image_response == "Size Error"):
            return ("ImageError", image_response)
          else:
            return ("Success", "Profile updated successfully")
        elif(data["image_file"] =="" and data["resume_file"] != ""):
          if(resume_response == "Extension Error"):
            return ("ResumeError", resume_response)
          elif(resume_response == "Size Error"):
            return ("ResumeError", resume_response)
          else:
            return ("Success", "Profile updated successfully")
        else:
          if(image_response == "Extension Error"):
            return ("ImageError", image_response)
          elif(image_response == "Size Error"):
            return ("ImageError", image_response)
          elif(resume_response == "Extension Error"):
            return ("ResumeError", resume_response)
          elif(resume_response == "Size Error"):
            return ("ResumeError", resume_response)
          else:
            return ("Success", "Profile updated successfully")     


class UserAuthentication(Resource):
  def get_parser(self):
    parser = reqparse.RequestParser()
    parser.add_argument(
                        "email", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "email cannot be blank"
                        )
    parser.add_argument(
                        "password", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "password cannot be blank"
                        )
    return parser
  
  
  def post(self):
    parser = self.get_parser()
    args = parser.parse_args()
    try: 
      email = args["email"]
      password = args["password"]                   
      
      user = app.security.datastore.find_user(email = email)
      if user:
        role = user.roles[0].name
        if(not user.active):
          if(role == "Customer"):
            return {
              "AccountError": "Your account is inactive. Due to fraudulent activity."
            }, 401
          else:
            return {
              "AccountError" : "Your account is inactive. Due to poor reviews."
            }, 401
        if(user.profile_verified and role == "Professional"):
          return {
            "VerificationError": "Your account is not verified wait for some time."
          }, 400
    
        if check_password_hash(user.password, password):
          if(current_user.is_authenticated):
            return {
              "message" : "User already logged in"
            }, 404
          login_user(user)
          user_detail = {
            "id" : user.user_id,
            "email" : user.email,
            "username" : user.username,
            "state_city" : Utility.fetch_state_city(),
            "auth_token" : user.get_auth_token(),
            "role" : user.roles[0].name,
          }
          return user_detail, 200
        else:
          return {
            "PasswordError" : "Incorrect password"
          }, 404
      else:
        return {
          "NotFoundError" : "User not found"
        }, 404
    except Exception as e:
      return{
        "message" : f"Error occured: {str(e)}"
      }, 500
      
      
  
class UserRegistration(Resource):
  def get_parser(self):
    parser = reqparse.RequestParser()
    parser.add_argument(
                        "email", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "email cannot be blank"
                        )
    parser.add_argument(
                        "user_name", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "username cannot be blank"
                        )
    parser.add_argument(
                        "password", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "password cannot be blank"
                        )
    parser.add_argument(
                        "role", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "role can be either customer or professional"
                        )
    return parser
  
  
  def post(self):
    parser = self.get_parser()
    args = parser.parse_args()
    try: 
      user = app.security.datastore.find_user(email = args["email"])
      if user is None:
        username_exist = User.query.filter_by(username = args["user_name"]).first()
        if not username_exist:
          validator = ValidateUserDetails()
          message_name, message_value = validator.validateUserRegistration(args)
          if(message_name != "Success"):
            return {
              message_name : message_value
            }, 400
          else: 
            app.security.datastore.create_user(
                                                email = args["email"],
                                                username = args["user_name"],
                                                password = generate_password_hash(args["password"]),
                                                roles = [args["role"]]
                                              )
            db.session.commit()
            return {
              message_name : message_value
            }, 200
        else:
          return {
            "UserNameExistError" : "Username not availlable try with different name."
          }, 404
      else:
        return {
          "UserExistError" : "User already exist"
        }, 404
    except Exception as e:
      return{
        "message" : f"Error occured: {str(e)}"
      }, 500
      
 
class UserProfile(Resource):
  def get_parser(self):
    parser = reqparse.RequestParser()
    parser.add_argument(
                        "user_id", 
                        type = int, 
                        required = True, 
                        help = "user id cannot be blank"
                        )
    parser.add_argument(
                        "name", 
                        type = str, 
                        required = True, 
                        help = "name cannot be blank"
                        )
    parser.add_argument(
                        "contact_number", 
                        type = str, 
                        required = True, 
                        help = "contact number cannot be blank"
                        )
    parser.add_argument(
                        "state", 
                        type = str, 
                        required = True, 
                        help = "state cannot be blank"
                        )
    parser.add_argument(
                        "city", 
                        type = str, 
                        required = True, 
                        help = "city cannot be blank"
                        )
    parser.add_argument(
                        "pin_code", 
                        type = str, 
                        required = True, 
                        help = "pin code cannot be blank"
                        )
    parser.add_argument(
                        "address", 
                        type = str, 
                        required = True, 
                        help = "address cannot be blank"
                        )
    parser.add_argument(
                        "service_type", 
                        type = str, 
                        required = current_user.roles[0] == "Professional", 
                        help = "service type cannot be blank"
                        )
    parser.add_argument(
                        "experience", 
                        type = int, 
                        required = current_user.roles[0] == "Professional", 
                        help = "experience cannot be blank"
                        )
    parser.add_argument(
                        "image_file", 
                        type = str,  
                        help = "image file cannot be blank"
                        )
    parser.add_argument(
                        "resume_file", 
                        type = str,  
                        help = "resume file file cannot be blank"
                        )
    return parser
  
  
  def search_column(self, args):
    role = current_user.roles[0].name.lower()
    city = args.get("city").lower().replace(" ","")
    pin_code = args.get("pin_code")
    state = args.get("state").lower().replace(" ","")
    name = args.get("name").lower().replace(" ","")
    if(role == "professional"):
      service_type = args.get("service_type").lower().replace(" ","")
      experience = args.get("experience")
      search_string = f"{args["user_id"]}{role}{name}{city}{state}{pin_code}{service_type}{experience}"
    else:
      search_string = f"{args["user_id"]}{role}{name}{city}{state}{pin_code}"
    return search_string

  
  @auth_required('token')
  @roles_accepted("Customer","Professional")
  def get(self, user_id):
    try:
      role = current_user.roles[0].name
      user = User.query.get(user_id)
      
      if(role == "Professional"):
        resume_url = f"/static/images/{role}/{user_id}_info/{user.professional_qualifications.resume}"
        image_url = f"/static/images/{role}/{user_id}_info/{user.user_details.image_file}"
      else:
        image_url = f"/static/images/{role}/{user_id}_info/{user.user_details.image_file}"

      user_detail_dict = {
        "name" : user.user_details.name,
        "contact_number" : user.user_details.contact_number,
        "city" : user.user_details.city,
        "state" : user.user_details.state,
        "pin_code" : user.user_details.pin_code,
        "address" : user.user_details.address,
        "image_url" : image_url,
        "experience" : user.professional_qualifications.experience if role == "Professional" else "",
        "service_type" : user.professional_qualifications.service_type if role == "Professional" else "",
        "resume_url" : resume_url if role == "Professional" else ""
      }
      return user_detail_dict, 200
    except Exception as e:
      return{
        "message" : f"Error occured: {str(e)}"
      }, 500

  
  @auth_required('token')
  @roles_accepted('Customer','Professional')
  def post(self):
    try:
      data = request.form.to_dict()
      role = current_user.roles[0].name
      if(role == "Professional"):
        resume_file = request.files.get("resume_file")
        image_file = request.files.get("image_file")
      else:
        image_file = request.files.get("image_file")
        
      if(image_file is not None):
        data["image_file"] = image_file
        
      if(role == "Professional" and resume_file is not None):
        data["resume_file"] = resume_file
      
      validator = ValidateUserDetails()
      message, message_value = validator.validatedetails(data)
    
      if(message != "Success"):
        return {
            message : message_value
          }, 400
      
      user_detail = UserDetails(
                              user_id = data["user_id"],
                              name = data["name"],
                              contact_number = data["contact_number"],
                              city =  data["city"],
                              state = data["state"],
                              address = data["address"],
                              pin_code = data["pin_code"],
                              image_file = str(data["user_id"]) + "." +data["image_file"].filename.split(".")[-1],
                              search_column = self.search_column(request.form)
                              )
      if(role == "Professional"):
        Utility.store_image(image_file)
        Utility.store_resume(resume_file)
        professional_qualification = ProfessionalQualification(
                                  user_id = data["user_id"],
                                  service_type = data["service_type"],
                                  experience = data["experience"],
                                  resume = str(data["user_id"]) + "." + data["resume_file"].filename.split(".")[-1]
                                )
        user = User.query.get(data["user_id"])
        user.profile_verified = True
        db.session.add(user_detail)
        db.session.add(professional_qualification)
      else:
         Utility.store_image(image_file)
         db.session.add(user_detail)
      db.session.commit()
      return {
        message : message_value
      }, 200
    except Exception as e:
      return{
        "message" : f"Error occured: {str(e)}"
      }, 500
    
    
  @auth_required('token')
  @roles_accepted("Customer", "Professional")
  def put(self, user_id):
    try:
      user = User.query.get(user_id)
      role = current_user.roles[0].name
      
      data = request.form.to_dict()
      if(role == "Professional"):
        image_file = request.files.get("image_file")
        resume_file = request.files.get("resume_file")
      else:
        image_file = request.files.get("image_file")

      
      if(image_file is not None):
        data["image_file"] = image_file
        
      if(role == "Professional" and resume_file is not None):
        data["resume_file"] = resume_file
    
      validator = ValidateUserDetails()
      message, message_value = validator.validatedetails(data, method="PUT")
      
      if(message != "Success"):
        return {
            message : message_value
          }, 400
        
      if(image_file is not None):
        Utility.store_image(image_file)
        
      if(role == "Professional" and resume_file is not None):
        Utility.store_resume(resume_file)

        
      user.user_details.name = data["name"]
      user.user_details.contact_number = data["contact_number"]
      user.user_details.state = data["state"]
      user.user_details.city = data["city"]
      user.user_details.address = data["address"]
      user.user_details.pin_code = data["pin_code"]
      user.user_details.image_file = user.user_details.image_file if image_file is None else str(user_id) + "." + data["image_file"].filename.split(".")[-1]
      user.user_details.search_column = self.search_column(request.form)
      if(role == "Professional"):
        user.professional_qualifications.service_type =data["service_type"]
        user.professional_qualifications.experience =data["experience"]
        user.professional_qualifications.resume = user.professional_qualifications.resume if resume_file is None else str(user_id) + "." + data["resume_file"].filename.split(".")[-1]

      db.session.commit()
      
      return {
        message : message_value
      }, 200
    except Exception as e:
      return{
        "message" : f"Error occured: {str(e)}"
      }, 500
    
    
  @auth_required('token')
  @roles_required('Admin')
  def delete(self, user_id):
    try:
      user = User.query.filter_by("user_id").first()
      if user:
        db.session.delete(user)
        db.session.commit()
        return {
          "message" : "User deleted successfully"
        }
    except Exception as e:
      return{
        "message" : f"Error occured: {str(e)}"
      }, 500
    

 
auth_api.add_resource(
                       UserAuthentication,
                       '/auth_api/login_user',
                      )

auth_api.add_resource(
                       UserRegistration,
                       '/auth_api/register_user',
                      )

auth_api.add_resource(
                       UserProfile,
                       '/auth_api/user_details/<int:user_id>',
                       '/auth_api/complete_profile',
                       '/auth_api/update_user_details/<int:user_id>',
                       '/auth_api/delete_profile/<int:user_id>'
                      )