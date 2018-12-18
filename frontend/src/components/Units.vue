<template>
  <div>
    <h1>{{'Units' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-on:click="addDialog = true">{{'Add' | translate}}</button>
        <button class="btn btn-success" v-if="isSelected" v-on:click="editDialog = true">{{'Edit' | translate}}</button>
        <button class="btn btn-danger" v-if="isSelected" v-on:click="deleteDialog = true">{{'Delete' | translate}}</button>
      </div>
    </div>
    <v-treeview :items="objects"></v-treeview>

        <!-- Add People Modal -->
    <v-dialog v-model="addDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Add organization' | translate}}</v-card-title>
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
    <!-- End of people modal -->
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
    <!-- End of people modal -->
    <!-- Delete People Modal -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Delete confirm' | translate}}</v-card-title>
        <v-card-text>{{'Delete organization' | translate}} #{{currentObject.id}} {{currentObject.name}} ?</v-card-text>
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
  name: 'Units',
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
      newObject: {'name': null, 'organization_id': 1},
      errorMessage: '',
      search_term: '',
      pagination: {},
      deleteDialog: false,
      editDialog: false,
      addDialog: false,
      errors: []
    }
  },
  mounted: function () {
    this.getObjects()
  },
  methods: {
    getObjects: function () {
      this.loading = true
      axios.get(process.env.API_URL + '/api/unit/')
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
      axios.post(process.env.API_URL + '/api/add/unit/', this.newObject)
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
        axios.put(process.env.API_URL + '/api/unit/' + this.currentObject.id + '/', this.currentObject)
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
              this.getPeoples()
            }
          })
      }
    },
    deleteObject: function () {
      this.deleteDialog = false
      if (this.currentObject !== '') {
        axios.delete(process.env.API_URL + '/api/unit/' + this.currentObject.id + '/')
          .then(resp => {
            this.currentObject = ''
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
