import bcrypt
import os
import secrets

class Config():
  SECRET_KEY = os.environ.get("SECRET_KEY",secrets.token_hex(16))     # hash user credentials in session
  SQLALCHEMY_DATABASE_URI = None
  SQLALCHEMY_TRACK_MODIFICATIONS = None
  SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
  DEBUG = True
  
  
class DevelopmentConfiguration(Config):
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  SQLALCHEMY_DATABASE_URI =  'sqlite:///householdService.db'
  SECURITY_PASSWORD_HASH = "bcrypt"              # method for hashing password
  # SECURITY_PASSWORD_SALT = secrets.token_hex(16)
  SECURITY_PASSWORD_SALT = "this-is-salt"
  WTF_CSRF_ENABLED = False
  DEBUG = True
  
  
class ProductionConfiguration(Config):
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",'sqlite:///householdService.db')
  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = bcrypt.gensalt()
  WTF_CSRF_ENABLED = True
  DEBUG = True