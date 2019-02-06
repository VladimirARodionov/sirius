<template>
  <div>
    <v-progress-linear v-if="data.loading" height="2" :indeterminate="true"></v-progress-linear>
    <v-card>
    <v-card-title class="headline lighten-2" primary-title> {{title}} </v-card-title>
    <v-form>
      <v-card-text>
        <v-alert outline type="error" value="true" v-if="errorMessageText">
          {{errorMessageText}}
        </v-alert>
        <v-item-group v-for="field_name in names" :key="field_name.name">
          <v-item-group v-if="field_name.type === 'input'">
            <v-text-field
              :id="field_name.name"
              :label="$t(field_name.text) + (field_name.required?' *':'')"
              :error-messages="data.errorMessage[field_name.name]"
               v-model="getObject[field_name.name]">
            </v-text-field>
          </v-item-group>
          <v-item-group v-else-if="field_name.type === 'date'">
            <v-menu
              ref="menu"
              lazy
              :close-on-content-click="false"
              v-model="menu"
              transition="scale-transition"
              offset-y
              full-width
              :nudge-right="40"
              min-width="290px"
            >
              <v-text-field
                :id="field_name.name"
                slot="activator"
                :label="$t(field_name.text) + (field_name.required?' *':'')"
                v-model="getObject[field_name.name]"
                append-icon="event"
                :error-messages="data.errorMessage[field_name.name]"
                readonly
              ></v-text-field>
              <v-date-picker
                ref="picker"
                :first-day-of-week="1"
                v-model="getObject[field_name.name]"
                @change="save"
                locale="ru"
                min="1930-01-01"
                :max="new Date().toISOString().substr(0, 10)"
              ></v-date-picker>
            </v-menu>
          </v-item-group>
          <v-item-group v-else-if="field_name.type === 'selector'">
              <v-text-field
                :label="$t(field_name.text) + (field_name.required?' *':'')"
                readonly
                type="text"
                :id="field_name.name"
                :error-messages="data.errorMessage[field_name.name]"
                v-if="getPeopleValue(data, field_name)"
                append-icon="search"
                @click:append="find(field_name)"
                :value="getPeopleValue(data, field_name)">
              </v-text-field>
              <v-text-field
                :label="$t(field_name.text) + (field_name.required?' *':'')"
                readonly
                type="text"
                :id="field_name.name"
                :error-messages="data.errorMessage[field_name.name]"
                v-else
                append-icon="search"
                @click:append="find(field_name)"
                :value="'Not selected' | translate">
              </v-text-field>
          </v-item-group>
          <v-item-group v-else-if="field_name.type === 'multi-selector'">
            <v-select
              readonly
              :items="getMultiSelectValues(data[field_name.name], field_name)"
              :value="getMultiSelectValues(data[field_name.name], field_name)"
              :label="$t(field_name.text) + (field_name.required?' *':'')"
              :id="field_name.name"
              append-icon="done_all"
              @click:append="changeMultiSelect(field_name)"
              :error-messages="data.errorMessage[field_name.name]"
              multiple
              chips>
            </v-select>
          </v-item-group>
          <v-item-group v-else-if="field_name.type === 'multi-selector-tree'">
            <v-select
              readonly
              :items="getMultiSelectTreeValues(data[field_name.tree_name], field_name)"
              :value="getMultiSelectTreeValues(data[field_name.tree_name], field_name)"
              :label="$t(field_name.text) + (field_name.required?' *':'')"
              :id="field_name.name"
              append-icon="search"
              @click:append="find(field_name)"
              :error-messages="data.errorMessage[field_name.name]"
              multiple
              chips>
            </v-select>
          </v-item-group>
        </v-item-group>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" @click.native="clicked()">{{'Save' | translate}}</v-btn>
        <v-btn color="red darken-1" v-roles="['admin_role', 'edit_role']" @click="changePasswordDialog = true">{{'Change password' | translate}}</v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
    <!-- Change password Modal -->
    <v-dialog v-model="changePasswordDialog" persistent max-width="800">
      <v-card>
        <v-card-title class="headline grey lighten-2" primary-title>{{'Password change' | translate}}</v-card-title>
        <v-form>
          <v-card-text>
            <div container v-if="result">
              <div class="row">
                <div class="col col-lg-6">

                  <div class="alert alert-success" v-if="result.success">
                    <p>{{ 'Password changed successfully' | translate}}</p>
                  </div>
                  <div class="alert alert-danger" v-else-if="result.error">
                    <p>{{ 'Failure' | translate}}</p>
                    <div>{{ result.error }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label for="id_new_password1">{{'New password' | translate}}</label>
              <input
                type="password"
                class="form-control"
                name="new_password1"
                id="id_new_password1"
                v-model="passwords.new_password1"
                required>
            </div>
            <div class="form-group">
              <label for="id_new_password2">{{'Password confirmation' | translate}}</label>
              <input
                type="password"
                class="form-control"
                name="new_password2"
                id="id_new_password2"
                v-model="passwords.new_password2"
                required>
            </div>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" @click="changePasswordDialog = false">{{'Close' | translate}}</v-btn>
            <v-btn color="green darken-1" @click="changePassword()">{{'Change' | translate}}</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <!-- End of change password -->
    <!-- Delete People Modal -->
    <MultiSelectDialog :dialog.sync="multiSelectDialog.positions" :json="multiSelectJson" :forId="'' + $route.params.id" forName="user" :currentSelected="data.currentObject.positions" :getFunction="getPeople"/>
    <MultiSelectDialog :dialog.sync="multiSelectDialog.categories" :json="multiSelectJson" :forId="'' + $route.params.id" forName="user" :currentSelected="data.currentObject.categories" :getFunction="getPeople"/>
  </div>
</template>

<script>
import Vue from 'vue'
import { onGetSingle, onGetAll, onPutSingle, onPostSingle } from '../api/requests'
import axios from 'axios'
import vuetifyToast from 'vuetify-toast'
import MultiSelectDialog from '../components/dialogs/MultiSelectDialog'

export default {
  name: 'UserDetail',
  data () {
    return {
      data: {
        currentObject: {},
        loading: false,
        errorMessage: '',
        currentPeople: {}
      },
      changePasswordDialog: false,
      passwords: { new_password1: '', new_password2: '' },
      result: {},
      menu: false,
      multiSelectDialog: {
        positions: false,
        categories: false
      },
      multiSelectJson: {}
    }
  },
  watch: {
    menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  },
  mounted: function () {
    this.getPeople()
    const names = this.names
    for (const field in names) {
      if (names[field].type === 'multi-selector' && !this.data[names[field].name]) {
        this.getMultiSelectItems(names[field])
      }
      if (names[field].type === 'multi-selector-tree' && !this.data[names[field].tree_name]) {
        this.getMultiSelectTreeItems(names[field])
      }
    }
    if (this.$store.getters.getSelectedObject) {
      const selectedValue = JSON.parse(JSON.stringify(this.$store.getters.getSelectedObject))
      this.$store.commit('clearSelectedObject')
      if (selectedValue.id instanceof Array) {
        // for (const item in selectedValue.id) {
        Vue.set(this.data, selectedValue.name, { id: selectedValue.id })
        // this.getSelectedObject(selectedValue.api, selectedValue.name + '_' + item)
        // }
      } else {
        Vue.set(this.data, selectedValue.name, { id: selectedValue.id })
        this.getSelectedObject(selectedValue.api, selectedValue.name)
      }
    }
  },
  updated: function () {
    const names = this.names
    for (const field in names) {
      if (names[field].type === 'selector' && !this.data[names[field].name] && this.data.currentObject[names[field].name]) {
        Vue.set(this.data, names[field].name, { id: this.data.currentObject[names[field].name] })
        this.getSelectedObject(names[field].api, names[field].name)
      }
      if (names[field].type === 'multi-selector-tree' && !this.data[names[field].name] && this.data.currentObject[names[field].tree_name]) {
        Vue.set(this.data, names[field].name, { id: this.data.currentObject[names[field].tree_name] })
      }
    }
  },
  computed: {
    getObject: function () {
      if (this.$store.getters.getSavedState[this.name]) {
        let savedState = this.$store.getters.getSavedState[this.name]
        this.$store.commit('clearSavedState', this.name)
        return savedState
      } else {
        return this.data.currentObject
      }
    },
    errorMessageText: function () {
      const errors = this.data.errorMessage
      if (!(errors instanceof Array)) {
        return errors
      }
      for (const value in errors) {
        if (errors[value] instanceof Array) {
          const names = this.names
          for (const field in names) {
            if (names[field].name === value) {
              return ''
            }
          }
          return errors[value][0]
        } else {
          return errors[value]
        }
      }
      return ''
    }
  },
  methods: {
    save (date) {
      this.$refs.menu[0].save(date)
    },
    clicked () {
      const names = this.names
      for (const field in names) {
        if (names[field].type === 'selector') {
          if (this.data[names[field].name]) {
            this.onSelect({ name: names[field].name, id: this.data[names[field].name].id })
          }
        }
        if (names[field].type === 'multi-selector') {
          if (this.data[names[field].name]) {
            this.onMultiSelect(names[field].name)
          }
        }
        if (names[field].type === 'multi-selector-tree') {
          if (this.data[names[field].name]) {
            this.onMultiSelectTree({ name: names[field].name, id: this.data[names[field].name].id }, names[field])
          }
        }
      }
      this.updatePeople()
    },
    onSelect: function (event) {
      if (event.name === 'address') {
        this.data.currentObject.address = event.id
      }
    },
    onMultiSelect: function (event) {
      if (event === 'positions') {
        // get current user positions
        // delete all user positions
        // add new user positions
      }
    },
    onMultiSelectTree: function (event, jsonField) {
      const currentObj = this.data.currentObject
      this.data.currentObject = { forId: currentObj.id, selected: this.data[jsonField.name].id }
      onPostSingle(jsonField.updateApi, this.data, this.getPeople)
      this.data.currentObject = currentObj
    },
    getMultiSelectItems: function (name) {
      this.data[name.name] = { id: this.$route.params.id }
      onGetSingle(name.updateApi, name.name, this.data)
    },
    getMultiSelectTreeItems: function (name) {
      onGetAll(name.api, name.tree_name, this.data)
    },
    changeMultiSelect: function (json) {
      this.multiSelectJson = json
      this.multiSelectDialog[json.name] = true
    },
    getSelectedObject (api, name) {
      onGetSingle(api, name, this.data)
    },
    getPeople: function () {
      axios.get(process.env.API_URL + this.api + this.$route.params.id + '/')
        .then(resp => {
          this.data.currentObject = resp.data
          // To update multi-select values
          const names = this.names
          for (const field in names) {
            if (names[field].type === 'multi-selector') {
              this.getMultiSelectItems(names[field])
            }
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    updatePeople: function () {
      onPutSingle(this.api, this.data, this.getPeople)
    },
    changePassword: function () {
      this.data.errorMessage = ''
      axios.post(process.env.API_URL + '/api/people/' + this.$route.params.id + '/password_change', this.passwords)
        .then(resp => {
          vuetifyToast.success(Vue.i18n.translate('Success'), { icon: 'check_circle_outline' })
          if (resp.data.result) {
            this.result = resp.data.result
          }
        })
        .catch(error => {
          vuetifyToast.error(Vue.i18n.translate('Error'), { icon: 'highlight_off' })
          if (error.response) {
            this.data.errorMessage = error.response.data
          } else if (error.request) {
            this.data.errorMessage = error.request
            console.log(error.request)
          } else {
            this.data.errorMessage = error.message
            console.log('Error', error.message)
          }
        })
    },
    find (jsonField) {
      this.$store.commit('setSavedState', { name: this.name, obj: this.object })
      if (jsonField.type === 'multi-selector-tree') {
        this.$store.commit('setSelectedObject', {
          name: jsonField.name,
          api: jsonField.api,
          id: this.data[jsonField.name].id
        })
      }
      this.$router.push({ name: jsonField.routerName, query: { select: 'true' } })
    },
    getPeopleValue: function (property, jsonField) {
      const arr = jsonField.value.split('.')
      if (arr.length === 1) {
        return property[jsonField.value]
      } else {
        var value = property
        if (value instanceof Array) {
          value = value[0]
        }
        for (const item in arr) {
          if (value[arr[item]]) {
            value = value[arr[item]]
          } else {
            return ''
          }
        }
        return value
      }
    },
    getMultiSelectValues (property, jsonField) {
      var result = []
      if (!property) { return result }
      if (property instanceof Array) {
        for (const item in property) {
          const value = this.getMultiSelectValue(property[item], jsonField)
          if (value) {
            result.push(value)
          }
        }
      } else {
        const value = this.getMultiSelectValue(property, jsonField)
        if (value) {
          result.push(value)
        }
      }
      return result
    },
    getMultiSelectValue: function (property, jsonField) {
      const arr = jsonField.multiselect_value.split('.')
      if (arr.length === 1) {
        return property[jsonField.multiselect_value]
      } else {
        var value = property
        if (value instanceof Array) {
          value = value[0]
        }
        for (const item in arr) {
          if (value[arr[item]]) {
            value = value[arr[item]]
          } else {
            return ''
          }
        }
        return value
      }
    },
    getMultiSelectTreeValues (property, jsonField) {
      var result = []
      if (!property) { return result }
      if (!this.data[jsonField.name]) { return result }
      for (const item in this.data[jsonField.name].id) {
        const value = this.getMultiSelectTreeValue(property, this.data[jsonField.name].id[item], jsonField)
        if (value) {
          result.push(value)
        }
      }
      return result
    },
    getMultiSelectTreeValue: function (property, id, jsonField) {
      const node = this.getNodeById(id, property)
      if (node) {
        return node[jsonField.value]
      } else {
        return ''
      }
    },
    getNodeById (id, node) {
      var reduce = [].reduce
      function runner (result, node) {
        if (result || !node) return result
        if (node.id === id) {
          return node
        } else {
          return runner(null, node.children) || reduce.call(Object(node), runner, result)
        }
      }
      return runner(null, node)
    }
  },
  props: {
    title: String,
    api: String,
    names: Array
  },
  components: {
    MultiSelectDialog
  }
}
</script>

<style scoped>

</style>
