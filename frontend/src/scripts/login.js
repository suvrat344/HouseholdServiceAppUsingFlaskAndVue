export default {
  data() {
    return {
      user_credential : {
        "email" : "",
        "password" : "",
        "user_name" : "",
        "role" : ""
      },
      errorMessage : {},
      SuccessMessage : "",
      isLogin : true,
      selectRole: "",
    };
  },
  methods: {
    validateEmail(){
      const regex = /^(?!.*\.\.)[a-zA-Z\d._%+-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$/;
      const result = regex.test(this.user_credential.email);
      if(result){
        this.$set(this.errorMessage, "EmailError", "");
        return true;
      }
      else{
        this.$set(this.errorMessage, "EmailError", "Please enter a valid email address. It must contain an '@' symbol, a period (.) after the '@', and no consecutive dots (e.g., 'test..example@example.com' is invalid).");
        console.log("Email errror");
      }
    },

    validateUsername(){
      const regex = /^[a-zA-Z\d]([a-zA-Z\d-]{1,7}[a-zA-Z0-9])?$/;
      const result = regex.test(this.user_credential.user_name);
      if(result){
        this.$set(this.errorMessage,"UserNameError","");
        return true;
      }
      else{
        this.$set(this.errorMessage,"UserNameError","Username must be between 3 and 9 characters long and can only contain letters, numbers, hyphens. It cannot start or end with a hyphen.");
      }
    },

    validatePassword(){
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d])(?=.*[\W_]).{4,8}/;
      const result = regex.test(this.user_credential.password);
      if(result){
        this.$set(this.errorMessage,"PasswordError","");
        return true;
      }
      else{
        this.$set(this.errorMessage,"PasswordError","Password must be between 4 and 8 characters long, include at least one symbol, one uppercase letter, one lowercase letter, and one number.");
      }
    },

    async handleRegisterUser(){
      if(!this.validateEmail()){
        return
      }
      if(!this.validateUsername()){
        return
      }
      if(!this.validatePassword()){
        return
      }
      else{
        await this.registerUser();
      }
    },

    async login(){
      try{
        const formData = {
          "email" : this.user_credential.email,
          "password" : this.user_credential.password
        };
        const response = await fetch("http://localhost:5000/auth_api/login_user",{
          method : "POST",
          headers : {
            'Content-Type' : "application/json"
          },
          body : JSON.stringify(formData)
        });
        const responseData = await response.json();
        
        if(response.ok){
          if(Object.keys(responseData).includes('auth_token')){
            localStorage.setItem("user_id", responseData["id"]);
            localStorage.setItem("email", responseData["email"]);
            localStorage.setItem("user_name", responseData["username"]);
            localStorage.setItem("role", responseData["role"]);
            localStorage.setItem("auth_token", responseData["auth_token"]);
            localStorage.setItem("state_city", JSON.stringify(responseData["state_city"]));
            if(responseData.role.includes('Admin')){
              this.$router.push('/admin');
            }
            else{
              this.$router.push('/home');
            }
          }
        }
        else{
          if(responseData.PasswordError){
            this.$set(this.errorMessage,"PasswordError",responseData.PasswordError);
          }
          else{
            this.$set(this.errorMessage,"PasswordError","");
          }

          if(responseData.NotFoundError){
            this.$set(this.errorMessage,"NotFoundError",responseData.NotFoundError);
          }
          else{
            this.$set(this.errorMessage,"NotFoundError","");
          }

          if(responseData.AccountError){
            this.$set(this.errorMessage, "AccountError", responseData.AccountError);
          }
          else{
            this.$set(this.errorMessage,"AccountError","");
          }

          if(responseData.VerificationError){
            this.$set(this.errorMessage, "VerificationError", responseData.VerificationError);
          }
          else{
            this.$set(this.errorMessage,"VerificationError","");
          }
        }
      }
      catch(error){
        console.log(error);
      }
    },

    async registerUser(){
      try{
        this.user_credential.role = this.selectRole;
        const response = await fetch("http://localhost:5000/auth_api/register_user",{
          method : "POST",
          headers : {
            'Content-Type' : "application/json"
          },
          body : JSON.stringify(this.user_credential)
        });
        const responseData = await response.json();
        console.log(responseData);
        if(response.ok){
          this.toggleSignInForm();
          this.SuccessMessage = responseData.Success;
        }
        else{
          if(responseData.EmailError){
            this.$set(this.errorMessage, "EmailError", responseData.EmailError);
          }
          else{
            this.$set(this.errorMessage, "EmailError", "");
          }

          if(responseData.PasswordError){
            this.$set(this.errorMessage, "PasswordError", responseData.PasswordError);
          }
          else{
            this.$set(this.errorMessage, "PasswordError", "");
          }

          if(responseData.UserNameError){
            this.$set(this.errorMessage, "UserNameError", responseData.UserNameError);
          }
          else{
            this.$set(this.errorMessage, "UserNameError", "");
          }

          if(responseData.RoleError){
            this.$set(this.errorMessage, "RoleError", responseData.RoleError);
          }
          else{
            this.$set(this.errorMessage, "RoleError", "");
          }

          if(responseData.UserNameExistError){
            this.$set(this.errorMessage, "UserNameExistError", responseData.UserNameExistError);
          }
          else{
            this.$set(this.errorMessage, "UserNameExistError", "");
          }

          if(responseData.UserExistError){
            this.$set(this.errorMessage, "UserExistError", responseData.UserExistError);
          }
          else{
            this.$set(this.errorMessage, "UserExistError", "");
          }
        }
      }
      catch(error){
        console.log(error);
      }
    },

    toggleSignUpForm(){
      this.isLogin = false;
      this.user_credential.email = "";
      this.user_credential.password = "";
      this.errorMessage = {};
    },
    
    toggleSignInForm(){
      this.isLogin = true;
      this.user_credential.user_name = "";
      this.user_credential.email = "";
      this.user_credential.password = "";
      this.errorMessage = {};
    },
  }
};