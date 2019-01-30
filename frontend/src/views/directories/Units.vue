<template>
  <Menu>
    <h1>{{'Units' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
        <button class="btn btn-success btn-block" v-roles="['admin_role', 'edit_role']" v-if="select === 'true'"
                v-on:click="onSelect()" :disabled="!isSelected">{{'Select' | translate}}
        </button>
    </div>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-on:click="addDialog = true">{{'Add' |
          translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="isSelected"
                v-on:click="editDialog = true">{{'Edit' | translate}}
        </button>
        <button class="btn btn-danger" v-roles="['admin_role', 'edit_role']" v-if="isSelected"
                v-on:click="deleteDialog = true">{{'Delete' | translate}}
        </button>
      </div>
    </div>
    <div id="tree"></div>

    <!-- Add People Modal -->
    <v-dialog v-model="addDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Add unit' | translate}}</v-card-title>
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
                v-model="newObject.text"
                required="required">
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
                v-model="currentObject.text"
                required="required">
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
    <!-- Delete Modal -->
    <DeleteDialog :dialog.sync="deleteDialog" :message="getDeleteMessage()" :on-clicked="deleteObject"/>
  </Menu>
</template>

<script>
import axios from 'axios'
import Menu from '../../layouts/Menu'
import DeleteDialog from '../../components/dialogs/DeleteDialog'

export default {
  name: 'Units',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('Name'), value: 'name' }
      ],
      objects: [],
      loading: false,
      currentObject: {},
      isSelected: false,
      message: null,
      newObject: { 'text': null, parent: null },
      errorMessage: '',
      search_term: '',
      pagination: {},
      deleteDialog: false,
      editDialog: false,
      addDialog: false,
      errors: [],
      select: 'false'
    }
  },
  mounted: function () {
    this.getObjects()
  },
  created () {
    if (this.$route.query && this.$route.query.select) {
      this.select = this.$route.query.select
    }
  },
  methods: {
    getObjects: function () {
      this.loading = true
      var self = this
      axios.get(process.env.API_URL + '/api/unit/')
        .then(resp => {
          self.objects = resp.data
          window.$('#tree').treeview({ data: self.objects, levels: 5 }).on({
            'nodeSelected': function (event, data) {
              self.selectObject(data)
            }
          }).on({
            'nodeUnselected': function (event, data) {
              self.currentObject = {}
              self.isSelected = false
            }
          })
          window.$('#tree').treeview('expandAll', {})
          self.currentObject = {}
          self.isSelected = false
          self.loading = false
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
      if (this.currentObject) {
        this.newObject.parent = this.currentObject.id
      }
      axios.post(process.env.API_URL + '/api/unit/', this.newObject)
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
              this.getObjects()
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
            this.getObjects()
          })
      }
    },
    onSelect: function () {
      if (this.isSelected && this.currentObject.id) {
        // store this.data.currentObject.id in vuex
        this.$store.commit('setSelectedObject', { name: 'unit', api: '/api/unit/', id: this.currentObject.id })
        this.$router.go(-1)
      }
    },
    getDeleteMessage: function () {
      return this.$t('Delete unit') + ' #' + this.currentObject.id + ' ' + this.currentObject.text + ' ?'
    }
  },
  components: {
    Menu,
    DeleteDialog
  }
}
</script>

<style scoped>

</style>
