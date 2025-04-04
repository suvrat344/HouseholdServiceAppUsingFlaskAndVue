from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from flask_security import auth_required, current_user, roles_required
from model.models import *
from controller.extensions import db


professional_bp = Blueprint("professional_bp", "__name__")

@auth_required("token")
@roles_required("Professional")
@professional_bp.route("/api/professional_request/<int:user_id>")
def professional_request(user_id):
  try:
    professional = User.query.get(user_id)
    professional_service_type = professional.professional_qualifications.service_type
    service_id = Service.query.filter_by(service_name = professional_service_type).first().service_id
    
    pending_requests = ServiceRequest.query.filter_by(
                                                      service_id = service_id,
                                                      service_status = "Pending"
                                                      ).all()
    
    for pending_request in pending_requests:
      customer_city = User.query.get(pending_request.customer_id).user_details.city
      professional_action = ProfessionalAction.query.filter_by(
                                                          service_request_id = pending_request.service_request_id,
                                                          professional_id = professional.user_id
                                                          ).first()
      if(pending_request.service_status == "Pending" and customer_city == professional.user_details.city):
        if(professional_action is None):
          professional_option = ProfessionalAction(
                                                    service_request_id = pending_request.service_request_id,
                                                    professional_id = professional.user_id,
                                                    action_type = "Pending" 
                                                  )
          db.session.add(professional_option)
          db.session.commit()
    service_request_details = ProfessionalAction.query.filter_by(
                                                                  professional_id = professional.user_id,
                                                                  action_type = "Pending" 
                                                                ).all()
    
    service_request_list = []
    for service_request_detail in service_request_details:
      service_request_dict = {}
      customer_id = service_request_detail.related_service_request.customer_id
      customer = User.query.get(customer_id)
      service_request_dict["service_request_id"] =  service_request_detail.related_service_request.service_request_id
      service_request_dict["icon"] =  service_request_detail.related_service_request.related_service.image_file
      service_request_dict["service_name"] =  service_request_detail.related_service_request.related_service.service_name
      service_request_dict["contact_number"] =  customer.user_details.contact_number
      service_request_dict["address"] = customer.user_details.address
      service_request_dict["city"] = customer.user_details.city
      service_request_dict["state"] = customer.user_details.state
      service_request_dict["date_of_request"] =  service_request_detail.related_service_request.date_of_request.isoformat()
      service_request_dict["date_of_completion"] = service_request_detail.related_service_request.date_of_completion.isoformat()
      service_request_list.append(service_request_dict)
    return jsonify(service_request_list), 200
  except Exception as e:
    return jsonify({
      "message" : e
    }), 500


@auth_required('token')
@roles_required('Professional')
@professional_bp.route("/api/accept_request/<int:user_id>/<int:service_request_id>", methods = ["GET"])
def accept_request(user_id, service_request_id):
  try:
    professional_action = ProfessionalAction.query.filter_by(
                                                              service_request_id = service_request_id,
                                                              professional_id = user_id
                                                            ).first()
    service_request = professional_action.related_service_request
    service_request.professional_id = user_id
    service_request.service_status = "Accepted"
    professional_action.action_type = "Accepted"
    professional_action = ProfessionalAction.query.filter(
                                    ProfessionalAction.professional_id != user_id,
                                    ProfessionalAction.service_request_id == service_request_id,
                                    ProfessionalAction.action_type != "Rejected"
                                    ).delete(synchronize_session = False)
    db.session.commit()
    return jsonify({
      "message" : "Request accepted"
    }), 200
  except Exception as e:
    return jsonify({
      "message" : e
    }), 500
  
  
@auth_required('token')
@roles_required('Professional')
@professional_bp.route("/api/reject_request/<int:user_id>/<int:service_request_id>", methods = ["GET"])
def reject_request(user_id, service_request_id):
  try:
    professional_action = ProfessionalAction.query.filter_by(
                                                              service_request_id = service_request_id,
                                                              professional_id = user_id
                                                            ).first()
    professional_action.action_type = "Rejected"
    db.session.commit()
    return jsonify({
      "message" : "Request rejected"
    }), 200
  except Exception as e:
    return jsonify({
      "message" : e
    }), 500


@auth_required('token')
@roles_required('Professional')
@professional_bp.route("/api/close_request/<int:user_id>/<int:service_request_id>", methods = ["GET"])
def close_request(user_id, service_request_id):
  try:
    service_request = ServiceRequest.query.get(service_request_id = service_request_id)
    if(service_request.date_of_completion + timedelta(days = 1) == datetime.now()):
      professional_action = ProfessionalAction.query.filter_by(
                                                    professional_id = service_request.professional_id,
                                                    service_request_id = service_request_id
                                                    ).first()
      service_request.service_status = "Closed"
      professional_action.action_type = "Closed"
      db.session.commit()

    return jsonify({
      "message" : "Request closed"
    }), 200
  except Exception as e:
    return jsonify({
      "message" : e
    }), 500
    

@auth_required('token')
@roles_required('Professional')
@professional_bp.route("/api/professional_transaction/<int:user_id>", methods = ["GET"])
def professional_transaction(user_id):
  try:
    professional_history = ProfessionalAction.query.filter(
                              ProfessionalAction.professional_id == user_id,
                              ProfessionalAction.action_type  != "Pending"
                           ).all()
    
    service_request_list = []
    for professional_action in professional_history:
      service_request_dict = {}
      customer = User.query.get(professional_action.related_service_request.customer_id)
      service_request_dict["service_request_id"] = professional_action.related_service_request.service_request_id
      service_request_dict["service_name"] = professional_action.related_service_request.related_service.service_name
      service_request_dict["date_of_request"] = professional_action.related_service_request.date_of_request
      service_request_dict["date_of_completion"] = professional_action.related_service_request.date_of_completion
      service_request_dict["service_status"] = professional_action.related_service_request.service_status
      service_request_dict["customer_name"] = customer.user_details.name
      service_request_dict["contact_number"] = customer.user_details.contact_number
      service_request_dict["city"] = customer.user_details.city
      service_request_dict["state"] = customer.user_details.state
      service_request_dict["address"] = customer.user_details.address
      service_request_list.append(service_request_dict)
    return jsonify(service_request_list), 200
  except Exception as e:
    return jsonify({
      "message" : e
    }), 500