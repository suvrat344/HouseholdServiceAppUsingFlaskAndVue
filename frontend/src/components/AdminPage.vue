<template>
  <div>
    <header id="side-nav">
      <nav>
        <ul>
          <li class="dropdown">
            Customer
            <ul class="dropdown-content">
              <li @click="showSection('getCustomer')">
                Get Customers
              </li>
              <li @click="showSection('getCustomer')">
                Search Customer
              </li>
              <li @click="showSection('blockCustomer')">
                Block Customer
              </li>
            </ul>
          </li>
        </ul>

        <ul>
          <li class="dropdown">
            Professional
            <ul class="dropdown-content">
              <li @click="showSection('getProfessional')">
                Get Professionals
              </li>
              <li>
                Search Professional
              </li>
              <li @click="showSection('blockProfessional')">
                Block Professional
              </li>
            </ul>
          </li>
        </ul>

        <ul>
          <li class="dropdown">
            Service Offered
            <ul class="dropdown-content">
              <li @click="showSection('getService')">
                Get Service
              </li>
              <li @click="showSection('addService')">
                Add Service
              </li>
              <li @click="showSection('updateService')">
                Update Service
              </li>
              <li @click="showSection('deleteService')">
                Delete Service
              </li>
            </ul>
          </li>
        </ul>

        <ul>
          <li class="dropdown">
            Service Request
            <ul class="dropdown-content">
                <li @click="showSection('getServiceRequest')">
                  Get Service Request
                </li>
                <li @click="showSection('editServiceRequest')">
                  Edit Service Request
                </li>
                <li @click="showSection('closeServiceRequest')">
                  Close Service Request
                </li>
              </ul>
            </li>
        </ul>

      </nav>
    </header>

    <main>
      <p v-if="successMessage" class="success">
          Message : {{ successMessage }}
      </p>

      <section id="professional-request">
        <h2>Profile Verification</h2>
          <p v-if="loading_professional_for_verification" class="loading">
            Loading professionals...
          </p>
          <p v-if="!loading_professional_for_verification && profiles.length == 0">
            Currently, no professionals profile available for verification. Wait for professional to register on the app.
          </p>
        <div class="profile-verified">
          <div v-for="(professional,index) in profiles" :key="index" class="card">
            <p>Name : {{ professional.name }}</p>
            <p>Service Type : {{ professional.service_type }}</p>
            <p>Experience : {{ professional.experience }}</p>
            <p>Contact Number : {{ professional.contact_number }}</p>
            <p>Address : {{ professional.address }}</p>
            <p>City : {{ professional.city }}</p>
            <p>State : {{ professional.state }}</p>
            <p>Pin Code : {{ professional.pin_code }}</p>
            <p>
              <a :href="'http://localhost:5000' + professional.resume_url" target="_blank">Download Resume</a>
            </p>
            <button @click="verified_profile(professional.user_id)">Verified</button>
          </div>
        </div>
      </section>

      <section v-if="(current_section === 'getCustomer' || current_section === 'blockCustomer') && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Customer Details</h2>
          <p v-if="loading_customer" class="loading">
            Loading customers...
          </p>
          <p v-if="!loading_customer && customers.length == 0">
            Currently, no customers have registered on the app. Wait for the moment. Please contact support if you need assistance.
          </p>
          <table v-if="!loading_customer && customers.length > 0">
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Contact Number</th>
                <th>Address</th>
                <th>City</th>
                <th>State</th>
                <th>Pin Code</th>
                <th v-if="current_section === 'blockCustomer'">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(customer,index) in customers" :key="index">
                <td>{{ customer.name }}</td>
                <td>{{ customer.contact_number }}</td>
                <td>{{ customer.address }}</td>
                <td>{{ customer.city }}</td>
                <td>{{ customer.state }}</td>
                <td>{{ customer.pin_code }}</td>
                <td v-if="current_section === 'blockCustomer'">
                  <button @click="BlockCustomer(customer.user_id)">
                    Block
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="(current_section === 'getProfessional' || current_section === 'blockProfessional') && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Professional Details</h2>
          <p v-if="loading_customer" class="loading">
            Loading professionals...
          </p>
          <p v-if="!loading_professional && professionals.length == 0">
            Currently, no professionals have registered on the app. Wait for the moment. Please contact support if you need assistance.
          </p>
          <table v-if="!loading_professional && professionals.length > 0">
            <thead>
              <tr>
                <th>Professional Name</th>
                <th>Service Type</th>
                <th>Experience</th>
                <th>Contact Number</th>
                <th>Address</th>
                <th>City</th>
                <th>State</th>
                <th>Pin Code</th>
                <th>Resume</th>
                <th v-if="current_section === 'blockProfessional'">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(professional,index) in professionals" :key="index">
                <td>{{ professional.name }}</td>
                <td>{{ professional.service_type }}</td>
                <td>{{ professional.experience }}</td>
                <td>{{ professional.contact_number }}</td>
                <td>{{ professional.address }}</td>
                <td>{{ professional.city }}</td>
                <td>{{ professional.state }}</td>
                <td>{{ professional.pin_code }}</td>
                <td><a :href="'http://localhost:5000/' + professional.resume_url" target="_blank">Resume</a></td>
                <td v-if="current_section === 'blockProfessional'">
                  <button @click="BlockProfessional(professional.user_id)">
                    Block
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      
      <section v-if="current_section === 'getService' && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Services Offered</h2>
          <p v-if="loading_service" class="loading">
            Loading service requests...
          </p>
          <p v-if="!loading_service && services.length == 0">
            No services available at the moment. Please add a service. Admin, you can add new services by clicking the 'Add Service' button. If you need assistance, please contact the support team.
          </p>
          <table v-if="!loading_service && services.length > 0">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Price</th>
                <th>Time Required</th>
                <th>Description</th>
                <th>Image Icon</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service,index) in services" :key="index">
                <td>{{ service.service_name }}</td>
                <td>{{ service.price }}</td>
                <td>{{ service.time_required }}</td>
                <td>{{ service.description }}</td>
                <td>{{ service.image_file }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="(current_section === 'addService' || current_section === 'UpdateForm') && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>{{ current_section==='addService' ? "Add New Service" : "Update Service" }}</h2>
          <form @submit.prevent="current_section==='addService' ? AddService() : UpdateService()">
            <div>
              <label for="service_name">Service Name</label>
              <input type="text" id="service_name" v-model="service.service_name" required>
            </div>
            <div>
              <label for="price">Price</label>
              <input type="text" id="price" v-model="service.price" required>
            </div>
            <div>
              <label for="time_required">Time Required</label>
              <input type="text" id="time_required" v-model="service.time_required" required>
            </div>
            <div>
              <label for="image_file">Image File</label>
              <input type="text" id="image_file" v-model="service.image_file" required>
            </div>
            <div>
              <label for="description">Description</label>
              <textarea id="description" rows="5" cols="10" v-model="service.description" required></textarea>
            </div>
            <div>
              <button type="submit">Submit</button>
            </div>
          </form> 
        </div>
      </section>

      <section v-if="current_section === 'updateService' && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Services Offered</h2>
          <p v-if="loading_service" class="loading">
            Loading service requests...
          </p>
          <p v-if="!services">
            No services available at the moment. Please add a service. Admin, you can add new services by clicking the 'Add Service' button. If you need assistance, please contact the support team.
          </p>
          <table v-if="!loading_service">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Price</th>
                <th>Time Required</th>
                <th>Description</th>
                <th>Image Icon</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service,index) in services" :key="index">
                <td>{{ service.service_name }}</td>
                <td>{{ service.price }}</td>
                <td>{{ service.time_required }}</td>
                <td>{{ service.description }}</td>
                <td>{{ service.image_file }}</td>
                <td>
                  <button @click="toggleUpdateServiceForm(service)">Update</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="current_section === 'deleteService' && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Services Offered</h2>
          <p v-if="loading_service" class="loading">
            Loading service requests...
          </p>
          <p v-if="!services">
            No services available at the moment. Please add a service. Admin, you can add new services by clicking the 'Add Service' button. If you need assistance, please contact the support team.
          </p>
          <table v-if="!loading_service">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Price</th>
                <th>Time Required</th>
                <th>Description</th>
                <th>Image Icon</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service,index) in services" :key="index">
                <td>{{ service.service_name }}</td>
                <td>{{ service.price }}</td>
                <td>{{ service.time_required }}</td>
                <td>{{ service.description }}</td>
                <td>{{ service.image_file }}</td>
                <td>
                  <button @click="DeleteService(service)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="(current_section === 'getServiceRequest' || current_section === 'editServiceRequest' || 'closeServiceRequest') && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Service Requests</h2>
          <p v-if="loading_service_request" class="loading">
            Loading service requests...
          </p>
          <p v-if="!loading_service_request && service_requests.length == 0">
            No service requests available at the moment. When customer add service request then it show on panel. If you need assistance, please contact the support team.
          </p>
          <table v-if="!loading_service_request">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Customer Name</th>
                <th>City</th>
                <th>State</th>
                <th>Date of request</th>
                <th>Date of completion</th>
                <th>Professional Name</th>
                <th>Rating</th>
                <th>Review</th>
                <th>Status</th>
                <th v-if="current_section==='editServiceRequest'">Action</th>
                <th v-if="service_request.service_status === 'Accepted' && current_section==='closeServiceRequest'">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service_request,index) in service_requests" :key="index">
                <td>{{ service_request.service_name }}</td>
                <td>{{ service_request.customer_name }}</td>
                <td>{{ service_request.city }}</td>
                <td>{{ service_request.state }}</td>
                <td>{{ formatDate(service_request.date_of_request) }}</td>
                <td>{{ formatDate(service_request.date_of_completion) }}</td>
                <td>{{ service_request.professional_name }}</td>
                <td>{{ service_request.rating }}</td>
                <td>{{ service_request.review }}</td>
                <td>{{ service_request.service_status }}</td>
                <td v-if="current_section==='editServiceRequest'">
                  <button @click="toggleEditServiceRequestForm(service_request)">Edit</button>
                </td>
                <td v-if="service_request.service_status === 'Accepted' && current_section==='closeServiceRequest'">
                  <button @click="CloseServiceRequestForm(service_request_id)">Close</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-if="current_section === 'EditServiceRequest' && role === 'Admin'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Edit Service Request</h2>
          <form @submit.prevent="EditServiceRequest(service_request)">
            <div>
              <label for="service_name">Service Name</label>
              <input type="text" id="service_name" v-model="service_request.service_name" disabled>
            </div>
            <div>
              <label for="customer_name">Customer Name</label>
              <input type="text" id="customer_name" v-model="service_request.customer_name" disabled>
            </div>
            <div>
              <label for="city">City</label>
              <input type="text" id="city" v-model="service_request.city" disabled>
            </div>
            <div>
              <label for="state">State</label>
              <input type="text" id="state" v-model="service_request.state" disabled>
            </div>
            <div>
              <label for="date_of_request">Date of Request</label>
              <input type="text" id="date_of_request" v-model="service_request.date_of_request" disabled>
            </div>
            <div>
              <label for="date_of_completion">Date of Completion</label>
              <input type="text" id="date_of_completion" v-model="service_request.date_of_completion" required>
            </div>
            <div>
              <label for="professional_name">Professional Name</label>
              <input type="text" id="professional_name" v-model="service_request.professional_name" disabled>
            </div>
            <div>
              <label for="rating">Rating</label>
              <input type="number" id="rating" v-model="service_request.rating" min="1" max="5">
            </div>
            <div>
              <label for="review">Review</label>
              <input type="text" id="review" v-model="service_request.review">
            </div>
            <div>
              <label for="status">Request Status</label>
              <input type="text" id="status" v-model="service_request.service_status">
            </div>
            <div>
              <button type="submit">Submit</button>
            </div>
          </form> 
        </div>
      </section>
      
    </main>
  </div>
</template>


<script>
  import AdminScript from '../scripts/admin.js'

  export default{
    name : "AdminPage",
    components : {
    },
    data(){
      return AdminScript.data();
    },

    mounted(){
      this.profile_verification();
      this.GetCustomers();
      this.GetServices();
      this.GetProfessionals();
      this.GetServiceRequest();
    },

    methods : AdminScript.methods
  }
</script>

<style src="../assets/styles/admin.css" scoped></style>