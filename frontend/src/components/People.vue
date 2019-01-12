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
    <AddPeopleDialog ref="addPeopleDialog" :dialog.sync="addDialog" :newPeople="this.newPeople" :title="this.$t('Add user')" :on-clicked="addPeople"/>
    <!-- Edit People Modal -->
    <v-dialog v-model="editDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Edit' | translate}}</v-card-title>
        <v-form>
          <v-card-text>

            <div class="alert alert-danger" v-if="errorMessage">
              {{errorMessage}}
            </div>
            <div class="form-group">
              <label for="edit_first_name">{{'First name' | translate}}</label>
              <input
                type="text"
                class="form-control"
                id="edit_first_name"
                v-model="currentPeople.first_name"
                required="required">
            </div>
            <div class="form-group">
              <label for="edit_last_name">{{'Last name' | translate}}</label>
              <input
                type="text"
                class="form-control"
                id="edit_last_name"
                v-model="currentPeople.last_name"
                required="required">
            </div>
            <div class="form-group">
              <label for="edit_email">{{'Email' | translate}}</label>
              <input
                type="text"
                class="form-control"
                id="edit_email"
                v-model="currentPeople.email">
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" @click="editDialog = false">{{'Close' | translate}}</v-btn>
            <v-btn color="green darken-1" @click="updatePeople()">{{'Save' | translate}}</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <!-- End of people modal -->
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
      errorMessage: '',
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
      this.errorMessage = ''
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
                this.$refs.addPeopleDialog.errorMessage = errors[value][0]
              } else {
                this.$refs.addPeopleDialog.errorMessage = errors[value]
              }
            }
            console.log(err.response.data)
          }
        })
    },
    updatePeople: function () {
      this.errorMessage = ''
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
                this.errorMessage = errors[value][0]
              }
              console.log(err.response.data)
              this.getPeoples()
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
    Menu
  }
}
</script>

<style scoped>

</style>
