from flask import Blueprint, jsonify, request
from flask_security import auth_required, roles_required
from model.models import *
from controller.extensions import db

admin_bp = Blueprint("admin_bp", "__name__")


@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/get_customers', methods = ["GET"])
def get_customers():
  try:
    customers = db.session.query(User).join(UserRole).join(Role).filter(Role.name == "Customer",User.active == True).all()
    customer_list = []
    for customer in customers:
      customer_dict = {}
      if(customer.user_details):
        customer_dict["user_id"] = customer.user_id
        customer_dict["name"] = customer.user_details.name
        customer_dict["contact_number"] = customer.user_details.contact_number
        customer_dict["address"] = customer.user_details.address
        customer_dict["city"] = customer.user_details.city
        customer_dict["state"] = customer.user_details.state
        customer_dict["pin_code"] = customer.user_details.pin_code
        customer_list.append(customer_dict)
    return jsonify(customer_list), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500


@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/block_customer/<int:user_id>',methods=["DELETE"])
def block_customer(user_id):
  try:
    user = User.query.get(user_id)
    user.active = False
    db.session.commit()
    return jsonify({
      "message" : "Customer account blocked"
    })
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500
    
    
@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/profile_verification', methods = ["GET"])
def profile_verification():
  try:
    professionals = User.query.filter_by(profile_verified = True).all()
    professional_list = []
    for professional in professionals:
      professional_dict = {}
      if(professional.user_details):
        resume_url = f"/static/images/professional/{professional.user_id}_info/{professional.professional_qualifications.resume}"
        professional_dict["user_id"] = professional.user_id
        professional_dict["name"] = professional.user_details.name
        professional_dict["contact_number"] = professional.user_details.contact_number
        professional_dict["address"] = professional.user_details.address
        professional_dict["city"] = professional.user_details.city
        professional_dict["state"] = professional.user_details.state
        professional_dict["pin_code"] = professional.user_details.pin_code
        professional_dict["service_type"] = professional.professional_qualifications.service_type
        professional_dict["experience"] = professional.professional_qualifications.experience
        professional_dict["resume_url"] = resume_url
        professional_list.append(professional_dict)
    return jsonify(professional_list), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500
    
    
@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/verified_profile/<int:user_id>', methods = ["GET"])
def verified_profile(user_id):
  try:
    professional = User.query.get(user_id)
    professional.profile_verified = False
    db.session.commit()
    return jsonify({
      "message" : "Profile verified successfully"
      }), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500
    
    
@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/get_professionals', methods = ["GET"])
def get_professionals():
  try:
    professionals = db.session.query(User).join(UserRole).join(Role).filter(Role.name == "Professional",User.active == True, User.profile_verified == False).all()
    professional_list = []
    for professional in professionals:
      professional_dict = {}
      if(professional.user_details):
        resume_url = f"static/images/professional/{professional.user_id}_info/{professional.professional_qualifications.resume}"
        professional_dict["user_id"] = professional.user_id
        professional_dict["name"] = professional.user_details.name
        professional_dict["contact_number"] = professional.user_details.contact_number
        professional_dict["address"] = professional.user_details.address
        professional_dict["city"] = professional.user_details.city
        professional_dict["state"] = professional.user_details.state
        professional_dict["pin_code"] = professional.user_details.pin_code
        professional_dict["service_type"] = professional.professional_qualifications.service_type
        professional_dict["experience"] = professional.professional_qualifications.experience
        professional_dict["resume_url"] = resume_url
        professional_list.append(professional_dict)
    return jsonify(professional_list), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500


@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/block_professional/<int:user_id>',methods=["DELETE"])
def block_professional(user_id):
  try:
    user = User.query.get(user_id)
    user.active = False
    db.session.commit()
    return jsonify({
      "message" : "Professional account blocked"
    })
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500
    
    
@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/get_service_requests', methods = ["GET"])
def get_service_requests():
  try:
    service_requests = ServiceRequest.query.order_by(db.desc(ServiceRequest.date_of_completion)).all()
    service_request_list = []
    for service_request in service_requests:
      service_request_dict = {}
      customer = User.query.get(service_request.customer_id)
      service_request_dict["service_request_id"] = service_request.service_request_id
      service_request_dict["service_name"] = service_request.related_service.service_name
      service_request_dict["customer_name"] = customer.user_details.name
      service_request_dict["service_status"] = service_request.service_status
      service_request_dict["city"] = customer.user_details.city
      service_request_dict["state"] = customer.user_details.state
      service_request_dict["date_of_request"] = service_request.date_of_request
      service_request_dict["date_of_completion"] = service_request.date_of_completion
      if(service_request.service_status in ["Accepted", "Closed"] or (service_request.service_status == "Cancelled" and service_request.professional_id is not None)):
        professional = User.query.get(service_request.professional_id)
        service_request_dict["professional_name"] = professional.user_details.name
        service_request_dict["rating"] = service_request.rating
        service_request_dict["review"] = service_request.remarks
      service_request_list.append(service_request_dict)
    return jsonify(service_request_list), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500
    
    
@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/edit_service_request', methods = ["GET","PUT"])
def edit_service_request(service_request_id):
  try:
    service_request = ServiceRequest.query.filter_by(service_request_id = service_request_id).first()
    data = request.get_json()
    service_request.date_of_completion = data["date_of_completion"]
    service_request.rating = data["rating"]
    service_request.remarks = data["remarks"]
    service_request.service_status = data["service_status"]
    db.session.commit()
    return jsonify({
      "message" : "Service request updated successfully"
      }), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500
    
    
@auth_required("token")
@roles_required("Admin")
@admin_bp.route('/api/close_service_request', methods = ["GET"])
def close_service_request(service_request_id):
  try:
    service_requests = ServiceRequest.query.order_by(db.desc(ServiceRequest.date_of_completion)).all()
    service_request_list = []
    for service_request in service_requests:
      service_request_dict = {}
      customer = User.query.get(service_request.customer_id)
      service_request_dict["service_request_id"] = service_request.service_request_id
      service_request_dict["service_name"] = service_request.related_service.service_name
      service_request_dict["customer_name"] = customer.user_details.name
      service_request_dict["service_status"] = ServiceRequest.service_status
      service_request_dict["city"] = customer.user_details.city
      service_request_dict["state"] = customer.user_detail.state
      service_request_dict["date_of_request"] = service_request.date_of_request
      service_request_dict["date_of_completion"] = service_request.date_of_completion
      if(service_request.service_status in ["Accepted", "Closed"] or (service_request.service_status == "Cancelled" and service_request.professional_id is not None)):
        professional = User.query.get(service_request.professional_id)
        service_request_dict["professional_name"] = professional.user_details.name
        service_request_dict["rating"] = service_request.rating
        service_request_dict["review"] = service_request.review
      service_request_list.append(service_request_dict)
    return jsonify(service_request_list), 200
  except Exception as e:
    return jsonify({
        "message": f"Error retrieving services: {str(e)}"
      }), 500