<template>
  <Default>
    <div container>
      <div class="row">
        <div class="col col-lg-6">
          <a v-on:click="goLogin()">{{'Login' | translate}}</a>
        </div>
      </div>
    </div>

    <!-- Change password Modal -->
    <v-dialog v-model="changePasswordDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Password reset' | translate}}</v-card-title>
        <v-form>
          <v-card-text>
            <div container v-if="result">
              <div class="row">
                <div class="col col-lg-6">

                  <div class="alert alert-success" v-if="result.success">
                    <p>{{ 'Password reset successfully' | translate}}</p>
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
                required>
            </div>
            <div class="form-group">
              <label for="id_new_password2">{{'Password confirmation' | translate}}</label>
              <input
                type="password"
                class="form-control"
                name="new_password2"
                id="id_new_password2"
                v-model="passwords.new_password2"
                required>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" @click="changePasswordDialog = false">{{'Close' | translate}}</v-btn>
            <v-btn color="green darken-1" @click="changePassword()">{{'Save' | translate}}</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <!-- End of change password -->
  </Default>
</template>

<script>
import axios from 'axios'
import router from '../router'
import Default from '../layouts/Default'

export default {
  name: 'ResetPasswordConfirm',
  data () {
    return {
      errorMessage: '',
      changePasswordDialog: false,
      passwords: { new_password1: '', new_password2: '' },
      result: {}
    }
  },
  mounted: function () {
    this.validateLink()
  },
  methods: {
    validateLink: function () {
      axios.get(process.env.API_URL + '/api/accounts/reset/' + this.$route.params.uidb64 + '/' + this.$route.params.token + '/')
        .then(resp => {
          if (resp.data.result) {
            if (resp.data.result.success) {
              if (resp.data.result.validlink) {
                this.changePasswordDialog = true
              } else {
                this.changePasswordDialog = false
              }
            }
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    goLogin: function () {
      router.push({ name: 'login' })
    },
    changePassword: function () {
      this.errorMessage = ''
      var formData = new FormData()
      formData.append('new_password1', this.passwords.new_password1)
      formData.append('new_password2', this.passwords.new_password2)
      axios.post(process.env.API_URL + '/api/accounts/reset/' + this.$route.params.uidb64 + '/' + this.$route.params.token + '/', formData)
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
  },
  components: {
    Default
  }

}
</script>

<style scoped>

</style>
