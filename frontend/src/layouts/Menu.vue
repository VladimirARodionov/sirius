<template>
  <div>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <router-link class="navbar-brand" active-class="active" :to="json.value">{{json.title | translate}}</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup"
              aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav d-lg-flex align-items-center">
          <div v-for="field in json.fields" :key="field.name">
            <router-link class="nav-item nav-link" active-class="active"
                       :to="field.value">{{field.text | translate}}</router-link>
          </div>
        </div>
        <div class="navbar-nav ml-auto d-lg-flex align-items-center">
          <div class="nav-item">
            <a class="nav-link" style="cursor: pointer;" @click="logout"><v-icon small color="grey">person</v-icon>{{'Logout' | translate}}</a>
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
  props: {
    program: {
      type: String,
      required: true
    }
  },
  data: () => ({
    json: {}
  }),
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      this.loaded = false
      this.json = this.getJson()
      this.loaded = true
    },
    getJson () {
      const json = require('./' + this.program + '.json')
      return json
    },
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
