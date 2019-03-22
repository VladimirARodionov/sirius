<template>
  <v-textarea
    :id="field.name"
    :label="$t(field.text) + (field.required?' *':'')"
    :error-messages="errorMessage[field.value]"
    counter
    auto-grow
    v-model="object[field.value]">
  </v-textarea>
</template>

<script>
export default {
  name: 'TextAreaField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      object: this.value.currentObject,
      errorMessage: {}
    }
  },
  created () {
    this.$bus.on('error', this.onError)
  },
  beforeDestroy () {
    this.$bus.off('error', this.onError)
  },
  updated () {
    this.$bus.emit('changeObject', this.object)
  },
  watch: {
    value: {
      handler () {
        this.object = this.value.currentObject
        this.errorMessage = this.value.errorMessage
      },
      deep: true
    }
  },
  methods: {
    onError (data) {
      this.errorMessage = data
    }
  }
}
</script>

<style scoped>

</style>
