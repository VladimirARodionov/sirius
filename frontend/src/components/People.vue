<template>
  <div>
    <h1>{{'List of Users' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" data-toggle="modal" data-target="#addUserModal">{{'Add' | translate}}</button>
        <button class="btn btn-success"  v-if="isSelected" v-on:click="goUserDetails()">{{'Details' | translate}}</button>
        <button class="btn btn-success" v-if="isSelected" data-toggle="modal" data-target="#editUserModal">{{'Edit' | translate}}</button>
        <button class="btn btn-danger" v-if="isSelected" v-on:click="deletePeopleConfirm()">{{'Delete' | translate}}</button>
      </div>
      <div class="input-group">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
        <button class="btn btn-success my-2 my-sm-0" v-on:click.prevent="getPeoples()">{{'Search' | translate}}</button>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="thead-dark">
        <tr>
          <th class="th-sm">#</th>
          <th>{{'First name' | translate}}</th>
          <th>{{'Last name' | translate}}</th>
          <th>{{'Email' | translate}}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="user in users" v-on:click="selectPeople(user)" v-bind:class="isActive(user)">
          <td >{{user.id}}</td>
          <td>{{user.first_name}}</td>
          <td>{{user.last_name}}</td>
          <td>{{user.email}}</td>
        </tr>
        </tbody>
      </table>
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
    <div class="modal fade" id="deleteUserModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">{{'Delete confirm' | translate}}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <form @submit.prevent="deletePeople()">
            <div class="modal-body">
              <div class="alert alert-danger" v-if="errorMessage">
                {{errorMessage}}
              </div>
              <div class="form-group">
                <label>Delete user #{{currentPeople.id}}  {{currentPeople.first_name}} {{currentPeople.last_name}} ({{currentPeople.email}}) ?</label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">{{'No' | translate}}</button>
              <button type="submit" class="btn btn-danger btn-primary">{{'Delete' | translate}}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- End of people modal -->
  </div>
</template>

<script>
import axios from 'axios'
import router from '../router'

export default {
  name: 'People',
  data () {
    return {
      users: [],
      loading: false,
      currentPeople: {},
      isSelected: false,
      message: null,
      newPeople: {'first_name': null, 'last_name': null, 'email': null},
      errorMessage: '',
      search_term: ''
    }
  },
  mounted: function () {
    this.getPeoples()
  },
  methods: {
    getPeoples: function () {
      this.loading = true
      let apiUrl = '/api/user/'
      if (this.search_term !== '' || this.search_term !== null) {
        apiUrl = apiUrl + '?search=' + this.search_term
      }
      axios.get(process.env.API_URL + apiUrl)
        .then(resp => {
          this.users = resp.data
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
          }})
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
            this.loading = false;
            console.log(err)
            if (err.response.data) {
              var errors = err.response.data
              for (var value in errors) {
                this.errorMessage = JSON.stringify(errors[value]).replace(/[\[\]"]+/g, '');
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
      this.loading = true
      $('#deleteUserModal').modal('hide')
      if (this.currentPeople !== '') {
        axios.delete(process.env.API_URL + '/api/userdetail/' + this.currentPeople.id + '/')
          .then(resp => {
            this.loading = false
            this.currentPeople = ''
            this.isSelected = false
            this.getPeoples()
          })
          .catch(err => {
            this.loading = false
            console.log(err)
          })
      }
    }
  }

}
</script>

<style scoped>

</style>
