<template>
  <div>
    <main>
      <section id="card-section">
        <div class="choice-section" v-if="service_requests.length > 0 && !loading">
          <select v-model="selectedChoice" required>
            <option value="" selected>All Service Request</option>
            <option v-if="role==='Customer'" value="Pending">Pending Requests</option>
            <option value="Accepted">Accepted Requests</option>
            <option v-if="role==='Professional'" value="Rejected">Rejected Requests</option>
            <option value="Cancelled">Cancelled Requests</option>
            <option value="Closed">Closed Requests</option>
          </select>
        </div>
        
        <p v-if="loading_customer_transaction" class="loading">Loading service requests...</p>

        <p v-if="!loading_customer_transaction && !service_requests.length" class="response">
          Dear {{ role }}, we noticed that you haven't made any service requests recently. If there's anything we can assist you with or any concerns you may have, feel free to reach out. We're here to help and ensure your satisfaction!
        </p>

        <p v-if="!loading_customer_transaction && filteredServiceRequest.length == 0" class="response">
            Oops! No service requests were found for the selected status.Please try adjusting the filter or select a different status to view available requests.
        </p>

        <div class="card-container">
          <div class="card" v-for="(service_request, index) in filteredServiceRequest" :key="index">
              <p> Service Name : {{ service_request.service_name }}</p>
              <p>Date of Request : {{ formatDate(service_request.date_of_request) }}</p>
              <p>Date of Completion : {{ formatDate(service_request.date_of_completion) }}</p>
              <p>Status : {{ service_request.service_status }}</p>
              <p v-if="service_request.professional_name && role==='Customer'">Professional Name : {{ service_request.professional_name }}</p>
              <p>Professional Name : {{ service_request.customer_name }}</p>
              <p v-if="service_request.contact_number">Contact Number : {{ service_request.contact_number }}</p>
              <p v-if="service_request.city">City : {{ service_request.city }}</p>
              <p v-if="service_request.state">State : {{ service_request.state }}</p>
              <p v-if="service_request.address">Address : {{ service_request.address }}</p>
            <div class="action" v-if="service_request.service_status !== 'Cancelled' && service_request.service_status !== 'Closed'">
              <button v-if="role==='Customer'" @click="toggleUpdateServiceRequest(service_request)">
                update
              </button>
              <button v-if="role==='Customer'" @click="customer_cancel_request(service_request)">
                cancel
              </button>
              <button v-if="service_request.service_status != 'Pending'" 
                      @click="role === 'Customer' ? toggleReviewForm(service_request.service_request_id) : ''">
                Closed
              </button>
            </div>
          </div>
        </div>
      </section>

      <section v-if="showUpdateForm && role === 'Customer'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Update Service Request</h2>
          <form @submit.prevent="updateServiceRequest(service.service_request_id)">
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
              {{ service.date_of_completion }}
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

      <section v-if="showReviewForm && role === 'Customer'" class="modal-overlay" @click="closeModal">
        <div class="modal-container">
          <h2>Review Form</h2>
          <form @submit.prevent="validateReviewForm()">
            <div>
              <label for="professional_rating">Professional Rating</label>
              <input type="number" id="professional_rating" v-model="rating" required @blur="validateRating()">
              <p v-if="error_message.RatingError" class="error">
                {{ error_message.RatingError }}
              </p>
            </div>
            <div>
              <label for="remarks">Remarks</label>
              <textarea id="remarks" rows="5" cols="10" v-model="remarks" required @blur="validateRemarks()"></textarea>
              <p v-if="error_message.RemarksError" class="error">
                {{ error_message.RemarksError }}
              </p>
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
  import TransactionScript from '../scripts/transaction.js'
  
  export default{
    name : "TransactionPage",
    components :{
    },
    data(){
      return TransactionScript.data()
    },
    mounted(){
      {
        this.role === "Customer" ? this.fetch_customer_service_request() : this.fetch_professional_service_request();
      }
    },
    computed : {
      filteredServiceRequest(){
        if(!this.selectedChoice){
          return this.service_requests;
        }
        return this.service_requests.filter((service_request) => service_request.service_status === this.selectedChoice);
      }
    },
    methods : TransactionScript.methods,
  }
</script>

<style src="../assets/styles/transaction.css"></style>