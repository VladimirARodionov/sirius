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
    :append-icon="field.hide_edit?'':'edit'"
    @click:append="goList()"
  >
  </v-autocomplete>
</template>

<script>
import { onGet } from '../api/requests'
import vuetifyToast from 'vuetify-toast'

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
      if (!this.field.hide_edit) {
        this.$store.commit('setSavedState', {
          resource: this.$route.params.resource,
          id: this.$route.params.id,
          obj: this.value
        })
        vuetifyToast.info(this.$t('ResourceSaved', {
          'resource': this.$route.params.resource,
          'id': this.$route.params.id
        }), { icon: 'edit', timeout: 6000 })
        this.$router.push('/' + this.$route.params.program + '/' + this.field.resource + '/list/')
      }
    }
  }
}
</script>

<style scoped>

</style>
