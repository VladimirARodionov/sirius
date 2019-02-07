<template>
   <div>
     <FormBuilder
      v-if="loaded"
      :resource="resource"
      :id="id"
      :data="data"
    ></FormBuilder>
   </div>
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
  mounted () {
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
      const json = require('./' + this.resource + '.json')
      return json
    }
  }
}
</script>

<style scoped>

</style>
