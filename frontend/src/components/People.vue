<template>
  <div>
    <h1>{{'List of Users' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" data-toggle="modal" data-target="#addUserModal">{{'Add' | translate}}</button>
        <button class="btn btn-success"  v-if="isSelected" v-on:click="goUserDetails()">{{'Details' | translate}}</button>
        <button class="btn btn-success" v-if="isSelected" data-toggle="modal" data-target="#editUserModal">{{'Edit' | translate}}</button>
        <button class="btn btn-danger" v-if="isSelected" v-on:click="deleteDialog = true">{{'Delete' | translate}}</button>
      </div>
      <div class="input-group">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
        <button class="btn btn-success my-2 my-sm-0" v-on:click.prevent="getPeoples()">{{'Search' | translate}}</button>
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
    <!--<div class="loading" v-if="loading===true">Loading&#8230;</div> -->
    <!-- Add People Modal -->
    <div class="modal fade" id="addUserModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">{{'Add user' | translate}}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <form @submit.prevent="addPeople()">
            <div class="modal-body">
              <div class="alert alert-danger" v-if="errorMessage">
                {{errorMessage}}
              </div>
              <div class="form-group">
                <label for="first_name">{{'First name' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="first_name"
                  placeholder="Enter First name"
                  v-model="newPeople.first_name"
                  required="required" >
              </div>
              <div class="form-group">
                <label for="last_name">{{'Last name' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="last_name"
                  placeholder="Enter Last name"
                  v-model="newPeople.last_name"
                  required="required" >
              </div>
              <div class="form-group">
                <label for="email">{{'Email' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="email"
                  placeholder="Enter email"
                  v-model="newPeople.email">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">{{'Close' | translate}}</button>
              <button type="submit" class="btn btn-primary">{{'Save' | translate}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- End of people modal -->
    <!-- Edit People Modal -->
    <div class="modal fade" id="editUserModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">{{'Edit' | translate}}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <form @submit.prevent="updatePeople()">
            <div class="modal-body">
              <div class="alert alert-danger" v-if="errorMessage">
                {{errorMessage}}
              </div>
              <div class="form-group">
                <label for="first_name">{{'First name' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="edit_first_name"
                  placeholder="Enter First name"
                  v-model="currentPeople.first_name"
                  required="required" >
              </div>
              <div class="form-group">
                <label for="last_name">{{'Last name' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="edit_last_name"
                  placeholder="Enter Last name"
                  v-model="currentPeople.last_name"
                  required="required" >
              </div>
              <div class="form-group">
                <label for="email">{{'Email' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="edit_email"
                  placeholder="Enter email"
                  v-model="currentPeople.email">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">{{'Close' | translate}}</button>
              <button type="submit" class="btn btn-primary">{{'Save' | translate}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- End of people modal -->
    <!-- Delete People Modal -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Delete confirm' | translate}}</v-card-title>
        <v-card-text>Delete user #{{currentPeople.id}}  {{currentPeople.first_name}} {{currentPeople.last_name}} ({{currentPeople.email}}) ?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click="deleteDialog = false">{{'No' | translate}}</v-btn>
          <v-btn color="red darken-1" flat @click="deletePeople()">{{'Delete' | translate}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import router from '../router'

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
      newPeople: {'first_name': null, 'last_name': null, 'email': null},
      errorMessage: '',
      search_term: '',
      pagination: {},
      deleteDialog: false
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

  mounted: function () {
    this.getPeoples()
  },
  methods: {
    getPeoples: function () {
      this.loading = true
      let apiUrl = '/api/user/' + '?page=' + this.pagination.page + '&page_size=' + this.pagination.rowsPerPage
      if (this.search_term) {
        apiUrl = apiUrl + '&search=' + this.search_term
      }
      if (this.pagination.sortBy) {
        const direction = this.pagination.descending ? '-' : '';
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
      this.loading = true
      this.errorMessage = ''
      axios.post(process.env.API_URL + '/api/userdetail/', this.newPeople)
        .then(resp => {
          this.loading = false
          $('#addUserModal').modal('hide')
          this.getPeoples()
        })
        .catch(err => {
          this.loading = false
          console.log(err)
          if (err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              this.errorMessage = JSON.stringify(errors[value]).replace(/[\[\]"]+/g, '')
            }
            console.log(err.response.data)
          }
        })
    },
    updatePeople: function () {
      this.loading = true
      this.errorMessage = ''
      if (this.currentPeople !== '') {
        axios.put(process.env.API_URL + '/api/userdetail/' + this.currentPeople.id + '/', this.currentPeople)
          .then(resp => {
            this.loading = false
            this.currentPeople = resp.data
            $('#editUserModal').modal('hide')
            this.getPeoples()
          })
          .catch(err => {
            this.loading = false
            console.log(err)
            if (err.response.data) {
              var errors = err.response.data
              for (var value in errors) {
                this.errorMessage = JSON.stringify(errors[value]).replace(/[\[\]"]+/g, '')
              }
              console.log(err.response.data)
            }
          })
      }
    },
    deletePeopleConfirm: function () {
      $('#deleteUserModal').modal('show')
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
    }
  }

}
</script>

<style scoped>

</style>
