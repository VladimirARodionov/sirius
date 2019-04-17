<template>
  <v-menu
    :ref="field.name + '_menu'"
    lazy
    :close-on-content-click="false"
    v-model="menu"
    transition="scale-transition"
    offset-y
    full-width
    :nudge-right="40"
    min-width="290px"
  >
    <v-text-field
      :id="field.name"
      slot="activator"
      :label="$t(field.text) + (field.required?' *':'')"
      v-model="object[field.value]"
      append-icon="event"
      :error-messages="errorMessage[field.value]"
      readonly/>
    <v-date-picker
      :ref="field.name + '_picker'"
      :first-day-of-week="1"
      v-model="object[field.value]"
      @change="save"
      locale="ru"
      :max="new Date().toISOString().substr(0, 10)"/>
  </v-menu>
</template>

<script>
export default {
  name: 'EndDateField',
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
    this.$bus.emit('changeEndDate', this.object[this.field.value])
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
