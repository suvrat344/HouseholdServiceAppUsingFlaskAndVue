export default{
  data : function(){
    return{
      isProfileComplete : false,
      user_credential : {},
      user_detail: {
        "name" : "",
        "contact_number" : "",
        "state" : "",
        "city" : "",
        "address" : "",
        "pin_code" : "",
        "image_file" : "",
        "image_url" : "",
        "experience" : "",
        "service_type" : "",
        "resume_file" : "",
        "resume_url" : ""
      },
      error_message : {},
      state_city : localStorage.getItem("state_city"),
      states : [],
      cities : [],
      services_name : {},
      selectedState : "",
      selectedCity : "",
      selectedService : "",
      image_file : "",
      resume_file :  "",
    }
  },

  methods : {
    fetch_state(){
      this.states = Object.keys(JSON.parse(this.state_city));
    },

    fetch_city(){
      this.user_detail.state = this.selectedState;
      this.cities = JSON.parse(this.state_city)[this.selectedState];
    },

    async fetch_services_name(){
      try {
        const response = await fetch("http://localhost:5000/admin_api/get_services?only_names=true",{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });
      
        if(response.ok){
          const responseData = await response.json();
          this.services_name = responseData.services_name;
        } 
      }
      catch(error){
        console.log(error);
      }
    },

    validateName(){
      const result = this.user_detail.name;
      if(result.length <= 30){
        this.$set(this.error_message,'NameError',"");
        return true;
      }
      else{
        this.$set(this.error_message,'NameError',"Name must be less than 30 characters.");
      }
    },

    validatePhoneNumber(){
      const regex = /^[6789][\d]{9}$/;
      const result = regex.test(this.user_detail.contact_number);
      if(result){
        this.$set(this.error_message, 'ContactNumberError', "");
        return true;
      }
      else{
        this.$set(this.error_message, 'ContactNumberError', "Please enter a valid phone number. It should start with 6, 7, 8, or 9 and have 10 digits.");
      }
    },

    validatePinCode(){
      const regex = /^[\d]{6}$/;
      const result = regex.test(this.user_detail.pin_code);
      if(result){
        this.$set(this.error_message, 'PinCodeError', "");
        return true;
      }
      else{
        this.$set(this.error_message, 'PinCodeError', "Please enter a valid pin code. It should be 6 digits long and contain only numbers.");
      }
    },

    validateAddress(){
      const result = this.user_detail.address;
      if(result.length <= 50){
        this.$set(this.error_message, 'AddressError', "");
        return true;
      }
      else{
        this.$set(this.error_message, 'AddressError', "Address must be less than 50 characters.");
      }
    },

    validateExperience(){
      const result = this.user_detail.experience;
      if(result < 0 || result > 50){
        this.$set(this.error_message, "ExperienceError", "Please enter your years of experience (between 0 and 50).");
      }
      else{
        this.$set(this.error_message, "ExperienceError","");
        return true;
      }
    },

    validateImage(){
      const file = this.$refs.image_file.files[0];
      if(file){
        const allowed_extensions = ['jpg', 'png'];
        const fileExtension = file.name.split(".").pop().toLowerCase();
        const maxSize = 2 * 1024 * 1024;

        if(!allowed_extensions.includes(fileExtension)){
          this.$set(this.error_message, 'ImageError', "Please upload an image file with .jpg or .png extension.");
          this.image_file = "";
        }
        else if(file.size > maxSize){
          this.$set(this.error_message, 'ImageError', "The file size is too large. Please upload an image under 2MB.");
          this.image_file = "";
        }
        else{
          this.$set(this.error_message, 'ImageError', "");
          this.user_detail.image_file = file;
          return true;
        }
      }
      else if(!file && this.isEditingProfile){
        this.user_detail.image_file = "";
        return true;
      }
    },

    validateResume(){
      const file = this.$refs.resume_file.files[0];
      if(file){
        const allowed_extensions = ['pdf'];
        const fileExtension = file.name.split(".").pop().toLowerCase();
        const maxSize = 10 * 1024 * 1024;
        if(!allowed_extensions.includes(fileExtension)){
          this.$set(this.error_message, "ResumeError", "Please upload a resume file with .pdf extension.");
          this.resume_file = "";
        }
        else if(file.size > maxSize){
          this.$set(this.error_message, "ResumeError", "The file size is too large. Please upload an image under 10MB.");
          this.resume_file = "";
        }
        else{
          this.$set(this.error_message, "ResumeError", "");
          this.user_detail.resume_file = file;
          return true;
        }
      }
      else if(!file && this.isEditingProfile){
        this.user_detail.resume_file = "";
        return true;
      }
    },  

    validateUserDetails(){
      if(this.validateName() && this.validatePhoneNumber() && this.validatePinCode() && this.validateImage() && this.validateAddress())
      {
        this.user_detail.city = this.selectedCity;
        
        const isRoleValid = this.user_credential.role === "Professional" ? this.validateExperience() && this.validateResume() : true;

        if(isRoleValid){
          if(this.isEditingProfile){
            this.updateUserDetail();
          }
          else if(this.isProfileComplete){
            this.submitUserDetail();
          }
        }
      }
    },
      
    async fetch_user_detail(){
      try {
        const response = await fetch(`http://localhost:5000/auth_api/user_details/${this.user_credential.user_id}`,{
          method : "GET",
          headers : {
            'Content-Type' : 'application/json',
            'Authentication-Token' : localStorage.getItem("auth_token")
          }
        });
        const responseData = await response.json();
        if(response.ok){
          this.user_detail = {
            "name" : responseData.name,
            "contact_number" : responseData.contact_number,
            "city" : responseData.city,
            "state" : responseData.state,
            "address" : responseData.address,
            "pin_code" : responseData.pin_code,
            "image_url" : responseData.image_url,
            "resume_url" : this.user_credential.role == "Professional" ? responseData.resume_url : "",
            "experience" : this.user_credential.role == "Professional" ? responseData.experience : "",
            "service_type" : this.user_credential.role == "Professional" ? responseData.service_type : "",
            "image_file" : "",
            "resume_file" : ""
            }
          }
        }
      catch(error){
        console.log(error);
      }
    },

    async submitUserDetail(){
      try{
        const formData = new FormData();
        formData.append("user_id", this.user_credential.user_id);
        formData.append("name", this.user_detail.name);
        formData.append("contact_number", this.user_detail.contact_number);
        formData.append("city", this.user_detail.city);
        formData.append("state", this.user_detail.state);
        formData.append("pin_code", this.user_detail.pin_code);
        formData.append("address", this.user_detail.address);
        formData.append("image_file", this.user_detail.image_file)

        if(this.user_credential.role === "Professional"){
          this.user_detail.service_type = this.selectedService;
          formData.append("experience", this.user_detail.experience)
          formData.append("resume_file", this.user_detail.resume_file)
          formData.append("service_type", this.user_detail.service_type)
        }
        let response = await fetch("http://localhost:5000/auth_api/complete_profile",{
          method : "POST",
          headers : {
              'Authentication-Token' : localStorage.getItem("auth_token")
            },
            body : formData
        });
      
        const responseData = await response.json();
          if(response.ok){
            this.successMessage = responseData.Success;
            localStorage.setItem("profile_status","Completed");
            this.selectedState = "";
            this.selectedCity = "";
            this.selectedService = "";
            this.isProfileComplete = false;
            if(this.user_credential.role === "Professional"){
              alert("Profile submiited successfully wait for 2 days");
              this.$router.push("/");
            }
          }
          else{
            if(responseData.NameError){
              this.$set(this.error_message,"NameError", responseData.NameError);
            }
            else{
              this.$set(this.error_message,"NameError", "");
            }

            if(responseData.AddressError){
              this.$set(this.error_message,"AddressError", responseData.AddressError);
            }
            else{
              this.$set(this.error_message,"AddressError", "");
            }

            if(responseData.ContactNumberError){
              this.$set(this.error_message,"ContactNumberError", responseData.ContactNumberError);
            }
            else{
              this.$set(this.error_message,"ContactNumberError", "");
            }

            if(responseData.CityError){
              this.$set(this.error_message,"CityError", responseData.CityError);
            }
            else{
              this.$set(this.error_message,"CityError", "");
            }

            if(responseData.StateError){
              this.$set(this.error_message,"StateError", responseData.StateError);
            }
            else{
              this.$set(this.error_message,"StateError", "");
            }

            if(responseData.PinCodeError){
              this.$set(this.error_message,"PinCodeError", responseData.PinCodeError);
            }
            else{
              this.$set(this.error_message,"PinCodeError", "");
            }

            if(responseData.ExperienceError){
              this.$set(this.error_message,"ExperienceError", responseData.ExperienceError);
            }
            else{
              this.$set(this.error_message,"ExperienceError", "");
            }

            if(responseData.ServiceTypeError){
              this.$set(this.error_message,"ServiceTypeError", responseData.ServiceTypeError);
            }
            else{
              this.$set(this.error_message,"ServiceTypeError", "");
            }

            if(responseData.ImageError){
              this.$set(this.error_message,"ImageError", responseData.ImageError);
            }
            else{
              this.$set(this.error_message,"ImageError", "");
            }

            if(responseData.ResumeError){
              this.$set(this.error_message,"ResumeError", responseData.ResumeError);
            }
            else{
              this.$set(this.error_message,"ResumeError", "");
            }
          } 
        }  
      catch(error){
        console.log(error);
      }
    },

  async updateUserDetail(){
    try{
      const formData = new FormData();
      formData.append("user_id", this.user_credential.user_id);
      formData.append("name", this.user_detail.name);
      formData.append("contact_number", this.user_detail.contact_number);
      formData.append("city", this.user_detail.city);
      formData.append("state", this.user_detail.state);
      formData.append("pin_code", this.user_detail.pin_code);
      formData.append("address", this.user_detail.address);
      formData.append("image_file", this.user_detail.image_file);
      formData.append("experience", this.user_credential.role == "Professional" ? this.user_detail.experience : "");
      formData.append("service_type", this.user_credential.role == "Professional" ? this.user_detail.service_type : "");
      formData.append("resume_file", this.user_detail.resume_file);

      let response = await fetch(`http://localhost:5000/auth_api/update_user_details/${this.user_credential.user_id}`,{
        method : "PUT",
        headers : {
            'Authentication-Token' : localStorage.getItem("auth_token")
          },
          body : formData
      });
      const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.Success;
          this.$emit("close-Profile");
          this.selectedState = "";
          this.selectedCity = "";
          this.fetch_user_detail();
        }
        else{
          if(responseData.NameError){
            this.error_message.NameError = responseData.NameError;
          }
          else if(responseData.AddressError){
            this.error_message.AddressError = responseData.AddressError;
          }
          else if(responseData.ContactNumberError){
            this.error_message.ContactNumberError = responseData.ContactNumberError;
          }
          else if(responseData.CityError){
            this.error_message.CityError = responseData.CityError;
          }
          else if(responseData.StateError){
            this.error_message.StateError = responseData.StateError;
          }
          else if(responseData.PinCodeError){
            this.error_message.PinCodeError = responseData.PinCodeError;
          }
          else if(responseData.ImageError){
            this.error_message.ImageError = responseData.ImageError;
          }
        }
      }  
    catch(error){
      console.log(error);
      }
    },

    check_profile_complete(){
      const status = localStorage.getItem("profile_status");
      if(status !== "Completed"){
        this.isProfileComplete = true;
      }
      else{
        this.fetch_user_detail();
      }
    },

    closeModal(event){
      if(event.target === event.currentTarget){
        this.$emit('close-Profile');
      }
    },
  }
}