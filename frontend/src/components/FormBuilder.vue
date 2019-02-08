<template>
  <div>
      <div v-for="field in json.fields" :key="field.name">
        <!--<div>{{JSON.stringify(field)}}</div>-->
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
  },
  created () {
    // this.populateModel(this.json.fields)
  },
  methods: {
    getFieldId (name) {
      return `input_${name}`
    },
    setValue (name, value) {
      this.$set(this.model, name, value)
      return this.$emit('input', this.model)
    },
    populateModel (field) {
      for (const v of field) {
        if (!this.model[v.name]) {
          this.$set(this.model, v.name, v.value)
        }
        if (v.fields) {
          this.populateModel(v.fields)
        }
      }
    }
  }
}
</script>

<style scoped>

</style>
