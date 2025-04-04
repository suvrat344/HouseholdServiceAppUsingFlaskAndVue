from datetime import datetime
from flask import Blueprint, request
from flask_restful import Api, reqparse, Resource
from flask_security import auth_required, current_user, roles_accepted, roles_required
from model.models import *
from controller.extensions import db


customer_api_bp = Blueprint("customer_api", "__name__")
customer_api = Api(customer_api_bp)


class ServiceRequested(Resource):
  def get_parser(self):
    parser = reqparse.RequestParser()
    parser.add_argument(
                        "user_id", 
                        type = int, 
                        required = request.method == "POST", 
                        help = "user id cannot be blank"
                        )
    parser.add_argument(
                        "service_id", 
                        type = int, 
                        required = request.method == "POST", 
                        help = "service id cannot be blank"
                        )
    parser.add_argument(
                        "date_of_request", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "date of request cannot be blank"
                        )
    parser.add_argument(
                        "date_of_completion", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "date of completion cannot be blank"
                        )
    parser.add_argument(
                        "problem_description", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "problem description cannot be blank")
    parser.add_argument(
                        "service_status", 
                        type = str, 
                        required = False, 
                        default = "Pending", 
                        help = "service status can be Pending, Completed, Closed and Cancelled"
                        )
    parser.add_argument(
                        "price", 
                        type = float, 
                        required = False,  
                        )
    parser.add_argument(
                        "time_required", 
                        type = float, 
                        required = False, 
                        )
    parser.add_argument(
                        "rating", 
                        type = int, 
                        )
    parser.add_argument(
                        "review", 
                        type = str
                        )
    return parser
  
  @auth_required("token")
  @roles_required("Customer")
  def get(self, user_id):
    try:
      service_request = ServiceRequest.query.filter_by(customer_id = user_id).order_by(ServiceRequest.date_of_request.desc()).all()
      service_request_list = []
      
      for service_requested in service_request:
        service_request_dict = {}
        service_request_dict["service_id"] = service_requested.service_id
        service_request_dict["service_request_id"] = service_requested.service_request_id
        service_request_dict["service_name"] = service_requested.related_service.service_name
        service_request_dict["problem_description"] = service_requested.problem_description
        service_request_dict["date_of_request"] = service_requested.date_of_request.isoformat()
        service_request_dict["date_of_completion"] = service_requested.date_of_completion.isoformat()
        service_request_dict["price"] = float(service_requested.related_service.price)
        service_request_dict["time_required"] = float(service_requested.related_service.time_required)
        service_request_dict["service_status"] = service_requested.service_status
        if(service_requested.professional_id is not None):
          user = User.query.get(service_requested.professional_id)
          service_request_dict["professional_name"] = user.user_details.name
          service_request_dict["contact_number"] = user.user_details.contact_number
          service_request_dict["address"] = user.user_details.address
          service_request_dict["city"] = user.user_details.city
          service_request_dict["state"] = user.user_details.state
        service_request_list.append(service_request_dict)
      if service_request_list:
        return service_request_list, 200
    except Exception as e:
      return{
          "message": f"Error retrieving services: {str(e)}"
        }, 500
   
   
  @auth_required("token")
  @roles_required("Customer")
  def post(self):
    parser = self.get_parser()
    args = parser.parse_args()
    try:    
      service_type = Service.query.get(args["service_id"]).service_name
      users = User.query.all()
      customer = User.query.get(args["user_id"])
      customer_city = customer.user_details.city
      customer_pin_code = customer.user_details.pin_code
      flag = False
      for professional in users[1:]:
        if(professional.roles[0].name == "Professional"):
          professional_city = professional.user_details.city
          professional_pin_code = professional.user_details.pin_code
          professional_service_type = professional.professional_qualifications.service_type
               
          if(customer_city == professional_city and customer_pin_code == professional_pin_code and professional_service_type == service_type):
            flag = True
            break
        
      if(not flag):
        return {
          "message" : "Service not available in your location"
        }, 404
        
      service_request = ServiceRequest(
                          customer_id = args["user_id"],
                          service_id = args["service_id"],
                          date_of_request = datetime.strptime(args["date_of_request"], "%Y-%m-%d").date(),
                          date_of_completion = datetime.strptime(args["date_of_completion"], "%Y-%m-%d").date(),
                          problem_description = args["problem_description"]
                        )
      # add service request to database
      db.session.add(service_request)
      db.session.commit()
      return {
        "message" : "Service request created successfully"
      }, 200
    except Exception as e:
      # if any internal error then rollback the transaction
      db.session.rollback()
      return{
        "message" : f"Error creating service: {str(e)}"
      }, 500
      
      
  @auth_required("token")
  @roles_required("Customer")
  def put(self, service_request_id):
    parser = self.get_parser()
    args = parser.parse_args()
    try:
      service_request = ServiceRequest.query.get(service_request_id)
      service_request.user_id = args["user_id"]
      service_request.service_id = args["service_id"]
      service_request.problem_description = args["problem_description"]     
      service_request.date_of_request = datetime.strptime(args["date_of_request"], "%d-%m-%Y").date()
      service_request.date_of_completion = datetime.strptime(args["date_of_completion"], "%Y-%m-%d").date()
      db.session.commit()
      return {
        "message" : "Service Request updated successfully"
      }, 200
    except Exception as e:
      # if any internal error then rollback the transaction
      db.session.rollback()
      return{
        "message" : f"Error creating service: {str(e)}"
      }, 500
      
      
  @auth_required("token")
  @roles_accepted("Admin", "Customer")
  def delete(self, service_request_id):
    try:
      is_accepted = request.args.get("is_accepted")
      cancel_request = ServiceRequest.query.get(service_request_id)
      if(is_accepted == "true"):
        professional_action = ProfessionalAction.query.filter_by(
                                                        service_request_id = service_request_id,
                                                        professional_id = cancel_request.professional_id
                                                        ).first()
        professional_action.action_type = "Cancelled"
      else:
        professional_action = ProfessionalAction.query.filter_by(
                                                        service_request_id = service_request_id,
                                                        ).delete()
      cancel_request.service_status = "Cancelled"
      db.session.commit()
      return {
        "message" : "Service Request cancelled successfully"
      }, 200
    except Exception as e:
      # if any internal error then rollback the transaction
      db.session.rollback()
      return{
        "message" : f"Error creating service: {str(e)}"
      }, 500

      
customer_api.add_resource(
                       ServiceRequested,
                       '/customer_api/get_service_request/<int:user_id>', 
                       '/customer_api/create_service_request', 
                       '/customer_api/update_service_request/<int:service_request_id>',
                       '/customer_api/cancel_service_request/<int:service_request_id>',
                      )