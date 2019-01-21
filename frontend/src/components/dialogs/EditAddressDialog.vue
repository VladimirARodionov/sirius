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
            <label for="edit_city_id">{{'City' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_city_id"
              v-model="currentObject.city_id"
              required="required">
          </div>
          <div class="form-group">
            <label for="edit_village">{{'Village' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_village"
              v-model="currentObject.village">
          </div>
          <div class="form-group">
            <label for="edit_street">{{'Street' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_street"
              v-model="currentObject.street">
          </div>
          <div class="form-group">
            <label for="edit_house">{{'House' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_house"
              v-model="currentObject.house">
          </div>
          <div class="form-group">
            <label for="edit_apartment">{{'Apartment' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="edit_apartment"
              v-model="currentObject.apartment">
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
  name: 'EditAddressDialog',
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
    currentObject: Object,
    onClicked: Function
  }
}
</script>

<style scoped>

</style>
