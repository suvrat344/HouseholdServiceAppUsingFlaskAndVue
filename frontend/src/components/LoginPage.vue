<template>
  <div class="login-container">
    <div class="col1">
      <form @submit.prevent="isLogin ? login() : handleRegisterUser()">
        <div class="form-group">
          <h2>{{ isLogin ? "Welcome Back" : "Create Account" }}</h2>
          <p>Welcome back! Please enter your details.</p>
        </div>

        <div class="form-group">
          <p v-if="errorMessage.NotFoundError" class="failure">
            {{ errorMessage.NotFoundError }}
          </p>

          <p v-if="errorMessage.UserNameExistError" class="failure">
          {{ errorMessage.UserNameExistError }}
          </p>

          <p v-if="errorMessage.UserExistError" class="failure">
            {{ errorMessage.UserExistError }}
          </p>

          <p v-if="errorMessage.PasswordError" class="failure">
            {{ errorMessage.PasswordError }}
          </p>

          <p v-if="errorMessage.AccountError" class="failure">
            {{ errorMessage.AccountError }}
          </p>

          <p v-if="errorMessage.VerificationError" class="failure">
            {{ errorMessage.VerificationError }}
          </p>
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" v-model="user_credential.email" id="email" placeholder="Enter your email" required @blur="isLogin?'':validateEmail()" />

          <p v-if="errorMessage.EmailError" class="error">
            {{ errorMessage.EmailError }}
          </p>
        </div>

        <div class="form-group" v-if="!isLogin">
          <label for="username">Username</label>
          <input type="text" v-model="user_credential.user_name" id="username" placeholder="Enter username" required @blur="validateUsername()" />
          <!-- Username Validation Error  required -->
          <p v-if="errorMessage.UserNameError" class="error">
            {{ errorMessage.UserNameError }}
          </p>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" v-model="user_credential.password" id="password"  placeholder="*************" required @blur="isLogin ? '' : validatePassword()" />
        </div>

        <div class="form-group" v-if="!isLogin">
          <select id="role" v-model="selectRole" required>
            <option value="" disabled>Select Role</option>
            <option value="Customer">Customer</option>
            <option value="Professional">Professional</option>
          </select>
          <p v-if="errorMessage.RoleError" class="error">
            {{ errorMessage.RoleError }}
          </p>
        </div>

        <div class="form-group check">
          <input type="checkbox" >{{ isLogin ? "Remember Me" : "Agree with terms and conditions" }}
          <p v-if="isLogin">Forgot Password</p>
        </div>

        <div class="form-group">
          <button type="submit">{{ isLogin ? "sign in" : "sign up" }}</button>
        </div>

        <p>
          {{ isLogin ? "Don't have an account?" : "Already have an account?" }} 
          <span @click="isLogin ? toggleSignUpForm() : toggleSignInForm()">
            {{ isLogin ? "Sign up for free!" : "Login" }}
          </span>
        </p>
      </form>
    </div>

    <div class="col2">
      <img src="../assets/images/login.jpg">
    </div>
  </div>
</template>

<script>
  import LoginScript from '../scripts/login.js'
  
  export default {
    data() {
      return LoginScript.data()
    },
    methods: LoginScript.methods,
  };
</script>

<style src="../assets/styles/login.css" scoped></style>