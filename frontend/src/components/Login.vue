<template>
  <div class="container py-5">
    <div class="row">
      <div class="col-md-12">
        <div class="row">
          <div class="col-md-6 mx-auto">

            <!-- form card login -->
            <div class="card rounded-0">
              <div class="card-header">
                <h3 class="mb-0">Login</h3>
              </div>
              <div class="card-body">
                <form class="form-container" method="post" @submit.prevent="login">
                  <div class="form-group">

                    <input v-model="username" type="email" name="username" id="id_username" class="form-control" placeholder="Email"
                           required autofocus/>

                  </div>

                  <div class="form-group">

                    <input v-model="password" type="password" name="password" class="form-control" id="id_password" placeholder="Password"
                           required>

                  </div>
                  <div class="forgot">
                    <a href="">Lost password?</a>
                  </div>
                  <input type="hidden" name="next" value=""/>
                  <button type="submit" class="btn btn-primary btn-block">Login</button>

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

</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login: function () {
      let username = this.username
      let password = this.password
      this.$store.dispatch('login', {username, password})
        .then(() => this.$router.push('/'))
        .catch(err => console.log(err))
    }
  },
  name: 'Login'

}
</script>

<style scoped>

</style>
