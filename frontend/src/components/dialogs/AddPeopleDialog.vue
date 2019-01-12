<template>
  <v-dialog v-model="dialog" persistent max-width="800">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title> {{title}} </v-card-title>
      <v-form>
        <v-card-text>

          <div class="alert alert-danger" v-if="errorMessage">
            {{errorMessage}}
          </div>
          <div class="form-group">
            <label for="add_first_name">{{'First name' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_first_name"
              v-model="newPeople.first_name"
              required="required">
          </div>
          <div class="form-group">
            <label for="add_last_name">{{'Last name' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_last_name"
              v-model="newPeople.last_name"
              required="required">
          </div>
          <div class="form-group">
            <label for="add_email">{{'Email' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_email"
              v-model="newPeople.email">
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click.native="close">{{'Close' | translate}}</v-btn>
          <v-btn color="green darken-1" @click.native="clicked()">{{'Save' | translate}}</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>

</template>

<script>
export default {
  name: 'AddPeopleDialog',
  methods: {
    clicked () {
      this.errorMessage = ''
      try {
        this.onClicked()
      } catch (err) {
        console.log(err)
        if (err.response && err.response.data) {
          var errors = err.response.data
          for (var value in errors) {
            if (value instanceof Array) {
              this.errorMessage = errors[value][0]
            } else {
              this.errorMessage = errors[value]
            }
          }
          console.log(err.response.data)
        }
      }
    },
    close () {
      this.$emit('update:dialog', false)
    }
  },
  props: {
    dialog: {
      default: false
    },
    errorMessage: {
      default: ''
    },
    title: String,
    newPeople: Object,
    onClicked: Function
  }
}
</script>

<style scoped>

</style>
