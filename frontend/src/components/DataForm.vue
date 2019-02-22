<template>
  <Menu :program="program">
    <v-container grid-list-xl fluid>
      <v-card :style="json.style">
        <v-card-title class="headline grey lighten-2" primary-title> {{json.title | translate}} </v-card-title>
        <div v-if="successMessage">
          <v-alert outline type="success" value="true">
            {{successMessage | translate}}
          </v-alert>
        </div>
        <div v-else>
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
        </div>
      </v-card>
      <!-- Delete Modal -->
      <DeleteDialog :dialog.sync="data.deleteDialog" :message="getDeleteMessage()" :on-clicked="deleteObject"/>
    </v-container>
  </Menu>
</template>

<script>
import FormBuilder from './FormBuilder'
import { onGetSingle, onPostSingle, onPutSingle, onDelete } from '../api/requests'
import { flattenJson } from '../api/utils'
import DeleteDialog from './dialogs/DeleteDialog'
import vuetifyToast from 'vuetify-toast'
import Menu from '../layouts/Menu'

export default {
  name: 'DataForm',
  props: {
    resource: {
      type: String,
      required: true
    },
    program: {
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
    Menu,
    FormBuilder,
    DeleteDialog
  },
  data: () => ({
    json: {},
    data: {
      currentObject: {},
      selectedObject: {},
      loading: false,
      errorMessage: '',
      deleteDialog: false,
      deleteDialogErrorMessage: ''
    },
    loaded: false,
    successMessage: ''
  }),
  created () {
    this.fetchData()
    this.$bus.on('changeObject', this.onChangeObject)
    this.$bus.on('saveObject', this.onSave)
    this.$bus.on('saveAppointment', this.onSaveAppointment)
    this.$bus.on('deleteObject', this.onDelete)
    this.$bus.on('selectObject', this.onSelect)
    this.$bus.on('error', this.onError)
  },
  mounted () {
    if (this.json.type === 'edit' || this.json.type === 'edittree' || this.json.type === 'addtree' || this.json.type === 'detail') {
      this.getObject()
    }
  },
  beforeDestroy () {
    this.$bus.off('changeObject', this.onChangeObject)
    this.$bus.off('saveObject', this.onSave)
    this.$bus.off('saveAppointment', this.onSaveAppointment)
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
      const json = require('../assets/' + this.program + '/' + this.resource + this.action + '.json')
      return json
    },
    onChangeObject (data) {
      this.data.currentObject = data
    },
    onSave () {
      if (this.json.type === 'add' || this.json.type === 'addtree') {
        this.addObject()
      } else if (this.json.type === 'edit' || this.json.type === 'edittree' || this.json.type === 'detail') {
        this.updateObject()
      }
    },
    onSaveAppointment () {
      this.addAppointment()
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
      if (this.json.type === 'addtree') {
        if (this.$route.params.id !== '0') {
          this.$set(this.data, 'currentObject', { parent: this.$route.params.id, children: {} })
        }
      } else {
        this.$set(this.data, 'currentObject', { id: this.$route.params.id })
        onGetSingle(this.json.api, 'currentObject', this.data).then(resp => {
          this.getSavedObject()
        })
      }
    },
    getSavedObject () {
      if (this.$store.getters.getSavedState[this.resource] && this.$store.getters.getSavedState[this.resource][this.id]) {
        let savedState = this.$store.getters.getSavedState[this.resource][this.id]
        this.$store.commit('clearSavedState', this.resource)
        this.$set(this.data, 'currentObject', savedState.currentObject)
        vuetifyToast.info(this.$t('ResourceRestored', { 'resource': this.resource, 'id': this.id }), { icon: 'edit', timeout: 6000 })
      }
    },
    addObject: function () {
      if (this.json.type === 'addtree' || this.json.type === 'edittree') {
        this.fillChildren()
      }
      onPostSingle(this.json.api, this.data, this.getObject).then(resp => {
        this.$bus.emit('goBack', {})
      })
    },
    addAppointment: function () {
      let self = this
      onPostSingle(this.json.api, this.data, null).then(resp => {
        self.successMessage = self.json.successMessage
      })
    },
    updateObject: function () {
      if (this.json.type === 'addtree' || this.json.type === 'edittree') {
        this.fillChildren()
      }
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
      return this.$t('Delete ' + (this.json.name ? this.json.name : '')) + ' #' + this.data.currentObject.id + ' ' + this.data.currentObject.name + ' ?'
    },
    fillChildren () {
      let children = []
      if (this.data.currentObject.children) {
        for (const child in this.data.currentObject.children) {
          children.push(this.data.currentObject.children[child].id)
        }
      }
      this.data.currentObject.children = children
    }
  },
  computed: {
    errorMessageText: function () {
      const errors = this.data.errorMessage
      let result = []
      for (const value in errors) {
        let skip = false
        if (errors[value] instanceof Array) {
          const names = flattenJson(this.json.fields) // TODO remove pathname
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
