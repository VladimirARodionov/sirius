<template>
  <Menu>
    <h1>{{'List of Users' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-on:click="data.addDialog = true">{{'Add' |
          translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="goUserDetails()">{{'Details' | translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="data.editDialog = true">{{'Edit' | translate}}
        </button>
        <button class="btn btn-danger" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="data.deleteDialog = true">{{'Delete' | translate}}
        </button>
      </div>
      <div class="input-group">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
        <span class="input-group-btn">
          <button class="btn btn-success" v-on:click.prevent="getPeoples()">{{'Search' | translate}}</button>
        </span>
      </div>
    </div>
    <div class="table-responsive">
      <v-data-table
        :headers="headers"
        :items="data.objects"
        :loading="data.loading"
        :total-items="data.totalObjects"
        :pagination.sync="pagination"
        :rows-per-page-items="[10, 20, 50, 100]"
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <tr v-on:click="selectPeople(props.item)" v-bind:class="isActive(props.item)">
            <td>{{ props.item.id }}</td>
            <td>{{ props.item.first_name }}</td>
            <td>{{ props.item.last_name }}</td>
            <td>{{ props.item.email }}</td>
          </tr>
        </template>
      </v-data-table>

    </div>
    <!-- Add People Modal -->
    <AddPeopleDialog :errorMessage="data.addDialogErrorMessage" :dialog.sync="data.addDialog" :newPeople="data.newObject" :title="this.$t('Add user')" :on-clicked="addPeople"/>
    <!-- Edit People Modal -->
    <EditPeopleDialog :errorMessage="data.editDialogErrorMessage" :dialog.sync="data.editDialog" :currentPeople="data.currentObject" :title="this.$t('Edit')" :on-clicked="updatePeople"/>
    <!-- Delete People Modal -->
    <DeleteDialog :dialog.sync="data.deleteDialog" :message="getDeleteMessage()" :on-clicked="deletePeople"/>
  </Menu>
</template>

<script>
import router from '../router'
import Menu from './layouts/Menu'
import DeleteDialog from './dialogs/DeleteDialog'
import AddPeopleDialog from './dialogs/AddPeopleDialog'
import EditPeopleDialog from './dialogs/EditPeopleDialog'
import { onGet, onPost, onPut, onDelete } from '../api/requests'

export default {
  name: 'People',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('First name'), value: 'first_name' },
        { text: this.$i18n.translate('Last name'), value: 'last_name' },
        { text: this.$i18n.translate('Email'), value: 'email' }
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
        editDialogErrorMessage: '',
        deleteDialogErrorMessage: ''
      },
      message: null,
      search_term: '',
      pagination: {},
      errors: []
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getPeoples()
      },
      deep: true
    }
  },
  methods: {
    getPeoples: function () {
      onGet('/api/user/', this.data, this.pagination, this.search_term)
    },
    selectPeople: function (user) {
      this.data.currentObject = user
      this.data.isSelected = true
    },
    isActive: function (user) {
      return {
        'table-primary': this.data.currentObject === user
      }
    },
    goUserDetails: function () {
      if (this.data.currentPeople !== '') {
        router.push({ name: 'peopleDetails', params: { id: this.data.currentObject.id } })
      }
    },
    addPeople: function () {
      onPost('/api/user/', this.data, this.getPeoples)
    },
    updatePeople: function () {
      onPut('/api/user/', this.data, this.getPeoples)
    },
    deletePeople: function () {
      onDelete('/api/user/', this.data, this.getPeoples)
    },
    getDeleteMessage: function () {
      return this.$t('Delete user') + ' ' + this.data.currentObject.id + ' ' + this.data.currentObject.first_name + ' ' + this.data.currentObject.last_name + ((this.data.currentObject.email) ? '(' + this.data.currentObject.email + ') ?' : ' ?')
    }
  },
  components: {
    DeleteDialog,
    AddPeopleDialog,
    EditPeopleDialog,
    Menu
  }
}
</script>

<style scoped>

</style>
