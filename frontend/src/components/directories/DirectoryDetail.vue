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
              <label >{{ getSelector(field_name.name)}}</label>
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
    if (this.$store.getters.getSelectedObject) {
      this.data[this.$store.getters.getSelectedObject.name] = {}
      this.data[this.$store.getters.getSelectedObject.name].id = this.$store.getters.getSelectedObject.id
      this.$store.commit('clearSelectedObject')
    }
  },
  updated: function () {
    this.getNames().forEach(function (fieldName, i, arr) {
      if (fieldName.type === 'selector') {
        if (this.data[fieldName.name].id) {
          // this.data[fieldName.name].id = this.object[fieldName.name].id
          this.getSelectedObject(fieldName.api, fieldName.name)
        } else {
          if (this.$store.getters.getSelectedObject[fieldName.name]) {
            this.data[fieldName.name].id = this.$store.getters.getSelectedObject.id
            this.$store.commit('clearSelectedObject')
            this.getSelectedObject(fieldName.api, fieldName.name)
          }
        }
        if (this.object[fieldName.name] && (this.data[fieldName.name] && !this.data[fieldName.name].id)) {
          this.data[fieldName.name].id = this.object[fieldName.name]
          this.getSelectedObject(fieldName.api, fieldName.name)
        }
      }
    })
  },
  methods: {
    clicked () {
      for (const fieldName in this.getNames()) {
        if (fieldName.type === 'selector') {
          this.$emit('onSelect_' + fieldName.name, this.data[fieldName.name].id) // Add onSelect_city method for updating city
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
    getSelector (fieldName) {
      if (this.data[fieldName] && this.data[fieldName].id) {
        return this.data[fieldName].name // TODO: change name to provided JSON value
      } else {
        return this.$t('Not selected')
      }
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
    names: Array
  }
}
</script>

<style scoped>

</style>
