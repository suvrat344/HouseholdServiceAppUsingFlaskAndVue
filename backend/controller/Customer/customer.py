from flask import Blueprint, jsonify, request
from flask_security import auth_required, roles_required
from model.models import *
from controller.extensions import db

customer_bp = Blueprint("customer_bp", "__name__")

class validateReviewForm():
  def validate_rating(self, rating):
    if(rating == ""):
      return ("RatingError","Rating cannot be blank")
    elif(int(rating) < 1 or int(rating) > 5):
      return ("RatingError","Rating can be between 1 and 5")
    else:
      return ("Success", "Rating verified")
    
    
  def validate_remarks(self, remarks):
    if(remarks == ""):
      return ("RemarksError","Remarks cannot be blank")
    elif(len(remarks) > 200):
      return ("RemarksError","Remarks in less than 200 words")
    else:
      return ("Success", "Remarks verified")
    
    
  def validateReview(self,data):
    rating_message, rating_message_value = self.validate_rating(data["rating"])
    if(rating_message != "Success"):
      return (rating_message, rating_message_value)
    
    remark_message, remark_message_value = self.validate_remarks(data["remarks"])
    if(remark_message != "Success"):
      return (remark_message, remark_message_value)
    
    if(rating_message == "Success" and remark_message == "Success"):
      return ("Success", "Review form submitted successfully")
    

@auth_required("token")
@roles_required("Customer")
@customer_bp.route("/api/customer_close_service_request/<int:service_request_id>",methods=["POST"])
def customer_close_service_request(service_request_id):
  data = request.get_json()
  
  validator = validateReviewForm()
  message, message_value = validator.validateReview(data)
  
  if(message != "Success"):
    return jsonify({
      message : message_value
    }), 400
    
  rating = data.get("rating")
  remarks = data.get("remarks")
  service_request = ServiceRequest.query.get(service_request_id)
  professional_action = ProfessionalAction.query.filter_by(
                                                    professional_id = service_request.professional_id,
                                                    service_request_id = service_request_id
                                                    ).first()
  service_request.service_status = "Closed"
  service_request.professional_rating = rating
  service_request.remarks = remarks
  professional_action.action_type = "Closed"
  db.session.commit()
  return jsonify({
    message : message_value
  }), 200