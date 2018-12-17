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
          <button class="btn btn-danger" v-on:click="changePasswordDialog = true">{{'Change password' | translate}}</button>
        </div>
      </div>
    </form>
        <!-- Change password Modal -->
    <v-dialog v-model="changePasswordDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Password change' | translate}}</v-card-title>
          <v-form>
            <v-card-text>
            <div container v-if="result">
                <div class="row">
                    <div class="col col-lg-6">

                            <div class="alert alert-success" v-if="result.success">
                                <p>{{ 'Password changed successfully' | translate}}</p>
                            </div>
                            <div class="alert alert-danger" v-else-if="result.error">
                                <p>{{ 'Failure' | translate}}</p>
                                <div>{{ result.error }}</div>
                            </div>
                    </div>
                </div>
            </div>

              <div class="form-group">
                <label for="id_new_password1">{{'New password' | translate}}</label>
                <input
                  type="password"
                  class="form-control"
                  name="new_password1"
                  id="id_new_password1"
                  v-model="passwords.new_password1"
                  required >
              </div>
              <div class="form-group">
                <label for="id_new_password2">{{'Password confirmation' | translate}}</label>
                <input
                  type="password"
                  class="form-control"
                  name="new_password2"
                  id="id_new_password2"
                  v-model="passwords.new_password2"
                  required >
              </div>
            </v-card-text>
            <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click="changePasswordDialog = false">{{'Close' | translate}}</v-btn>
          <v-btn color="green darken-1" @click="changePassword()">{{'Change' | translate}}</v-btn>
        </v-card-actions>
          </v-form>
      </v-card>
    </v-dialog>
    <!-- End of change password -->
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PeopleDetails',
  data () {
    return {
      currentPeople: {},
      errorMessage: '',
      changePasswordDialog: false,
      passwords: {new_password1: '', new_password2: ''},
      result: {}
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
      this.errorMessage = ''
      axios.put(process.env.API_URL + '/api/userdetail/' + this.$route.params.id + '/', this.currentPeople)
        .then(resp => {
          this.currentPeople = resp.data
          this.getPeople()
        })
        .catch(err => {
          console.log(err)
          if (err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              this.errorMessage = errors[value][0]
            }
            console.log(err.response.data)
          }
        })
    },
    changePassword: function () {
      this.errorMessage = ''
      axios.post(process.env.API_URL + '/api/people/' + this.$route.params.id + '/password_change', this.passwords)
        .then(resp => {
          if (resp.data.result) {
            this.result = resp.data.result
          }
        })
        .catch(err => {
          console.log(err)
          if (err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              this.errorMessage = errors[value][0]
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
