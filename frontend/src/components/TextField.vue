<template>
  <v-text-field
    :id="field.name"
    :label="$t(field.text) + (field.required?' *':'')"
    :error-messages="errorMessage[field.value]"
    v-model="object[field.value]">
  </v-text-field>
</template>

<script>
export default {
  name: 'TextField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      object: {},
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
  methods: {
    onError (data) {
      this.errorMessage = data
    }
  }
}
</script>

<style scoped>

</style>
