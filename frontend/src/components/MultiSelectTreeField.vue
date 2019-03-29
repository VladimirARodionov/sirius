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
    item-value="id"
    multiple
    :search-input.sync="search_term"
    :loading="data.loading"
    :append-icon="field.hide_edit?'':'edit'"
    @click:append="goList()"
  >
    <template slot="item" slot-scope="data">
      <div>
        {{data.item[field.item_text] + ' (' + data.item.user_count + ')'}}
      </div>
    </template>

  </v-autocomplete>
</template>

<script>
import { onGetAll } from '../api/requests'
import { flattenTree } from '../api/utils'
import vuetifyToast from 'vuetify-toast'

export default {
  name: 'MultiSelectTreeField',
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
        rowsPerPage: 100 // TODO check select with pagination enabled
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
    }
  },
  methods: {
    onError (data) {
      this.errorMessage = data
    },
    getItems () {
      onGetAll(this.field.api, 'objects', this.data).then(resp => {
        this.data.objects = flattenTree(this.data.objects)
      })
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
