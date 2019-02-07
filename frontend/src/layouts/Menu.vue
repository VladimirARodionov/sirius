<template>
  <div>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <router-link class="navbar-brand" active-class="active" to="/">{{'Sirius' | translate}}</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup"
              aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav d-lg-flex align-items-center">
          <router-link class="nav-item nav-link" active-class="active"
                       to="/employee">{{'Employees' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active"
                       to="/disciple">{{'Disciples' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active"
                       to="/reports">{{'Reports' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active"
                       to="/actions">{{'Actions' | translate}}</router-link>
          <router-link class="nav-item nav-link" active-class="active"
                       to="/directory">{{'Directories' | translate}}</router-link>
        </div>
        <div class="navbar-nav ml-auto d-lg-flex align-items-center">
          <div class="nav-item">
            <a class="nav-link" style="cursor: pointer;" @click="logout"><font-awesome-icon icon="user"/>{{'Logout' | translate}}</a>
          </div>
        </div>
      </div>
    </nav>
    <div class="container-fluid">

      <div class="row">
        <div class="col-sm-12">
          <slot/>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
export default {
  name: 'Menu',
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
    }
  }
}
</script>

<style scoped>

</style>
