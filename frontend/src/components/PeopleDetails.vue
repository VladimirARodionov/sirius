<template>
  <div>
    <h1>{{'User details' | translate}}</h1>
    <div class="alert alert-danger" v-if="errorMessage">
      {{errorMessage}}
    </div>
    <form @submit.prevent="updatePeople()">
      <div class="form-row">
        <div class="form-group col-md-3">
          <label for="last_name">{{'Last name' | translate}}</label>
          <input type="text" class="form-control" id="last_name" name="last_name" required v-model="currentPeople.last_name">
        </div>
        <div class="form-group col-md-3">
          <label for="first_name">{{'First name' | translate}}</label>
          <input type="text" class="form-control" id="first_name" name="first_name" required v-model="currentPeople.first_name">
        </div>
        <div class="form-group col-md-3">
          <label for="middle_name">{{'Middle name' | translate}}</label>
          <input type="text" class="form-control" id="middle_name" name="middle_name" v-model="currentPeople.middle_name">
        </div>
      </div>
      <div class="form-group">
        <label for="email">{{'Email' | translate}}</label>
        <input type="email" class="form-control" id="email" name="email" v-model="currentPeople.email">
      </div>
      <div class="form-group">
        <label for="mobile">{{'Mobile' | translate}}</label>
        <input type="tel" class="form-control" id="mobile" name="mobile" v-model="currentPeople.mobile">
      </div>
      <div class="form-group">
        <label for="birthday">{{'Birthday' | translate}}</label>
        <input type="date" class="form-control" id="birthday" name="birthday" v-model="currentPeople.birthday">
      </div>
      <div class="btn-toolbar justify-content-between mb-3">
        <div>
          <button type="submit" class="btn btn-primary">{{'Save' | translate}}</button>
          <button class="btn btn-danger" data-toggle="modal" data-target="#changePasswordModal">{{'Change password' | translate}}</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PeopleDetails',
  data () {
    return {
      currentPeople: {},
      errorMessage: ''
    }
  },
  mounted: function () {
    this.getPeople()
  },
  methods: {
    getPeople: function () {
      axios.get(process.env.API_URL + '/api/userdetail/' + this.$route.params.id + '/')
        .then(resp => {
          this.currentPeople = resp.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    updatePeople: function () {
      this.loading = true
      this.errorMessage = ''
      axios.put(process.env.API_URL + '/api/userdetail/' + this.$route.params.id + '/', this.currentPeople)
        .then(resp => {
          this.currentPeople = resp.data
          this.getPeople()
        })
        .catch(err => {
          this.loading = false
          console.log(err)
          if (err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              this.errorMessage = JSON.stringify(errors[value]).replace(/[\[\]"]+/g, '')
            }
            console.log(err.response.data)
          }
        })
    }
  }

}
</script>

<style scoped>

</style>
