from flask import Flask
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from controller.config import DevelopmentConfiguration, ProductionConfiguration
from controller.Main.auth_api import auth_api, auth_api_bp
from controller.Admin.admin import admin_bp
from controller.Admin.admin_api import admin_api, admin_api_bp
from controller.Customer.customer import customer_bp
from controller.Customer.customer_api import customer_api, customer_api_bp
from controller.Professional.professional import professional_bp
from model.models import User, Role
from controller.extensions import db
import nltk
import os
from werkzeug.security import generate_password_hash


def initialize_nltk_resources():
  try:
    nltk.data.find('tokenizers/punkt')
  except LookupError:
    nltk.download("punkt")
  try:
    nltk.data.find('corpora/stopwords')
  except LookupError:
    nltk.download("stopwords")
  try:
    nltk.data.find('sentiment/vader_lexicon')
  except LookupError:
    nltk.download("vader_lexicon")
    

def init_app():
  householdService_app = Flask(__name__)
  CORS(householdService_app)
  if(os.getenv("FLASK_ENV") == "development"): 
    householdService_app.config.from_object(DevelopmentConfiguration)
  elif(os.getenv("FLASK_ENV") == "production"):
    householdService_app.config.from_object(ProductionConfiguration)
  db.init_app(householdService_app)
  admin_api.init_app(householdService_app)
  auth_api.init_app(householdService_app)
  customer_api.init_app(householdService_app)
  householdService_app.register_blueprint(admin_bp)
  householdService_app.register_blueprint(admin_api_bp)
  householdService_app.register_blueprint(auth_api_bp)
  householdService_app.register_blueprint(customer_bp)
  householdService_app.register_blueprint(customer_api_bp)
  householdService_app.register_blueprint(professional_bp)
  householdService_app.app_context().push()
  datastore = SQLAlchemyUserDatastore(db, User, Role)
  householdService_app.security = Security(householdService_app, datastore)
  return householdService_app
  
app = init_app()


with app.app_context():
  db.create_all()
  
  app.security.datastore.find_or_create_role(name = "Admin", description = "Superuser of an app")
  app.security.datastore.find_or_create_role(name = "Customer", description = "Customer of app")
  app.security.datastore.find_or_create_role(name = "Professional", description = "Professional of app")
  db.session.commit()
  
  if(not app.security.datastore.find_user(email = "user@admin.com")):
    app.security.datastore.create_user(email = "user@admin.com", 
                                      username = "admin01", 
                                      password = generate_password_hash("1234"),
                                      roles = ["Admin"])   
  db.session.commit()

if __name__ == "__main__":
  app.run(debug = True)