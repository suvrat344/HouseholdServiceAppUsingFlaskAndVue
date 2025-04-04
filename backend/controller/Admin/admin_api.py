from flask import Blueprint, current_app, request
from flask_restful import Api, reqparse, Resource
from flask_security import auth_required, roles_accepted, roles_required
from model.models import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from controller.extensions import db

admin_api_bp = Blueprint("admin_api", "__name__")
admin_api = Api(admin_api_bp)


class Services(Resource):
  def get_parser(self):
    parser = reqparse.RequestParser()
    parser.add_argument(
                        "service_name", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "service name cannot be blank"
                        )
    parser.add_argument(
                        "description", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "description cannot be blank"
                        )
    parser.add_argument(
                        "image_file", 
                        type = str, 
                        required = request.method == "POST", 
                        help = "image icon cannot be bank"
                        )
    parser.add_argument(
                        "price", 
                        type = float, 
                        required = request.method == "POST", 
                        help = "price cannot be blank"
                        )
    parser.add_argument(
                        "time_required", 
                        type = float, 
                        required = request.method == "POST", 
                        help = "time_required cannot be blank")
    return parser

  
  def search_keyword(self, description):
    words = word_tokenize(description)
    stop_words = set(stopwords.words('english'))
    keywords = [word.lower() for word in words if word not in stop_words and word.isalpha()]
    return keywords


  def search_column(self, args):
    service_name = args["service_name"].lower().replace(" ","")
    keywords = self.search_keyword(args["description"])
    last_service = Service.query.order_by(db.desc(Service.service_id)).first()
    if(last_service is None):
      service_id = 1
    else: 
      service_id = last_service.service_id + 1
    search_string  = f"{service_id}{service_name}{''.join(keywords)}"
    return search_string

  
  @auth_required("token")
  def get(self):
    only_names = request.args.get("only_names", False)
    try:
      services = Service.query.all()
      if only_names:
        services_name = [service.service_name for service in services]
        if services_name:
          return {
            "services_name" : services_name
          }, 200
      else:
        services_list = []
        for service in services:
          service_dict = {}
          service_dict["service_id"] = service.service_id
          service_dict["service_name"] = service.service_name
          service_dict["description"] = service.description
          service_dict["image_file"] = service.image_file
          service_dict["price"] = service.price
          service_dict["time_required"] = float(service.time_required)
          services_list.append(service_dict)
        return services_list, 200
    except Exception as e:
      return{
          "message": f"Error retrieving services: {str(e)}"
        }, 500
      
   
   
  @auth_required("token")
  @roles_required("Admin")
  def post(self):
    parser = self.get_parser()
    args = parser.parse_args()
    try:  
      # create an instance of service object
      service = Service(
                        service_name = args["service_name"],
                        description = args["description"],
                        image_file = args["image_file"],
                        price = args["price"],
                        time_required = args["time_required"],
                        search_column = self.search_column(args)
                        )
        
      # add service to database
      db.session.add(service)
      db.session.commit()
      return {
        "message" : "Service created successfully"
      }, 200
    except Exception as e:
      # if any internal error then rollback the transaction
      db.session.rollback()
      return{
        "message" : f"Error creating service: {str(e)}"
      }, 500
      
      
  @auth_required("token")
  @roles_required("Admin")
  def put(self, service_id):
    parser = self.get_parser()
    args = parser.parse_args()
    try:
      service = Service.query.get(service_id)
      # check service exist or not
      if service:
        service.service_name = args["service_name"]
        service.description = args["description"]
        service.price = args["price"]
        service.time_required = args["time_required"]
        service.image_file = args["image_file"]
        service.search_column = self.search_column(args)
        db.session.commit()
        return {
          "message" : "Service updated successfully"
        }, 200
    except Exception as e:
      # if any internal error then rollback the transaction
      db.session.rollback()
      return{
        "message" : f"Error creating service: {str(e)}"
      }, 500
      
      
  @auth_required("token")
  @roles_required("Admin")
  def delete(self, service_id):
    try:
      service = Service.query.get(service_id)
      
      # check service exist or not
      if service:
        db.session.delete(service)
        db.session.commit()
        return {
          "message" : "Service deleted successfully"
        }, 200
    except Exception as e:
      # if any internal error then rollback the transaction
      db.session.rollback()
      return{
        "message" : f"Error creating service: {str(e)}"
      }, 500

      
admin_api.add_resource(
                       Services,
                       '/admin_api/get_services',
                       '/admin_api/create_service', 
                       '/admin_api/update_service/<int:service_id>',
                       '/admin_api/delete_service/<int:service_id>'
                      )