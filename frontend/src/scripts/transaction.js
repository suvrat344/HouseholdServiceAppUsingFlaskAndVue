export default{
  data : function(){
    return{
      successMessage : "",
      failedMessage : "",
      service_requests : [],
      service_request_id : "",
      showUpdateForm : false,
      showReviewForm : false,
      rating : "",
      remarks : "",
      selectedChoice : "",
      loading_customer_transaction : true,
      service : {
        "service_id" : "",
        "service_request_id" : "",
        "date_of_request" : "",
        "date_of_completion" : "",
        "problem_description" : ""
      },
      error_message : {},
      user_id : localStorage.getItem("user_id"),
      role : localStorage.getItem("role")
    }
  },

  methods : {
    formatDate(dateString){
      const date = new Date(dateString);
      return date.toLocaleDateString('en-GB').split("/").join("-");
    },

    // Methods related to customer review form
    validateRating(){
      if(this.rating < 1 || this.rating > 5){
        this.$set(this.error_message, "RatingError", "Rating can be between 1 and 5");
      }
      else{
        this.$set(this.error_message, "RatingError", "");
        return true;
      }
    },

    validateRemarks(){
      if(this.remarks === "" || this.remarks.length > 200){
        this.$set(this.error_message, "RemarksError", "Remarks in less than 200 words.");
      }
      else{
        this.$set(this.error_message, "RemarksError", "");
        return true;
      }
    },

    validateReviewForm(){
      if(!this.validateRating()){
        return
      }
      else if(!this.validateRemarks()){
        return
      }
      else{
        this.customer_close_request();
      }
    },
    // Method related to customer review form ends


    // Method related to customer actions starts
    async fetch_customer_service_request(){
      try{
        const response = await fetch(`http://localhost:5000/customer_api/get_service_request/${this.user_id}`,{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.service_requests = responseData ? responseData : [];
          this.loading_customer_transaction = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async updateServiceRequest(service_request_id){
      try{
        const formData = {
          "user_id" : this.user_id,
          "service_id" : this.service.service_id,
          "date_of_request" : this.service.date_of_request,
          "date_of_completion" : this.service.date_of_completion,
          "problem_description" : this.service.problem_description
        }
        
        const response = await fetch(`http://localhost:5000/customer_api/update_service_request/${service_request_id}`,{
          method : "PUT",
          headers : {
            'Content-Type' : 'application/json',
            "Authentication-Token" : localStorage.getItem("auth_token")
          },
          body : JSON.stringify(formData)
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.showUpdateForm = false;
          this.fetch_customer_service_request();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async customer_cancel_request(service_request){
      try{
        let flag = service_request.status === "Accepted" ? "true" : "false";
        const response = await fetch(`http://localhost:5000/customer_api/cancel_service_request/${service_request.service_request_id}?is_accepted=${flag}`,{
          method : "DELETE",
          headers : {
            "Authentication-Token" : localStorage.getItem("auth_token"),
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.fetch_customer_service_request();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async customer_close_request(){
      const formData = {
        "rating" : this.rating,
        "remarks" : this.remarks
      };
      try{
        const response = await fetch(`http://localhost:5000/api/customer_close_service_request/${this.service_request_id}`,{
          method : "POST",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token"),
          },
          body : JSON.stringify(formData)
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.showReviewForm = false;
          this.service_request_id = "";
          this.fetch_customer_service_request();
        }
        else{
          if(responseData.message === "RatingError"){
            this.$set(this.error_message, "RatingError", responseData.message);
          }
          else{
            this.$set(this.error_message, "RatingError", "");
          }

          if(responseData.message === "RemarksError"){
            this.$set(this.error_message, "RemarksError", responseData.message);
          }
          else{
            this.$set(this.error_message, "RemarksError", "");
          }
        }
      }
      catch(error){
        console.log(error);
      }
    },
    // Method related to customer actions ends

    // Method related to professional action starts
    async fetch_professional_service_request(){
      try{
        const response = await fetch(`http://localhost:5000/api/professional_transaction/${this.user_id}`,{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.service_requests = responseData;
          this.loading = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    // Method related to professional action ends
    toggleUpdateServiceRequest(service_request){
      this.showUpdateForm = true;
      this.service.service_request_id = service_request.service_request_id;
      this.service.service_id = service_request.service_id;
      this.service.service_name = service_request.service_name;
      this.service.date_of_request = this.formatDate(service_request.date_of_request);
      this.service.price = service_request.price;
      this.service.time_required = service_request.time_required;
      this.service.problem_description = service_request.problem_description;
    },

    toggleReviewForm(service_request_id){
      this.showReviewForm = true;
      this.service_request_id = service_request_id;
    },

    closeModal(event){
      if(event.target === event.currentTarget){
        this.showUpdateForm = false;
        this.showReviewForm = false;
      }
    },
  },
}