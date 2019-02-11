<template>
  <v-autocomplete
    :id="field.name"
    :label="$t(field.text) + (field.required?' *':'')"
    :error-messages="errorMessage[field.value]"
    chips
    :maxlength="field.maxlength"
    v-model="object[field.value]"
    :items="data.objects"
    :item-text="field.item_text"
    item-value="id"
    :search-input.sync="search_term"
    :loading="data.loading"
    append-icon="edit"
    @click:append="goList()"
  >
  </v-autocomplete>
</template>

<script>
import { onGet } from '../api/requests'

export default {
  name: 'SelectField',
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
  },
  beforeDestroy () {
    this.$bus.off('error', this.onError)
  },
  updated () {
    this.$bus.emit('changeObject', this.object)
  },
  mounted () {
    this.getItems()
  },
  watch: {
    value: {
      handler () {
        this.object = this.value.currentObject
        this.errorMessage = this.value.errorMessage
      },
      deep: true
    },
    search_term: {
      handler () {
        this.getItems()
      }
    }
  },
  methods: {
    onError (data) {
      this.errorMessage = data
    },
    getItems () {
      onGet(this.field.api, this.data, this.pagination, this.search_term)
    },
    goList () {
      this.$router.push('/' + this.field.resource + '/list/')
    }
  }
}
</script>

<style scoped>

</style>
