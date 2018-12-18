<template>
  <div id="app">
    <v-app>
    <span v-if="isLoggedIn">
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <router-link class="navbar-brand" active-class="active" to="/">{{'Sirius' | translate}}</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav d-lg-flex align-items-center">
          <router-link class="nav-item nav-link" active-class="active" to="/people">{{'People' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active" to="/reports">{{'Reports' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active" to="/actions">{{'Actions' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active" to="/directories">{{'Directories' | translate}}</router-link>
        </div>
        <div class="navbar-nav ml-auto d-lg-flex align-items-center">
          <div class="nav-item">
            <a class="nav-link" style="cursor: pointer;" @click="logout"><font-awesome-icon icon="user" />{{'Logout' | translate}}</a>
          </div>
        </div>
      </div>
    </nav>
    <div class="container-fluid">

      <div class="row">
        <div class="col-sm-2">
        </div>
        <div class="col-sm-10 ">
          <router-view></router-view>
        </div>
      </div>

    </div>

    </span>
      <span v-else>
          <router-view></router-view>
      </span>
    </v-app>
  </div>
</template>

<script>
const axios = require('axios')

export default {
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isLoggedIn
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
    }
  },
  created: function () {
    axios.interceptors.response.use(
      (response) => {
        return response
      },
      (err) => {
        if (err.response.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw err
      })
  },
  name: 'App'
}
</script>

<style lang="scss">
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
</style>
