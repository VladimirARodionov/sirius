<template>
  <v-card>
    <v-card-title class="headline grey lighten-2" primary-title> {{json.title | translate}} </v-card-title>
      <v-card-text>
     <FormBuilder
      v-if="loaded"
      :resource="resource"
      :id="id"
      :json="json"
      v-model="data"/>
     </v-card-text>
   </v-card>
</template>

<script>
import FormBuilder from './FormBuilder'
import { onGetSingle, onPostSingle, onPutSingle, onDelete } from '../api/requests'

export default {
  name: 'DataForm',
  props: {
    resource: {
      type: String,
      required: true
    },
    action: {
      type: String,
      required: true
    },
    id: {
      default: ''
    }
  },
  components: {
    FormBuilder
  },
  data: () => ({
    json: {},
    data: {
      currentObject: {},
      loading: false,
      errorMessage: ''
    },
    loaded: false
  }),
  created () {
    this.fetchData()
    this.$bus.on('changeObject', this.onChangeObject)
    this.$bus.on('save', this.onSave)
  },
  beforeDestroy () {
    this.$bus.off('changeObject', this.onChangeObject)
    this.$bus.off('save', this.onSave)
  },
  methods: {
    fetchData () {
      this.loaded = false
      this.json = this.getJson()
      this.loaded = true
    },
    getJson () {
      const json = require('./' + this.resource + this.action + '.json')
      return json
    },
    onChangeObject (data) {
      this.data.currentObject = data
    },
    onSave () {
      if (this.json.type === 'add') {
        this.addObject()
      } else if (this.json.type === 'edit') {
        this.updateObject()
      }
    },
    getObject () {
      onGetSingle(this.json.api, 'curentObject', this.data)
    },
    addObject: function () {
      onPostSingle(this.json.api, this.data, this.getObject)
    },
    updateObject: function () {
      onPutSingle(this.json.api, this.data, this.getObject)
    },
    deleteObject: function () {
      onDelete(this.json.api, this.data, this.getObject)
    }
  }
}
</script>

<style scoped>

</style>
