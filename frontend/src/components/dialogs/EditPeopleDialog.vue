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
            <label for="edit_first_name">{{'First name' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_first_name"
              v-model="currentPeople.first_name"
              required="required">
          </div>
          <div class="form-group">
            <label for="edit_last_name">{{'Last name' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_last_name"
              v-model="currentPeople.last_name"
              required="required">
          </div>
          <div class="form-group">
            <label for="edit_email">{{'Email' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_email"
              v-model="currentPeople.email">
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click.native="close">{{'Close' | translate}}</v-btn>
          <v-btn color="green darken-1" @click="clicked()">{{'Save' | translate}}</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>

</template>

<script>
export default {
  name: 'EditPeopleDialog',
  methods: {
    clicked () {
      this.onClicked()
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
    currentPeople: Object,
    onClicked: Function
  }
}
</script>

<style scoped>

</style>
