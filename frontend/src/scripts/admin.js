export default{
  data(){
      return{
        role : localStorage.getItem("role"),
        current_section : "",
        loading_service : true,
        loading_customer : true,
        loading_professional : true,
        loading_service_request : true,
        loading_professional_for_verification : true,
        successMessage : "",
        service : {
        "service_name" : "",
        "price" : "",
        "time_required" : "",
        "description" : "",
        "image_file" : ""
        },
        service_request : {
          "service_name" : "",
          "customer_name" : "",
          "city" : "",
          "state" : "",
          "date_of_request" : "",
          "date_of_completion" : "",
          "professional_name" : "",
          "rating" : "",
          "review" : "",
          "status" : ""
        },
        services : [],
        customers : [],
        professionals : [],
        profiles : [],
        service_requests : []
      }
  },

  methods: {
    formatDate(dateString){
      const date = new Date(dateString);
      return date.toLocaleDateString('en-GB').split("/").join("-");
    },

    showSection(section){
      this.current_section = section;
    },

    create_empty_service_object(){
      this.service = {
        "service_name" : "",
        "price" : "",
        "time_required" : "",
        "description" : "",
        "image_file" : ""
      }
    },


    async GetServices(){
      try{
        const response = await fetch("http://localhost:5000/admin_api/get_services",{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.services = responseData;
          this.loading_service = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async AddService(){
      try{
        const response = await fetch('http://localhost:5000/admin_api/create_service',{
          method : "POST",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem('auth_token')
          },
          body : JSON.stringify(this.service)
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.current_section = "";
          this.create_empty_service_object();
          this.GetServices();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async UpdateService(){
      try{
        const response = await fetch(`http://localhost:5000/admin_api/update_service/${this.service.service_id}`,{
          method : "PUT",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem('auth_token')
          },
          body : JSON.stringify(this.service)
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.create_empty_service_object();
          this.current_section = "";
          this.GetServices();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async DeleteService(service){
      try{
        const response = await fetch(`http://localhost:5000/admin_api/delete_service/${service.service_id}`,{
          method : "DELETE",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem('auth_token')
          },
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.current_section = "";
          this.GetServices();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async GetCustomers(){
      try{
        const response = await fetch("http://localhost:5000/api/get_customers",{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.customers = responseData;
          this.loading_customer = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async BlockCustomer(user_id){
      try{
        const response = await fetch(`http://localhost:5000/api/block_customer/${user_id}`,{
          method : "DELETE",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.current_section = "";
          this.GetCustomers();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async profile_verification(){
      try{
        const response = await fetch('http://localhost:5000//api/profile_verification',{
          method : "GET",
          headers : {
            "Content-Type" : 'application/json',
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        })
  
        const responseBody = await response.json();
        if(response.ok){
          this.profiles = responseBody;
          this.loading_professional_for_verification = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async verified_profile(user_id){
      try{
        const response = await fetch(`http://localhost:5000/api/verified_profile/${user_id}`,{
          method : "GET",
          headers : {
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.profile_verification();
        }
      }
      catch(error){
        console.log(error)
      }
    },

    async GetProfessionals(){
      try{
        const response = await fetch("http://localhost:5000/api/get_professionals",{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.professionals = responseData;
          this.loading_professional = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async BlockProfessional(user_id){
      try{
        const response = await fetch(`http://localhost:5000/api/block_professional/${user_id}`,{
          method : "DELETE",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.current_section = "";
          this.GetProfessionals();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async GetServiceRequest(){
      try{
        const response = await fetch("http://localhost:5000/api/get_service_requests",{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.service_requests = responseData;
          this.loading_service_request = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async EditServiceRequest(service_request){
      try{
        const formData = {
          "date_of_completion" : service_request.date_of_completion,
          "rating" : service_request.rating,
          "remarks" : service_request.remarks,
          "service_status" : service_request.service_status
        }
        const response = await fetch(`http://localhost:5000/api/edit_service_request/${service_request.service_request_id}`,{
          method : "PUT",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          },
          body : JSON.stringify(formData)
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.current_section = "";
        }
      }
      catch(error){
        console.log(error);
      }
    },

    toggleEditServiceRequestForm(service_request){
      this.service_request = { ...service_request };
      this.service_request["date_of_request"] = this.formatDate(this.service_request["date_of_request"]);
      this.service_request["date_of_completion"] = this.formatDate(this.service_request["date_of_completion"]);
      this.current_section = "EditServiceRequest";
    },

    toggleUpdateServiceForm(service){
      this.service = { ...service };
      this.current_section = "UpdateForm";
    },

    closeModal(event){
      if(event.target === event.currentTarget){  
        if(this.current_section === "addService" || this.current_section === "UpdateForm"){
          this.create_empty_service_object();
        }      
        this.current_section = "";
      }
    }
  }
}