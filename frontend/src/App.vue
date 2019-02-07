<template>
  <div id="app">
    <v-app>
      <router-view :key="$route.name + ($route.params.resource || '') + ($route.params.id || '')"></router-view>
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
  created: function () {
    axios.interceptors.response.use(
      (response) => {
        return response
      },
      (err) => {
        if (err.response && err.response.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch('logout')
        }
        throw err
      })
  },
  name: 'App'
}
</script>

<style lang="scss">
</style>
