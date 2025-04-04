<template>
  <div>
    <main>

      <!--------------------------------- hero section starts  --------------------------------------------->
      <section id="hero-section">
        <div class="img-container">
          <img src="../assets/images/home.jpg" alt="image">

          <div class="overlay-text">
            <span>What Can Our Home Improvement Professionals Do For You?</span>
            <span>Call Us: (719) 445-2808</span>
            <p>Working time: Monday to Thursday: 9:00 A.M. - 6:00 P.M.</p>
          </div>

          <div class="grid-col">
            <div v-for="(content, index) in info" :key="index">
              <i :class="[content.icon, 'icon']"></i>
              <p>{{ content.heading }}</p>
              <p>{{ content.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!--------------------------------- hero section ends --------------------------------------------->


      <!-------------------------------- service-section starts ----------------------------------------->
      <section id="service-section" v-if="role === 'Customer'">
        <span>Our Professional Maid Services</span>
        <p v-show="successMessage" class="success">
          {{ successMessage }}
        </p>
        <p v-show="failedMessage" class="failure">
          {{ failedMessage }}
        </p>
        <p v-if="loading_services" class="loading">Loading Services...</p>
        <div class="service-container" v-if="services">
          <div class="card" v-for="(service, index) in services" :key="index">
            <i :class="[service.image_file, 'icon']"></i>
            <p>{{ service.service_name }}</p>
            <p>{{ service.description }}</p>
            <p>Price : {{ service.price }}</p>
            <p>TIme : {{ service.time_required }}</p>
            <button @click="toggleAddServiceRequest(service)">
               Add
            </button>
          </div>
        </div>
        <div v-else>
          <p>
            No services are available at the moment. We're currently not offering any services due to unforeseen circumstances. Our team is working hard to resume service offerings as soon as possible. Please check back later for updates on our available services. In the meantime, if you need assistance or have any inquiries, feel free to reach out to our support team. We apologize for any inconvenience this may have caused and appreciate your patience and understanding. Thank you for your support, and we look forward to serving you again soon!
          </p>
        </div>
      </section>

      <section id="service-section" v-else>
        <span>Service Request</span>
        <p v-show="successMessage" class="success">
          {{ successMessage }}
        </p>
        <p v-show="failedMessage" class="failure">
          {{ failedMessage }}
        </p>
        <p v-if="load_service_request" class="loading">Loading Service Requests...</p>
        <div class="service-container" v-if="!load_service_request && service_requests.length > 0">
          <div class="card card1" v-for="(service_request, index) in service_requests" :key="index">
            <i :class="[service_request.icon, 'icon']"></i>
            <p>{{ service_request.service_name }}</p>
            <p>Contact Number : {{ service_request.contact_number }}</p>
            <p>Address : {{ service_request.address }}</p>
            <p>City : {{ service_request.city }}</p>
            <p>State : {{ service_request.state }}</p>
            <p>Date of Request : {{ service_request.date_of_request }}</p>
            <p>Date of Completion : {{ service_request.date_of_completion }}</p>
            <div class="professional_choice">
              <button @click="accept_request(service_request)">Accept</button>
              <button @click="reject_request(service_request)">Reject</button>
            </div>
          </div>
        </div>
        <p class="response" v-if="!load_service_request && service_requests.length == 0">
          No service requests are available at the moment. Our team is working diligently to process and fulfill new service requests, but currently, we have no active requests in the system. Please check back later or contact our support team if you have urgent needs or inquiries. We are always ready to assist you, and we greatly appreciate your patience and understanding during this time.
        </p>
      </section>

      <section v-if="showAddServiceRequestForm && role === 'Customer'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Add New Service Request</h2>
          <form @submit.prevent="submitServiceRequestForm">
            <div>
              <label for="service_name">Service Name</label>
              <input type="text" id="service_name" v-model="service.service_name" disabled>
            </div>
            <div>
              <label for="date_of_request">Date of Request</label>
              <input type="text" id="date_of_request" v-model="service.date_of_request" disabled>
            </div>
            <div>
              <label for="date_of_completion">Date of Completion</label>
              <input type="date" id="date_of_completion" v-model="service.date_of_completion" required>
            </div>
            <div>
              <label for="price">Price</label>
              <input type="text" id="price" v-model="service.price" disabled>
            </div>
            <div>
              <label for="time_required">Time Required</label>
              <input type="text" id="time_required" v-model="service.time_required" disabled>
            </div>
            <div>
              <label for="problem_description">Problem Description</label>
              <textarea id="problem_description" rows="5" cols="10" v-model="service.problem_description" required></textarea>
            </div>
            <div>
              <button type="submit">Submit</button>
            </div>
          </form>
        </div>
      </section>
      <!-------------------------------- service-section ends ------------------------------------------->


      <!-------------------------------- more-service-section starts ------------------------------------>
      <section id="more-services">
        <div class="more-service-container">
          <div class="col1">
            <span>More Services</span>
            <p>What Can Our Home Improvement Professionals Do For You?</p>
          </div>

          <div class="col2">
            <ul>
              <li v-for="(content, index) in more_services" :key="index">{{ content }}</li>
            </ul>
          </div>
        </div>
      </section>
      <!-------------------------------- more-service-section ends -------------------------------------->


      <!-------------------------------- help-section starts -------------------------------------------->
      <section id="help-section">
        <div class="help-container">
          <div class="col1">
            <img src="../assets/images/img3.jpg" alt=image>
          </div>
          <div class="col2">
            <p>Our experts will solve them in no time.</p>
            <p>Have Any Housing Problems?</p>
            <router-link to="/contact">
              <button>Make an Appointment</button>
            </router-link>
          </div>
        </div>
      </section>
      <!-------------------------------- help-section ends ----------------------------------------------->


      <!-------------------------------- choose-section starts ----------------------------------------------->
      <section id="choose-why">
        <span>Why Choose JohnnyGo for Your Home Repair Needs?</span>
        <div class="choose-why-container">
          <div class="col" v-for="(content, index) in choose" :key="index">
            <div class="column1">
              <i :class="[content.icon, 'icon']"></i>
            </div>
            <div class="column2">
              <p>{{ content.title }}</p>
              <p>{{ content.description }}</p>
            </div>
          </div>
        </div>
      </section>
      <!-------------------------------- choose-section ends ----------------------------------------------->
    </main>
  </div>
</template>


<script>
  import HomeScript from '../scripts/home.js'

  export default{
    name : "HomePage",
    components : {
    },

    data(){
      return HomeScript.data()
    },

    mounted(){
      this.role === "Customer" ? this.fetch_services() : this.fetch_professional_service_request();
    },

    methods : HomeScript.methods,
  }
</script>

<style src="../assets/styles/home.css" scoped></style>