<template>
  <div id="app">
    <NavBar v-if="showNavBar" @edit-profile="editProfile"/>
    <Profile v-if="showNavBar" 
    :savedCredential="savedCredential"
    :isEditingProfile="isEditingProfile" 
    @close-Profile="closeProfileForm"/>
    <router-view></router-view>
    <Footer v-if="showNavBar" />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';
import ProfileSection from './components/ProfileSection.vue'
import FooterSection from './components/FooterSection.vue';

export default {
  name: 'App',
  components: {
    "NavBar" : NavBar,
    "Footer" : FooterSection,
    "Profile" : ProfileSection,
  },

  data : function(){
    return{
      isEditingProfile : false,
      savedCredential : {
        email : localStorage.getItem("email"),
        user_name : localStorage.getItem("user_name"),
        user_id : localStorage.getItem("user_id"),
        role : localStorage.getItem("role"),
      },
    }
  },

  computed : {
    showNavBar(){
      const routesWithNavBar = ['home', 'about', 'blog', 'contact', 'transaction'];
      return routesWithNavBar.includes(this.$route.name);
    }
  },

  methods : {
    editProfile(){
      this.isEditingProfile = true;
    },

    closeProfileForm(){
      this.isEditingProfile = !this.isEditingProfile;
    },

    closeModal(event){
      if(event.target === event.currentTarget){
        this.showAddServiceRequestForm = false;
      }
    },
  }
}
</script>