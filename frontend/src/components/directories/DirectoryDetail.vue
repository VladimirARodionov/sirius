<template>
  <v-card>
    <v-card-title class="headline lighten-2" primary-title> {{title}} </v-card-title>
    <v-form>
      <v-card-text>
        <div class="alert alert-danger" v-if="errorMessage">
          {{errorMessage}}
        </div>
        <div class="form-group" v-for="field_name in getNames()" :key="field_name.name">
          <div v-if="field_name.type === 'input'">
            <label :for="field_name.name">{{field_name.text | translate}}</label>
            <input
              type="text"
              class="form-control"
              :id="field_name.name"
              v-model="object[field_name.name]">
          </div>
          <div v-else-if="field_name.type === 'selector'">
            <div class="form-row align-items-center">
              <label >{{field_name.text | translate}}</label>&nbsp;
              <label v-if="data[field_name.name]">{{ data[field_name.name].name }}</label>
              <label v-else>{{ 'Not selected' | translate}}</label>
              <span class="input-group-btn">
                <v-btn color="green darken-1" @click="find(field_name.routerName)">{{'Find' | translate}}</v-btn>
              </span>
            </div>
          </div>
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
</template>

<script>
import Vue from 'vue'
import { onGetSingle } from '../../api/requests'
export default {
  name: 'DirectoryDetail',
  data () {
    return {
      defaultNames: [
        { text: 'Name', type: 'input', name: 'name', required: true }
        // { text: 'City', type: 'selector', name: 'city', routerName: 'cities', api: '/api/city/', required: true }
      ],
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  mounted: function () {
    const names = this.getNames()
    for (const field in names) {
      if (names[field].type === 'selector' && this.object[names[field].name]) {
        Vue.set(this.data, names[field].name, { id: this.object[names[field].name] })
        this.getSelectedObject(this.object[names[field].name].api, this.object[names[field].name].name)
      }
    }
    if (this.$store.getters.getSelectedObject) {
      const selectedValue = JSON.parse(JSON.stringify(this.$store.getters.getSelectedObject))
      this.$store.commit('clearSelectedObject')
      Vue.set(this.data, selectedValue.name, { id: selectedValue.id })
      this.getSelectedObject(selectedValue.api, selectedValue.name)
    }
  },
  methods: {
    clicked () {
      const names = this.getNames()
      for (const field in names) {
        if (names[field].type === 'selector') {
          this.onSelect({ name: names[field].name, id: this.data[names[field].name].id })
        }
      }
      this.onClicked() // TODO: show popup message depending on errorMessage set or not. Or this.$router.go(-1)
    },
    find (routerName) {
      this.$router.push({ name: routerName, query: { select: true } })
    },
    getSelectedObject (api, name) {
      onGetSingle(api, name, this.data)
    },
    getNames: function () {
      if (this.names) {
        return this.names
      } else {
        return this.defaultNames
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
    names: Array,
    onSelect: Function
  }
}
</script>

<style scoped>

</style>
