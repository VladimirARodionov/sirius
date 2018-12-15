<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-12">
        <div class="row">
          <div class="col-md-6 mx-auto">

            <!-- form card login -->
            <div class="card rounded-0">
              <div class="card-header">
                <h3 class="mb-0">{{'Password reset' | translate}} </h3>
              </div>
              <div container v-if="result">
                <div class="row">
                  <div class="col col-lg-6">
                    <div class="alert alert-success" v-if="result.success">
                      <p>{{ 'Password reset link was sent to your email' | translate}}</p>
                    </div>
                    <div class="alert alert-danger" v-else-if="result.error">
                      <p>{{ 'Failure' | translate}}</p>
                      <div>{{ result.error }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="card-body">
                <form class="form-container" @submit.prevent="resetPassword">
                  <div class="form-group">

                    <input v-model="email" type="email" name="email" id="id_email" class="form-control" placeholder="Email" required autofocus />

                  </div>

                  <button type="submit" class="btn btn-primary btn-block">{{'Reset password' | translate}}</button>

                </form>
              </div>
              <!--/card-block-->
            </div>
            <!-- /form card login -->
          </div>
        </div>
        <!--/row-->
      </div>
      <!--/col-->
    </div>
    <!--/row-->
  </div>
  <!--/container-->

</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      email: '',
      result: {}
    }
  },
  methods: {
    resetPassword: function () {
      this.errorMessage = ''
      var formData = new FormData()
      formData.append('email', this.email)
      axios.post(process.env.API_URL + '/api/accounts/password_reset/', formData)
        .then(resp => {
          if (resp.data.result) {
            this.result = resp.data.result
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  name: 'ResetPasswordEmail'
}
</script>

<style scoped>

</style>
