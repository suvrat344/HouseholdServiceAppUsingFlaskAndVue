<template>
  <div>
    <main>
        <section id="hero-section">
          <div class="hero">
            <div class="first-col">
              <span>Contact Details</span>
              <div class="row" v-for="(contact,index) in contactInfo" :key="index">
                <div class="col1">
                  <i :class="[contact.icon, 'icon']"></i>
                </div>
                <div class="col2">
                  <p>{{ contact.title }}</p>
                  <p>{{ contact.value }}</p>
                </div>
              </div>
            </div>
            
            <div class="second-col">
              <span>Drop Us a Line</span>
              <form>
                <div>
                  <input type="text" placeholder="your name">
                </div>
                <div>
                  <input type="email" placeholder="your email">
                </div>
                <div>
                  <input type="text" placeholder="your phone number">
                </div>
                <div>
                  <input type="text" placeholder="your address">
                </div>    
                <div>
                  <textarea placeholder="your comment" cols="10" rows="10"></textarea>
                </div>
              </form>
              <div class="row">
                <p>We will contact you within one business day.</p>
                <button>send message</button>
              </div>
            </div>
          </div>
        </section>
    </main>
  </div>
</template>

<script>
import ContactScript from '../scripts/contact.js'

export default{
  name : "ContactPage",
  components : {
  },
  data(){
    return ContactScript.data()
  }
}
</script>

<style src="../assets/styles/contact.css"></style>