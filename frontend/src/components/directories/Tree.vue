<template>
  <div>
    <h1> {{title | translate}} </h1>
    <div class="btn-toolbar justify-content-between mb-3">
        <button class="btn btn-success btn-block" v-roles="['admin_role', 'edit_role']" v-if="select === 'true'"
                v-on:click="onSelect()" :disabled="!data.isSelected">{{'Select' | translate}}
        </button>
    </div>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-on:click="goAdd">{{'Add' |
          translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="goEdit">{{'Edit' | translate}}
        </button>
        <button class="btn btn-danger" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="data.deleteDialog = true">{{'Delete' | translate}}
        </button>
      </div>
    </div>
    <div class="table-responsive">
      <v-treeview
        :items="data.objects"
        open-all
        activatable
        :active.sync="active"
      />

    </div>
    <!-- Delete Modal -->
    <DeleteDialog :dialog.sync="data.deleteDialog" :message="getDeleteMessage()" :on-clicked="deleteObject"/>
  </div>
</template>

<script>
import router from '../../router'
import DeleteDialog from '../dialogs/DeleteDialog'
import { onGetAll, onPost, onPut, onDelete } from '../../api/requests'

export default {
  name: 'Tree',
  data () {
    return {
      defaultHeaders: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('Name'), value: 'name' }
      ],
      defaultNames: [
        { name: 'id' },
        { name: 'name' }
      ],
      data: {
        objects: [],
        loading: false,
        totalObjects: 0,
        newObject: {},
        currentObject: {},
        isSelected: false,
        addDialog: false,
        editDialog: false,
        deleteDialog: false,
        addDialogErrorMessage: '',
        ediDialogErrorMessage: '',
        deleteDialogErrorMessage: ''
      },
      active: [],
      message: null,
      errorMessage: '',
      errors: []
    }
  },
  watch: {
    active: 'selectObject'
  },
  mounted () {
    this.getObjects()
  },
  methods: {
    getObjects: function () {
      onGetAll(this.api, 'objects', this.data)
    },
    selectObject: function () {
      if (this.active.length) {
        let selectedObject = this.data.objects.find(obj => obj.id === this.active[0])
        this.data.currentObject = JSON.parse(JSON.stringify(selectedObject))
        this.data.isSelected = true
      } else {
        this.data.currentObject = {}
        this.data.isSelected = false
      }
    },
    isActive: function (obj) {
      return {
        'table-primary': this.data.currentObject.id === obj.id
      }
    },
    addObject: function () {
      onPost(this.api, this.data, this.getObjects)
    },
    updateObject: function () {
      onPut(this.api, this.data, this.getObjects)
    },
    deleteObject: function () {
      onDelete(this.api, this.data, this.getObjects)
    },
    onSelect: function () {
      if (this.data.isSelected && this.data.currentObject.id) {
        // store this.data.currentObject.id in vuex
        this.$store.commit('setSelectedObject', { name: this.name, api: this.api, id: this.data.currentObject.id })
        this.$router.go(-1)
      }
    },
    getDeleteMessage: function (name, object) {
      if (this.data.isSelected && this.deleteMessage) {
        return this.deleteMessage(this.name, this.data.currentObject)
      } else {
        return this.$t('Delete ' + this.name) + ' #' + this.data.currentObject.id + ' ' + this.data.currentObject.name + ' ?'
      }
    },
    goAdd: function () {
      router.push({ name: this.addRouter })
    },
    goEdit: function () {
      if (this.data.currentObject) {
        router.push({ name: this.editRouter, params: { id: this.data.currentObject.id } })
      }
    }
  },
  computed: {
    getNames: function () {
      if (this.names) {
        return this.names
      } else {
        return this.defaultNames
      }
    },
    getHeaders: function () {
      if (this.headers) {
        return this.headers
      } else {
        return this.defaultHeaders
      }
    }
  },
  components: {
    DeleteDialog
  },
  props: {
    title: String,
    name: String,
    api: String,
    select: String,
    headers: Array,
    names: Array,
    addRouter: String,
    editRouter: String,
    deleteMessage: Function
  }
}
</script>

<style scoped>

</style>
