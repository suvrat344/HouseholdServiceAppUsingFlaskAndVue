<template>
  <div>
    <main>
      <!---------------------------------- hero-section starts ----------------------------------------------->
      <section id="hero">
        <div class="image-container">
          <img src="../assets/images/img1.jpg" alt="image">
          <div class="overlay-text">
            <p id="main-heading">Need some professional household help?</p>
            <p>
              Contact our Customer Service representative to make an appointment and to answer all your <br>questions!
            </p>
            <router-link to="/contact">
              <button>make an appointment</button>
            </router-link>
          </div>
        </div>
      </section>
      <!---------------------------------- hero-section ends ------------------------------------------------->

      
      <!----------------------------------- about-section starts --------------------------------------------->
      <section id="about-section">
        <div class="about">
          <div class="first-col">
            <span>We Are JohnnyGo</span>
            <p>
              We are a team of professional and skilled experts in all domestic spheres. We offer a wide range of services and at the same time we are always glad to help you with any unconventional household needs:
            </p>
            <ul>
              <li v-for="(service,index) in services" :key="index">{{ service }}</li>
            </ul>
          </div>
          <div class="second-col">
            <img src="../assets/images/img2.jpg" alt="image">
          </div>
        </div>
      </section>
      <!---------------------------------- about-section ends ----------------------------------------------------->


      <!---------------------------------- choose-section starts --------------------------------------------------->
      <section id="choose-section">
        <span>Why Choose Us</span>
        <div class="choose">
          <div class="card" v-for="(content,index) in choose" :key="index">
            <i :class="[content.icon, 'icon']" aria-hidden="true"></i>
            <h4>{{ content.title }}</h4>
            <p>
             {{ content.description }}
            </p>
          </div>
        </div>
      </section>
      <!---------------------------------- choose-section ends --------------------------------------------------->


      <!---------------------------------- mission-section start ------------------------------------------------->
      <section id="mission-section">
        <div class="mission">
          <div class="first-col">
            <span>Our Mission</span>
            <p>
              We work to ensure people's comfort at their home, and to provide the best and the fastest help at fair prices. We stand for quality, safety and credibility, so you could be sure about our work.
            </p>
            <p>
              Initially we started as a company specializing in household maintenance. During our successful work we expanded our list of services. Now we are proud that we can help people with welding, moving, dry cleaning, landscaping and even pest control.
            </p>
            <p>
              Every member of our team is indeed good at his job and the company guarantees the quality of work and materials we use.
            </p>
            <p>
              We value our every worker and every client, and we strive to do our best to provide you with the best services ever.
            </p>
            <button>Our Projects</button>
          </div>
          <div class="second-col">
            <span>Popular Questions</span>
            <p @click="getAnswer(0)" v-html="getArrow(0) + ' Why does a renovation project cost so much?'">
            </p>
            <p class="answer" v-if="activeQuestion === 0">
              Every renovation project requires a lot of expenses. They include such bulks as materials and labor. Materials, in turns, include tile, mortar, grout, rough plumbing materials, paint and many other. If you need to  make a calculation of your future renovation project, please give us a call or email us, and our manager will help you with this issue.
            </p>
            <hr>

            <p @click="getAnswer(1)" v-html="getArrow(1) + ' What is the timeline for the project?'">
            </p>
            <p class="answer" v-if="activeQuestion === 1">
              Depending on dimensions of the space and amount of work, it takes from a week to a 2-3 month to complete the renovation project.
            </p>
            <hr>

            <p @click="getAnswer(2)" v-html="getArrow(2) + ' What is the total budget for construction?'">
            </p>
            <p class="answer" v-if="activeQuestion === 2">
              The total budget may vary as sizes of rooms are very different. For example, approximate budget for a basic bathroom renovation is from $3500 to $5000. If you need detailed calculation of materials and work, please contact our Customer Service Department.
            </p>
            <hr>

            <p @click="getAnswer(3)" v-html="getArrow(3) + ' How is renovation project initiated?'">
            </p>
            <p class="answer" v-if="activeQuestion === 3">
              Renovation project can be initiated by the clients. If you need to reconstruct your old house, a room or a basement, you need to appeal to us, approve the project and budget and we’ll start working.
            </p>
            <hr>
          </div>
        </div>
      </section>
      <!---------------------------------- mission-section ends -------------------------------------------------->


      <!---------------------------------- info-section starts -------------------------------------------------->
      <section id="info-section">
        <div class="info">
          <div class="info-item" v-for="(content, index) in info" :key="index">
            <i :class="[content.icon ,'icon']" aria-hidden="true"></i>
            <div class="contact-info">
              <span>{{ content.title }}</span>
              <span>{{ content.value }}</span>
            </div>
          </div>
        </div>
      </section>
      <!---------------------------------- info-section ends -------------------------------------------------->
    </main>
  </div>
</template>


<script>
  import AboutScript from '../scripts/about.js'

  export default{
    name : "AboutPage",
    components : {
    },
    data(){
      return AboutScript.data();
    },
    methods : AboutScript.methods
  }
</script>

<style src="../assets/styles/about.css" scoped></style>