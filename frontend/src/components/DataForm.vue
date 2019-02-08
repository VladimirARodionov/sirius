<template>
  <div :style="json.style">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title> {{json.title | translate}} </v-card-title>
        <v-alert outline type="error" value="true" v-if="errorMessageText">
          {{errorMessageText}}
        </v-alert>
      <v-card-text>
        <FormBuilder
          v-if="loaded"
          :resource="resource"
          :id="id"
          :json="json"
          v-model="data"/>
      </v-card-text>
    </v-card>
    <!-- Delete Modal -->
    <DeleteDialog :dialog.sync="data.deleteDialog" :message="getDeleteMessage()" :on-clicked="deleteObject"/>
  </div>
</template>

<script>
import FormBuilder from './FormBuilder'
import { onGetSingle, onPostSingle, onPutSingle, onDelete } from '../api/requests'
import DeleteDialog from './dialogs/DeleteDialog'

export default {
  name: 'DataForm',
  props: {
    resource: {
      type: String,
      required: true
    },
    action: {
      type: String,
      required: true
    },
    id: {
      default: ''
    }
  },
  components: {
    FormBuilder,
    DeleteDialog
  },
  data: () => ({
    json: {},
    data: {
      currentObject: {},
      loading: false,
      errorMessage: '',
      deleteDialog: false,
      deleteDialogErrorMessage: ''
    },
    loaded: false
  }),
  created () {
    this.fetchData()
    this.$bus.on('changeObject', this.onChangeObject)
    this.$bus.on('saveObject', this.onSave)
    this.$bus.on('deleteObject', this.onDelete)
    this.$bus.on('selectObject', this.onSelect)
    this.$bus.on('error', this.onError)
    if (this.json.type === 'edit') {
      this.getObject()
    }
  },
  beforeDestroy () {
    this.$bus.off('changeObject', this.onChangeObject)
    this.$bus.off('saveObject', this.onSave)
    this.$bus.off('deleteObject', this.onDelete)
    this.$bus.off('selectObject', this.onSelect)
    this.$bus.off('error', this.onError)
  },
  methods: {
    fetchData () {
      this.loaded = false
      this.json = this.getJson()
      this.loaded = true
    },
    getJson () {
      const json = require('./' + this.resource + this.action + '.json')
      return json
    },
    onChangeObject (data) {
      this.data.currentObject = data
    },
    onSave () {
      if (this.json.type === 'add') {
        this.addObject()
      } else if (this.json.type === 'edit') {
        this.updateObject()
      }
    },
    onDelete () {
      if (this.data.currentObject.id) {
        this.data.deleteDialog = true
      }
    },
    onSelect (data) {
      if (data) {
        this.data.currentObject = data
      } else {
        this.data.currentObject = {}
      }
    },
    onError (data) {
      this.data.errorMessage = data
    },
    getObject () {
      this.$set(this.data, 'currentObject', { id: this.$route.params.id })
      onGetSingle(this.json.api, 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle(this.json.api, this.data, this.getObject).then(resp => {
        this.$bus.emit('goBack', {})
      })
    },
    updateObject: function () {
      onPutSingle(this.json.api, this.data, this.getObject).then(resp => {
        this.$bus.emit('goBack', {})
      })
    },
    deleteObject: function () {
      onDelete(this.json.api, this.data, this.getObject).then(resp => {
        this.$bus.emit('updateList', {})
      })
    },
    getDeleteMessage: function () {
      return this.$t('Delete ' + this.json.name ? this.json.name : '') + ' #' + this.data.currentObject.id + ' ' + this.data.currentObject.name + ' ?'
    }
  },
  computed: {
    errorMessageText: function () {
      const errors = this.data.errorMessage
      let result = []
      let skip = false
      for (const value in errors) {
        if (errors[value] instanceof Array) {
          const names = this.json.fields
          for (const field in names) {
            if (names[field].value === value) {
              skip = true
            }
          }
          if (!skip) {
            result.push(value + ': ' + errors[value][0])
            skip = false
          }
        } else {
          result.push(errors[value])
        }
      }
      if (result.length) {
        return JSON.stringify(result)
      } else {
        return ''
      }
    }
  }
}
</script>

<style scoped>

</style>
