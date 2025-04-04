<template>
  <header id="header-section">
    <img src="../assets/images/logo.jpg" alt="Logo">
    <nav class="navbar">
      <ul>
        <li>
          <router-link to="/home">home</router-link>
        </li>
        <li>
          <router-link to="/about">about</router-link>
        </li>
        <li>
          <router-link to="/blog">blog</router-link>
        </li>
        <li>
          <router-link to="/contact">contact</router-link>
        </li>
        <li id="dropdown" v-if="is_auth">
          <router-link to="#" @click.prevent="triggeredEditProfile()">Hello {{ username }}</router-link>  
          <ul id="dropdownContent">
            <li>
              <a @click.prevent="triggeredEditProfile">Edit Profile</a>
            </li>
            <li>
              <router-link to="transaction">Transactions</router-link>
            </li>
            <li>
              <router-link to="#">Log Out</router-link>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
  export default{
    data: function(){
      return{
        "username" : localStorage.getItem("user_name"),
        "is_auth" : localStorage.getItem("auth_token"),
      }
    },
    methods: {
      triggeredEditProfile() {
        this.$emit('edit-profile');
      }
    }
  }
</script>