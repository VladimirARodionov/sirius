<template>
  <div>
    <h1> {{title | translate}} </h1>
    <div class="btn-toolbar justify-content-between mb-3">
        <button class="btn btn-success btn-block" v-roles="['admin_role', 'edit_role']" v-if="select"
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
      <div class="input-group">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
        <span class="input-group-btn">
            <button class="btn btn-success" v-on:click.prevent="getObjects()">{{'Search' | translate}}</button>
        </span>
      </div>
    </div>
    <div class="table-responsive">
      <v-data-table
        :headers="getHeaders()"
        :items="data.objects"
        :loading="data.loading"
        :total-items="data.totalObjects"
        :pagination.sync="pagination"
        :rows-per-page-items="[10, 20, 50, 100]"
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <tr v-on:click="selectObject(props.item)" v-bind:class="isActive(props.item)">
            <td v-for="fieldName in getNames()" :key="fieldName.name">{{ props.item[fieldName.name] }}</td>
          </tr>
        </template>
      </v-data-table>

    </div>
    <!-- Delete Modal -->
    <DeleteDialog :dialog.sync="data.deleteDialog" :message="getDeleteMessage()" :on-clicked="deleteObject"/>
  </div>
</template>

<script>
import router from '../../router'
import DeleteDialog from '../dialogs/DeleteDialog'
import { onGet, onPost, onPut, onDelete } from '../../api/requests'

export default {
  name: 'Directory',
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
      message: null,
      errorMessage: '',
      search_term: '',
      pagination: {},
      errors: []
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getObjects()
      },
      deep: true
    }
  },
  methods: {
    getObjects: function () {
      onGet(this.api, this.data, this.pagination, this.search_term)
    },
    selectObject: function (obj) {
      this.data.currentObject = JSON.parse(JSON.stringify(obj))
      this.data.isSelected = true
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
    getDeleteMessage: function () {
      return this.$t('Delete ' + this.name) + ' #' + this.data.currentObject.id + ' ' + this.data.currentObject.name + ' ?'
    },
    onSelect: function () {
      if (this.data.isSelected && this.data.currentObject.id) {
        // store this.data.currentObject.id in vuex
        console.log('from Directory onSelect ' + this.data.currentObject.id)
        this.$store.commit('setSelectedObject', { name: this.name, api: this.api, id: this.data.currentObject.id })
        this.$router.go(-1)
      }
    },
    goAdd: function () {
      router.push({ name: this.addRouter })
    },
    goEdit: function () {
      if (this.data.currentObject !== '') {
        router.push({ name: this.editRouter, params: { id: this.data.currentObject.id } })
      }
    },
    getHeaders: function () {
      if (this.headers) {
        return this.headers
      } else {
        return this.defaultHeaders
      }
    },
    getNames: function () {
      if (this.names) {
        return this.names
      } else {
        return this.defaultNames
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
    select: Boolean,
    headers: Array,
    names: Array,
    addRouter: String,
    editRouter: String
  }
}
</script>

<style scoped>

</style>
