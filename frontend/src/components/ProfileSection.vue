<template>
  <div>
    <section v-if="isProfileComplete || isEditingProfile" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>{{ isEditingProfile ? "Edit Profile" : "User Details" }}</h2>
          <form @submit.prevent="validateUserDetails">
            <div>
              <label for="email">Email</label>
              <input type="email" id="email" v-model="user_credential.email" disabled>
            </div>

            <div>
              <label for="username">Username</label>
              <input type="text" id="username" v-model="user_credential.user_name" disabled>
            </div>

            <div>
              <label for="name">Name</label>
              <input type="text" id="name" v-model="user_detail.name" required @blur="validateName()"> 
              <p v-if="error_message.NameError" class="error">
                {{ error_message.NameError }}
              </p>
            </div>
            
            <div>
              <label for="contact_number">Contact Number</label>
              <input type="text" id="contact_number" v-model="user_detail.contact_number" required @blur="validatePhoneNumber()">
              <p v-if="error_message.ContactNumberError" class="error">
                {{ error_message.ContactNumberError }}
              </p>
            </div>

            <div>
              <label for="address">Address</label>
              <textarea id="address" rows="3" cols="10" v-model="user_detail.address" required @blur="validateAddress()"></textarea>
              <p v-if="error_message.AddressError" class="error">
                {{ error_message.AddressError }}
              </p>
            </div>

            <div>
              <label for="state">State</label>
              <select v-model="selectedState" @change="fetch_city" required>
                <option value="" selected disabled>Select State</option>
                <option v-for="(state,index) in states" :key="index" :value="state">{{ state }}</option>
              </select>
              <p v-if="error_message.StateError" class="error">
                {{ error_message.StateError }}
              </p>
            </div>

            <div>
              <label for="city">City</label>
              <select v-model="selectedCity" required>
                <option value="" selected disabled>Select City</option>
                <option v-for="(city, index) in cities" :key="index" :value="city">{{ city }}</option>
              </select>
              <p v-if="error_message.CityError" class="error">
                {{ error_message.CityError }}
              </p>
            </div>

            <div>
              <label for="pin_code">Pin Code</label>
              <input type="text" id="pin_code" v-model="user_detail.pin_code" required @blur="validatePinCode()">
              <p v-if="error_message.PinCodeError" class="error">
                {{ error_message.PinCodeError }}
              </p>
            </div>

            <div v-if="user_credential.role === 'Professional'">
              <label for="service_type">Service Type</label>
              <select v-if="isProfileComplete" v-model="selectedService" required>
                <option value="" selected disabled>
                  Select Service
                </option>
                <option v-for="(service_name,index) in services_name" :key="index" :value="service_name">
                  {{ service_name }}
                </option>
              </select>
              <input type="text" v-if="!isProfileComplete" v-model="user_detail.service_type" disabled>
              <p v-if="error_message.ServiceTypeError" class="error">
                {{ error_message.ServiceTypeError }}
              </p>
            </div>

            <div v-if="user_credential.role==='Professional'">
              <label for="experience">Experience</label>
              <input type="number" id="experience" v-model="user_detail.experience" min="0" max="50" required @blur="validateExperience()" />
              <p v-if="error_message.ExperienceError" class="error">
                {{ error_message.ExperienceError }}
              </p>
            </div>

            <div>
              <div v-if="user_detail.image_url">
                <p>Previously uploaded image</p>
                <img :src="'http://localhost:5000' + user_detail.image_url + '?t=' + new Date().getTime()" alt="Uploaded Image" style="max-width: 50px;border-radius: 50%;">
              </div>
              <label for="image_file">Image</label>
              <input type="file" id="image_file" ref="image_file" :required="isProfileComplete && !isEditingProfile" @blur="validateImage()">
              <p v-if="error_message.ImageError" class="error">
                {{ error_message.ImageError }}
              </p>
            </div>


            <div v-if="user_credential.role==='Professional'">
              <div v-if="user_detail.resume_url">
                <p>Previously uploaded resume</p>
                <a :href="'http://localhost:5000' + user_detail.resume_url + '?t=' + new Date().getTime()" target="_blank">Uploaded Resume</a>
              </div>
              <label for="resume_file">Resume</label>
              <input type="file" id="resume_file" ref="resume_file" :required="isProfileComplete && !isEditingProfile" @blur="validateResume()">
              <p v-if="error_message.ResumeError" class="error">
                {{ error_message.ResumeError }}
              </p>
            </div>
            
            <div>
              <button type="submit">Submit</button>
            </div>
          </form>
        </div>
      </section>
  </div>
</template>

<script>
  import ProfileScript from '../scripts/profile.js'

  export default{
    name : "ProfileSection",

    props :{
      isEditingProfile : {
        type : Boolean,
        required : true
      },
      savedCredential : {
        type : Object,
        required : true
      },
    },
    
    data(){
      return ProfileScript.data()
    },

    mounted(){
      if(this.savedCredential){
        this.user_credential = JSON.parse(JSON.stringify(this.savedCredential));
      }
      this.check_profile_complete();
      this.fetch_state();
      this.fetch_services_name();
    },

    methods : ProfileScript.methods,
}
</script>