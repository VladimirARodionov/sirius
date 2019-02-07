<template>
  <div>
      <div v-for="field in fields" :key="field.name">
        <!--<div>{{JSON.stringify(field) + ' ' + JSON.stringify(name) + ' ' + model[field.name]}}</div>-->
        <FormFieldFactory v-model="model" :id="getFieldId(field.name)"
        :name="field.name" :text="field.text" :field="field" :key="id + '_' +field.name" />
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
    data: {
      type: Object,
      required: true
    }
  },
  components: {
    FormFieldFactory
  },
  data () {
    return {
      model: {},
      errors: [],
      fields: this.data.fields
    }
  },
  created () {
    this.populateModel(this.data.fields)
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
