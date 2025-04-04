import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import './assets/styles/global.css'



// import components
import AdminPage from './components/AdminPage.vue'
import HomePage from './components/HomePage.vue'
import AboutPage from './components/AboutPage.vue'
import BlogPage from './components/BlogPage.vue'
import ContactPage from './components/ContactPage.vue'
import LoginPage from './components/LoginPage.vue'
import TransactionPage from './components/TransactionPage.vue'

Vue.use(VueRouter)

// Define your routes
const routes = [
  { path: '/', component: LoginPage },
  { path: '/admin', name : "admin", component : AdminPage },
  { path: '/home', name : "home", component : HomePage },
  { path: '/about', name : "about", component : AboutPage },
  { path: '/blog', name : "blog", component : BlogPage },
  { path: '/contact', name : "contact", component : ContactPage },
  { path: '/transaction',name : "transaction", component: TransactionPage},
];


// Create the router instance
const router = new VueRouter({
  routes
});

new Vue({
  render: h => h(App),
  router
}).$mount('#app')

