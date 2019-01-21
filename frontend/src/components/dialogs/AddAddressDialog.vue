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
            <label for="add_city_id">{{'City' | translate}}</label>
            <v-select id="add_city_id" :items="newObject.city_items" required="required"></v-select>
            <input
              type="text"
              class="form-control"
              id="add_city_id"
              v-model="newObject.city_id"
              required="required">
          </div>
          <div class="form-group">
            <label for="add_village">{{'Village' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_village"
              v-model="newObject.village">
          </div>
          <div class="form-group">
            <label for="add_street">{{'Street' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_street"
              v-model="newObject.street">
          </div>
          <div class="form-group">
            <label for="add_house">{{'House' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_house"
              v-model="newObject.house">
          </div>
          <div class="form-group">
            <label for="add_apartment">{{'Apartment' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="add_apartment"
              v-model="newObject.apartment">
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
  name: 'AddAddressDialog',
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
    newObject: Object,
    onClicked: Function
  }
}
</script>

<style scoped>

</style>
