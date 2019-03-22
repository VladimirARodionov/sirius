<template>
  <v-autocomplete
    :id="field.name"
    :label="$t(field.text) + (field.required?' *':'')"
    :error-messages="errorMessage[field.value]"
    chips
    deletable-chips
    :maxlength="field.maxlength"
    v-model="object[field.value]"
    :items="data.objects"
    :item-text="field.item_text"
    :item-value="field.item_value"
    :search-input.sync="search_term"
    :loading="data.loading"
  >
  </v-autocomplete>
</template>

<script>
import { onGetAll } from '../api/requests'

export default {
  name: 'AppointmentSelectField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      data: {
        objects: [],
        loading: false
      },
      object: this.value.currentObject,
      errorMessage: {},
      pagination: {
        page: 1,
        rowsPerPage: 20
      },
      search_term: ''
    }
  },
  created () {
    this.$bus.on('error', this.onError)
    this.$bus.on('changeAppointmentDate', this.onChangeAppointmentDate)
  },
  beforeDestroy () {
    this.$bus.off('error', this.onError)
    this.$bus.off('changeAppointmentDate', this.onChangeAppointmentDate)
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
    },
    onChangeAppointmentDate (date) {
      if (date) {
        this.getItems(date)
      }
    },
    getItems (date) {
      onGetAll(this.field.api + '?date=' + date, 'objects', this.data)
    }
  }
}
</script>

<style scoped>

</style>
