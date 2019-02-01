<template>
  <v-card>
    <v-card-title class="headline lighten-2" primary-title> {{title}} </v-card-title>
    <v-form>
      <v-card-text>
        <v-alert outline type="error" value="true" v-if="errorMessageText">
          {{errorMessageText}}
        </v-alert>
        <v-item-group v-for="field_name in getNames" :key="field_name.name">
          <v-item-group v-if="field_name.type === 'input'">
            <v-text-field
              :id="field_name.name"
              :label="$t(field_name.text) + (field_name.required?' *':'')"
              :error-messages="errorMessage[field_name.name]"
               v-model="getObject[field_name.name]">
            </v-text-field>
          </v-item-group>
          <v-item-group v-else-if="field_name.type === 'selector'">
              <v-text-field
                :label="$t(field_name.text) + (field_name.required?' *':'')"
                readonly
                type="text"
                :id="field_name.name"
                :error-messages="errorMessage[field_name.name]"
                v-if="data[field_name.name]"
                append-icon="search"
                @click:append="find(field_name.routerName)"
                v-model="data[field_name.name].name">
              </v-text-field>
              <v-text-field
                :label="$t(field_name.text) + (field_name.required?' *':'')"
                readonly
                type="text"
                :id="field_name.name"
                :error-messages="errorMessage[field_name.name]"
                v-else
                append-icon="search"
                @click:append="find(field_name.routerName)"
                :value="'Not selected' | translate">
              </v-text-field>
          </v-item-group>
        </v-item-group>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="gray darken-1" @click="$router.go(-1)">{{'Back' | translate}}</v-btn>
        <v-btn color="green darken-1" @click.native="clicked()">{{'Save' | translate}}</v-btn>
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
        currentObject: { 'text': null, parent: null },
        loading: false,
        errorMessage: ''
      }
    }
  },
  mounted: function () {
    if (this.$store.getters.getSelectedObject) {
      const selectedValue = JSON.parse(JSON.stringify(this.$store.getters.getSelectedObject))
      this.$store.commit('clearSelectedObject')
      Vue.set(this.data, selectedValue.name, { id: selectedValue.id })
      this.getSelectedObject(selectedValue.api, selectedValue.name)
    }
  },
  beforeUpdate: function () {
  },
  updated: function () {
    const names = this.getNames
    for (const field in names) {
      if (names[field].type === 'selector' && !this.data[names[field].name] && this.object[names[field].name]) {
        Vue.set(this.data, names[field].name, { id: this.object[names[field].name] })
        this.getSelectedObject(names[field].api, names[field].name)
      }
    }
  },
  methods: {
    clicked () {
      if (this.onUpdate) {
        this.onUpdate(this.getObject)
      }
      const names = this.getNames
      for (const field in names) {
        if (names[field].type === 'selector') {
          if (this.data[names[field].name]) {
            this.onSelect({ name: names[field].name, id: this.data[names[field].name].id })
          }
        }
      }
      this.onClicked()
    },
    find (routerName) {
      this.$store.commit('setSavedState', { name: this.name, obj: this.object })
      this.$router.push({ name: routerName, query: { select: 'true' } })
    },
    getSelectedObject (api, name) {
      onGetSingle(api, name, this.data)
    }
  },
  computed: {
    getNames: function () {
      if (this.names) {
        return this.names
      } else {
        return this.defaultNames
      }
    },
    getObject: function () {
      if (this.$store.getters.getSavedState[this.name]) {
        let savedState = this.$store.getters.getSavedState[this.name]
        this.$store.commit('clearSavedState', this.name)
        return savedState
      } else {
        return this.object
      }
    },
    errorMessageText: function () {
      const errors = this.errorMessage
      for (const value in errors) {
        if (errors[value] instanceof Array) {
          const names = this.getNames
          for (const field in names) {
            if (names[field].name === value) {
              return ''
            }
          }
          return errors[value][0]
        } else {
          return errors[value]
        }
      }
      return ''
    }
  },
  props: {
    errorMessage: {
      default: ''
    },
    title: String,
    name: String,
    object: Object,
    onClicked: Function,
    names: Array,
    onSelect: Function,
    onUpdate: Function
  }
}
</script>

<style scoped>

</style>
