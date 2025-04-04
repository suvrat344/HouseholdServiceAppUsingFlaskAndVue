import csv
import os
from flask import current_app
from flask_security import current_user

class Utility:
  @classmethod
  def fetch_state_city(cls):
    state_city = dict()
    fileLocation = os.path.join(current_app.root_path,'controller/Main','IndianCities.csv')
    with open(fileLocation,mode = "r",newline = "",encoding = "utf-8") as city:
      reader = csv.reader(city)
      next(reader)
      for row in reader:
        if(row[1] not in state_city):
          state = row[1].strip()
          state_city[state] = []
        city = row[0].strip()
        state_city[state].append(city)
      for state in state_city:
        state_city[state] = sorted(state_city[state])
    return state_city
  
  @classmethod
  def store_image(cls, file):
    id = current_user.user_id
    role = current_user.roles[0].name
    
    image_location_folder = os.path.join(current_app.root_path,f'static/images/{role}')
    
    if(not os.path.isdir(image_location_folder)):
      os.makedirs(image_location_folder)
      
    info_folder = os.path.join(image_location_folder,f"{id}_info")
    
    if(not os.path.isdir(info_folder)):
      os.makedirs(info_folder)
      
    file_extension = file.filename.split(".")[-1]
    image_path = os.path.join(info_folder,f"{id}.{file_extension}")
    file.save(image_path)
      
  @classmethod
  def store_resume(cls, file):
    id = current_user.user_id
    role = current_user.roles[0].name
    
    resume_location_folder = os.path.join(current_app.root_path,f'static/images/{role}')
    
    if(not os.path.isdir(resume_location_folder)):
      os.makedirs(resume_location_folder)
      
    info_folder = os.path.join(resume_location_folder,f"{id}_info")
    
    if(not os.path.isdir(info_folder)):
      os.makedirs(info_folder)
      
    resume_path = os.path.join(info_folder,f"{id}.pdf")
    file.save(resume_path)