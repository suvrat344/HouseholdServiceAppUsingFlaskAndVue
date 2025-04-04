export default{
  data : function(){
    return{
      info : [
        {
          "icon" : "fa fa-database",
          "heading" : "Large Number of Services Provided",
          "description" : "We are a company providing a wide range of maintenance and many other services."
        },
        {
          "icon" : "fa fa-user",
          "heading" : "15 Years of Professional Experience",
          "description" : "We work to ensure people's comfort at their home, and to provide the best and the fastest."
        },
        {
          "icon" : "fa fa-users",
          "heading" : "A Large Number of Grateful Customers",
          "description" : "We have been working for years to improve our skills, to expand the spheres of our work."
        }
      ],
      more_services : [
        "Bathroom Repair", 
        "Drywall Repair", 
        "Garage Door Repair", 
        "Ceiling Fan Repair", 
        "Electrical Repair", 
        "Grout Repair", 
        "Countertop Repair", 
        "Faucet Repair", 
        "Gutter Repair", 
        "Deck Repair", 
        "Flooring Repair", 
        "Handrail Repair", 
        "Door Repair", 
        "Furniture Repair", 
        "Kitchen Repair"
      ],
      choose : [
        {
          "title" : "National Standards, Local Owners",
          "description" : "Qualified Agents All our team members are high-qualified, educated and skilled agents. All of them are being trained according to the latest technologies.",
          "icon" : "fa fa-sticky-note"
        },
        {
          "title" : "Professional Approach",
          "description" : "Best Offers We provide discounts on the most popular services and on the season services, so you could definitely receive any help without delay.",
          "icon" : "fab fa-tencent-weibo"
        },
        {
          "title" : "Worry-Free Experience",
          "description" : "We accept requests and phone calls 24/7 so you could resolve any problem whenever you need. Our emergency team will be at your place",
          "icon" : "fa fa-handshake"
        },
        {
          "title" : "Qualified Agents",
          "description" : "Quality of work and speed of fulfilment. We always stand for doing our job fast and at the highest level as understand people value their time and money.",
          "icon" : "fa fa-user"
        },
        {
          "title" : "Whole Home Improvement Team",
          "description" : "Our prices are both fair and affordable for all people. We offer flexible discount system so you could use any service you need.",
          "icon" : "fa fa-users"
        },
        {
          "title" : "Best Offers",
          "description" : "Help with any domestic problem. You can choose the service from our list, or if you need any other maintenance help, we will gladly do even non-standard work!",
          "icon" : "fab fa-slideshare"
        }
      ],
      services : [],
      service_requests : [],
      successMessage : "",
      failedMessage : "",
      isEditingProfile : false,
      showAddServiceRequestForm : false,
      loading_services : true,
      load_service_request : true,

      // Services related data
      service : {
        "user_id" : localStorage.getItem("user_id"),
        "service_id" : "",
        "service_name" : "",
        "date_of_request" : "",
        "date_of_completion" : "",
        "price" : "",
        "time_required" : "",
        "problem_description" : ""
      },
      user_id : localStorage.getItem("user_id"),
      role : localStorage.getItem("role"),
    }
  },
  methods : {
    empty_service(){
      this.service = {
        "user_id" : localStorage.getItem("user_id"),
        "service_id" : "",
        "service_name" : "",
        "date_of_request" : "",
        "date_of_completion" : "",
        "price" : "",
        "time_required" : "",
        "problem_description" : ""
      }
    },
    // Methods related to add service request and fetch services
    async fetch_services(){
      try {
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
          this.loading_services = false;
        }
      }
      catch(error){
        console.log(error);
      }
    },

    // Method related to professional accept, reject service request
    async fetch_professional_service_request(){
      try {
        const response = await fetch(`http://localhost:5000/api/professional_request/${this.user_id}`,{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.service_requests = responseData;
          this.load_service_request = false;
        }
        else{
          this.failedMessage = responseData.message;         
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async accept_request(service_request){
      try {
        const response = await fetch(`http://localhost:5000/api/accept_request/${this.user_id}/${service_request.service_request_id}`,{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.fetch_professional_service_request();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async reject_request(service_request){
      try {
        const response = await fetch(`http://localhost:5000/api/reject_request/${this.user_id}/${service_request.service_request_id}`,{
          method : "GET",
          headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : localStorage.getItem("auth_token")
          }
        });

        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.fetch_professional_service_request();
        }
        else{
          this.failedMessage = responseData.message;         
        }
      }
      catch(error){
        console.log(error);
      }
    },

    toggleAddServiceRequest(service){
      this.showAddServiceRequestForm = !this.showAddServiceRequestForm;
      const currentDate = new Date();
      this.service.service_id = service.service_id;
      this.service.service_name = service.service_name;
      this.service.price = service.price;
      this.service.time_required = service.time_required;
      this.service.date_of_request = currentDate.toISOString().split('T')[0];
    },

    async submitServiceRequestForm(){
      try{
        const response = await fetch('http://localhost:5000/customer_api/create_service_request',{
          method : "POST",
          headers : {
            'Content-Type' : 'application/json',
            'Authentication-Token' : localStorage.getItem("auth_token")
          },
          body : JSON.stringify(this.service)
        });
        const responseData = await response.json();
        if(response.ok){
          this.successMessage = responseData.message;
          this.failedMessage = "";
          this.showAddServiceRequestForm = false;
          this.empty_service();
        }
        else{
          this.failedMessage = responseData.message;
          this.successMessage = "";
          this.showAddServiceRequestForm = false;
          this.empty_service();
        }
      }
      catch(error){
        console.log(error);
      }
    },

    closeModal(event){
      if(event.target === event.currentTarget){
        this.showAddServiceRequestForm = false;
      }
    }
  },
}