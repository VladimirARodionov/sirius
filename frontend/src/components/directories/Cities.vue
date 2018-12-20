<template>
  <div>
    <h1>{{'Cities' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-on:click="addDialog = true">{{'Add' | translate}}</button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="isSelected" v-on:click="editDialog = true">{{'Edit' | translate}}</button>
        <button class="btn btn-danger" v-roles="['admin_role', 'edit_role']" v-if="isSelected" v-on:click="deleteDialog = true">{{'Delete' | translate}}</button>
      </div>
      <div class="input-group">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
        <button class="btn btn-success my-2 my-sm-0" v-on:click.prevent="getObjects()">{{'Search' | translate}}</button>
      </div>
    </div>
    <div class="table-responsive">
      <v-data-table
        :headers="headers"
        :items="objects"
        :loading="loading"
        :total-items="totalObjects"
        :pagination.sync="pagination"
        :rows-per-page-items="[10, 20, 50, 100]"
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <tr v-on:click="selectObject(props.item)" v-bind:class="isActive(props.item)">
            <td>{{ props.item.id }}</td>
            <td>{{ props.item.name }}</td>
          </tr>
        </template>
      </v-data-table>

    </div>
    <!-- Add Modal -->
    <v-dialog v-model="addDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Add city' | translate}}</v-card-title>
          <v-form>
            <v-card-text>

              <div class="alert alert-danger" v-if="errorMessage">
                {{errorMessage}}
              </div>
              <div class="form-group">
                <label for="add_name">{{'Name' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="add_name"
                  v-model="newObject.name"
                  required="required" >
              </div>
            </v-card-text>
            <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click="addDialog = false">{{'Close' | translate}}</v-btn>
          <v-btn color="green darken-1" @click="addObject()">{{'Save' | translate}}</v-btn>
        </v-card-actions>
          </v-form>
      </v-card>
    </v-dialog>
    <!-- End of add modal -->
    <!-- Edit Modal -->
    <v-dialog v-model="editDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Edit' | translate}}</v-card-title>
          <v-form>
            <v-card-text>

              <div class="alert alert-danger" v-if="errorMessage">
                {{errorMessage}}
              </div>
              <div class="form-group">
                <label for="edit_name">{{'Name' | translate}}</label>
                <input
                  type="text"
                  class="form-control"
                  id="edit_name"
                  v-model="currentObject.name"
                  required="required" >
              </div>
            </v-card-text>
            <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click="editDialog = false">{{'Close' | translate}}</v-btn>
          <v-btn color="green darken-1" @click="updateObject()">{{'Save' | translate}}</v-btn>
        </v-card-actions>
          </v-form>
      </v-card>
    </v-dialog>
    <!-- End of edit modal -->
    <!-- Delete Modal -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Delete confirm' | translate}}</v-card-title>
        <v-card-text>{{'Delete city' | translate}} #{{currentObject.id}} {{currentObject.name}} ?</v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-1" @click="deleteDialog = false">{{'No' | translate}}</v-btn>
          <v-btn color="red darken-1" @click="deleteObject()">{{'Delete' | translate}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Cities',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('Name'), value: 'name' }
      ],
      objects: [],
      totalObjects: 0,
      loading: false,
      currentObject: {},
      isSelected: false,
      message: null,
      newObject: {'name': null},
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
        this.getObjects()
      },
      deep: true
    }
  },
  methods: {
    getObjects: function () {
      this.loading = true
      let apiUrl = '/api/city/' + '?page=' + this.pagination.page + '&page_size=' + this.pagination.rowsPerPage
      if (this.search_term) {
        apiUrl = apiUrl + '&search=' + this.search_term
      }
      if (this.pagination.sortBy) {
        const direction = this.pagination.descending ? '-' : ''
        apiUrl = apiUrl + '&ordering=' + direction + this.pagination.sortBy
      }
      axios.get(process.env.API_URL + apiUrl)
        .then(resp => {
          this.objects = resp.data.results
          this.totalObjects = resp.data.count
          this.currentObject = {}
          this.isSelected = false
          this.loading = false
        })
        .catch(err => {
          this.loading = false
          console.log(err)
        })
    },
    selectObject: function (obj) {
      this.currentObject = obj
      this.isSelected = true
    },
    isActive: function (obj) {
      return {
        'table-primary': this.currentObject === obj
      }
    },
    addObject: function () {
      this.errorMessage = ''
      axios.post(process.env.API_URL + '/api/edit/city/', this.newObject)
        .then(resp => {
          this.loading = false
          this.addDialog = false
          this.getObjects()
        })
        .catch(err => {
          console.log(err)
          if (err.response && err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              this.errorMessage = errors[value][0]
            }
            console.log(err.response.data)
          }
        })
    },
    updateObject: function () {
      this.errorMessage = ''
      if (this.currentPeople !== '') {
        axios.put(process.env.API_URL + '/api/edit/city/' + this.currentObject.id + '/', this.currentObject)
          .then(resp => {
            this.loading = false
            this.currentObject = resp.data
            this.editDialog = false
            this.getObjects()
          })
          .catch(err => {
            console.log(err)
            if (err.response && err.response.data) {
              var errors = err.response.data
              for (var value in errors) {
                this.errorMessage = errors[value][0]
              }
              console.log(err.response.data)
              this.getObjects()
            }
          })
      }
    },
    deleteObject: function () {
      this.deleteDialog = false
      if (this.currentObject !== '') {
        axios.delete(process.env.API_URL + '/api/edit/city/' + this.currentObject.id + '/')
          .then(resp => {
            this.currentObject = ''
            this.isSelected = false
            this.getObjects()
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
