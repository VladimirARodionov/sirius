<template>
  <Menu>
    <h1>{{'List of Users' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-on:click="addDialog = true">{{'Add' |
          translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="isSelected"
                v-on:click="goUserDetails()">{{'Details' | translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="isSelected"
                v-on:click="editDialog = true">{{'Edit' | translate}}
        </button>
        <button class="btn btn-danger" v-roles="['admin_role', 'edit_role']" v-if="isSelected"
                v-on:click="deleteDialog = true">{{'Delete' | translate}}
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
        :items="users"
        :loading="loading"
        :total-items="totalUsers"
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
    <AddPeopleDialog :errorMessage="addPeopleDialogErrorMessage" :dialog.sync="addDialog" :newPeople="this.newPeople" :title="this.$t('Add user')" :on-clicked="addPeople"/>
    <!-- Edit People Modal -->
    <EditPeopleDialog :errorMessage="editPeopleDialogErrorMessage" :dialog.sync="editDialog" :currentPeople="this.currentPeople" :title="this.$t('Edit')" :on-clicked="updatePeople"/>
    <!-- Delete People Modal -->
    <DeleteDialog :dialog.sync="deleteDialog" :message="getDeleteMessage()" :on-clicked="deletePeople"/>
  </Menu>
</template>

<script>
import axios from 'axios'
import router from '../router'
import Menu from './layouts/Menu'
import DeleteDialog from './dialogs/DeleteDialog'
import AddPeopleDialog from './dialogs/AddPeopleDialog'
import EditPeopleDialog from './dialogs/EditPeopleDialog'

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
      users: [],
      totalUsers: 0,
      loading: false,
      currentPeople: {},
      isSelected: false,
      message: null,
      newPeople: { 'first_name': null, 'last_name': null, 'email': null },
      editPeopleDialogErrorMessage: '',
      addPeopleDialogErrorMessage: '',
      search_term: '',
      pagination: {},
      deleteDialog: false,
      editDialog: false,
      addDialog: false,
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
      this.loading = true
      let apiUrl = '/api/user/' + '?page=' + this.pagination.page + '&page_size=' + this.pagination.rowsPerPage
      if (this.search_term) {
        apiUrl = apiUrl + '&search=' + this.search_term
      }
      if (this.pagination.sortBy) {
        const direction = this.pagination.descending ? '-' : ''
        apiUrl = apiUrl + '&ordering=' + direction + this.pagination.sortBy
      }
      axios.get(process.env.API_URL + apiUrl)
        .then(resp => {
          this.users = resp.data.results
          this.totalUsers = resp.data.count
          this.currentPeople = {}
          this.isSelected = false
          this.loading = false
        })
        .catch(err => {
          this.loading = false
          console.log(err)
        })
    },
    selectPeople: function (user) {
      this.currentPeople = user
      this.isSelected = true
    },
    isActive: function (user) {
      return {
        'table-primary': this.currentPeople === user
      }
    },
    goUserDetails: function () {
      if (this.currentPeople !== '') {
        router.push({ name: 'peopleDetails', params: { id: this.currentPeople.id } })
      }
    },
    addPeople: function () {
      this.addPeopleDialogErrorMessage = ''
      axios.post(process.env.API_URL + '/api/userdetail/', this.newPeople)
        .then(resp => {
          this.loading = false
          this.addDialog = false
          this.getPeoples()
        })
        .catch(err => {
          if (err.response && err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              if (errors[value] instanceof Array) {
                this.addPeopleDialogErrorMessage = errors[value][0]
              } else {
                this.addPeopleDialogErrorMessage = errors[value]
              }
            }
            console.log(err.response.data)
          }
        })
    },
    updatePeople: function () {
      this.editPeopleDialogErrorMessage = ''
      if (this.currentPeople !== '') {
        axios.put(process.env.API_URL + '/api/userdetail/' + this.currentPeople.id + '/', this.currentPeople)
          .then(resp => {
            this.loading = false
            this.currentPeople = resp.data
            this.editDialog = false
            this.getPeoples()
          })
          .catch(err => {
            console.log(err)
            if (err.response && err.response.data) {
              var errors = err.response.data
              for (var value in errors) {
                if (errors[value] instanceof Array) {
                  this.editPeopleDialogErrorMessage = errors[value][0]
                } else {
                  this.editPeopleDialogErrorMessage = errors[value]
                }
                console.log(err.response.data)
              }
            }
          })
      }
    },
    deletePeople: function () {
      this.deleteDialog = false
      if (this.currentPeople !== '') {
        axios.delete(process.env.API_URL + '/api/userdetail/' + this.currentPeople.id + '/')
          .then(resp => {
            this.currentPeople = ''
            this.isSelected = false
            this.getPeoples()
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    getDeleteMessage: function () {
      return this.$t('Delete user') + ' ' + this.currentPeople.id + ' ' + this.currentPeople.first_name + ' ' + this.currentPeople.last_name + ((this.currentPeople.email) ? '(' + this.currentPeople.email + ') ?' : ' ?')
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
