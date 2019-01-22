<template>
  <Menu>
    <v-card>
      <v-card-title class="headline lighten-2" primary-title> {{title}} </v-card-title>
      <v-form>
        <v-card-text>

          <div class="alert alert-danger" v-if="errorMessage">
            {{errorMessage}}
          </div>
          <div class="form-group">
            <div class="form-row align-items-center">
              <label >{{'City' | translate}}</label>&nbsp;
              <label >{{ this.getCityName()}}</label>
              <span class="input-group-btn">
                <v-btn color="green darken-1" @click="find()">{{'Find' | translate}}</v-btn>
              </span>
            </div>

          </div>
          <div class="form-group">
            <label for="village">{{'Village' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="village"
              v-model="object.village">
          </div>
          <div class="form-group">
            <label for="street">{{'Street' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="street"
              v-model="object.street">
          </div>
          <div class="form-group">
            <label for="house">{{'House' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="house"
              v-model="object.house">
          </div>
          <div class="form-group">
            <label for="apartment">{{'Apartment' | translate}}</label>
            <input
              type="text"
              class="form-control"
              id="apartment"
              v-model="object.apartment">
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click="$router.go(-1)">{{'Back' | translate}}</v-btn>
          <v-btn color="green darken-1" @click="clicked()">{{'Save' | translate}}</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </Menu>
</template>

<script>
import { onGetSingle } from '../api/requests'
export default {
  name: 'AddressDetail',
  data () {
    return {
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  mounted: function () {
    if (this.object.city) {
      this.data.currentObject.id = this.object.city
    } else {
      this.data.currentObject.id = this.$store.getters.getSelectedId
      this.$store.commit('clearSelectedId')
    }
    this.getCity()
  },
  updated: function () {
    if (this.object.city && !this.data.currentObject.id) {
      this.data.currentObject.id = this.object.city
      this.getCity()
    }
  },
  methods: {
    clicked () {
      this.$emit('onSelectCity', this.data.currentObject.id)
      this.onClicked()
    },
    find () {
      this.$router.push({ name: 'cities', query: { select: true } })
    },
    getCity () {
      onGetSingle('/api/city/', this.data)
    },
    getCityName () {
      if (this.data.currentObject.id) {
        return this.data.currentObject.name
      } else {
        return this.$t('Not selected')
      }
    }
  },
  props: {
    errorMessage: {
      default: ''
    },
    title: String,
    object: Object,
    onClicked: Function,
    select: Boolean
  }
}
</script>

<style scoped>

</style>
