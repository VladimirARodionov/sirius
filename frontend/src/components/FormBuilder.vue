<template>
  <div>
      <div v-for="field in json.fields" :key="field.name">
        <FormFieldFactory
          v-model="value"
          :field="field"/>
      </div>
  </div>
</template>

<script>
import FormFieldFactory from './FormFieldFactory'

export default {
  name: 'FormBuilder',
  props: {
    resource: {
      type: String,
      required: true
    },
    id: {
      default: ''
    },
    json: {
      type: Object,
      required: true
    },
    value: {}
  },
  components: {
    FormFieldFactory
  },
  data () {
    return {
      model: {},
      errors: [],
      fields: this.json.fields
    }
  }
}
</script>

<style scoped>

</style>
