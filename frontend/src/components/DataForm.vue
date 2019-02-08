<template>
  <v-card>
    <v-card-title class="headline grey lighten-2" primary-title> {{data.title | translate}} </v-card-title>
      <v-card-text>
     <FormBuilder
      v-if="loaded"
      :resource="resource"
      :id="id"
      :data="data"/>
     </v-card-text>
   </v-card>
</template>

<script>
import FormBuilder from './FormBuilder'

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
    data: {},
    loaded: false
  }),
  created () {
    this.fetchData()
  },
  methods: {
    fetchData () {
      this.loaded = false
      let json = this.getJson()
      this.data = json
      this.loaded = true
    },
    getJson () {
      const json = require('./' + this.resource + this.action + '.json')
      return json
    }
  }
}
</script>

<style scoped>

</style>
