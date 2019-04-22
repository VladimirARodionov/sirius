<template>
    <v-datetime-picker
      :first-day-of-week="1"
      v-model="object[field.value]"
      :label="field.text"
      :error-messages="errorMessage[field.value]"
      locale="ru"/>
</template>

<script>
export default {
  name: 'DateTimeField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      object: this.value.currentObject,
      errorMessage: {},
      menu: false
    }
  },
  created () {
    this.$bus.on('error', this.onError)
    this.$bus.on('beginEndClearAction', this.onBeginEndClearAction)
  },
  beforeDestroy () {
    this.$bus.off('error', this.onError)
    this.$bus.off('beginEndClearAction', this.onBeginEndClearAction)
  },
  updated () {
    this.$bus.emit('changeObject', this.object)
    this.$bus.emit('changeBeginDate', this.object[this.field.value])
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
    },
    save (date) {
      this.$refs[this.field.name + '_menu'].save(date)
    },
    onBeginEndClearAction () {
      this.object[this.field.value] = null
    }
  }
}
</script>

<style scoped>

</style>
