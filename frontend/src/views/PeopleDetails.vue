<template>
  <Menu>
  <v-card>
    <v-card-title class="headline lighten-2" primary-title> {{'User details' | translate}} </v-card-title>
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
                @click:append="find(field_name.routerName)"
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
                @click:append="find(field_name.routerName)"
                :value="'Not selected' | translate">
              </v-text-field>
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
  </Menu>
</template>

<script>
import Vue from 'vue'
import { onGetSingle, onPutSingle } from '../api/requests'
import axios from 'axios'
import Menu from '../layouts/Menu'

export default {
  name: 'PeopleDetails',
  data () {
    return {
      names: [
        { text: 'Last name', type: 'input', name: 'last_name', required: true },
        { text: 'First name', type: 'input', name: 'first_name', required: true },
        { text: 'Middle name', type: 'input', name: 'middle_name' },
        { text: 'Email', type: 'input', name: 'email' },
        { text: 'Mobile', type: 'input', name: 'mobile' },
        { text: 'Birthday', type: 'date', name: 'birthday' },
        { text: 'Address', type: 'selector', name: 'address', routerName: 'addresses', api: '/api/address/', value: 'address.address_city.name' },
        { text: 'Unit', type: 'selector', name: 'unit', routerName: 'units', api: '/api/unit/', value: 'unit.text' }
      ],
      data: {
        currentObject: {},
        loading: false,
        errorMessage: '',
        currentPeople: {}
      },
      changePasswordDialog: false,
      passwords: { new_password1: '', new_password2: '' },
      result: {},
      menu: false
    }
  },
  watch: {
    menu (val) {
      val && this.$nextTick(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  },
  mounted: function () {
    this.getPeople()
    if (this.$store.getters.getSelectedObject) {
      const selectedValue = JSON.parse(JSON.stringify(this.$store.getters.getSelectedObject))
      console.log('from mounted:' + JSON.stringify(selectedValue))
      this.$store.commit('clearSelectedObject')
      Vue.set(this.data, selectedValue.name, { id: selectedValue.id })
      this.getSelectedObject(selectedValue.api, selectedValue.name)
    }
  },
  updated: function () {
    const names = this.names
    for (const field in names) {
      if (names[field].type === 'selector' && !this.data[names[field].name] && this.data.currentObject[names[field].name]) {
        Vue.set(this.data, names[field].name, { id: this.data.currentObject[names[field].name] })
        this.getSelectedObject(names[field].api, names[field].name)
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
            console.log('from clicked:' + names[field].name)
            this.onSelect({ name: names[field].name, id: this.data[names[field].name].id })
          }
        }
      }
      this.updatePeople()
    },
    onSelect: function (event) {
      console.log('from onSelect:' + JSON.stringify(event))
      if (event.name === 'address') {
        this.data.currentObject.address = event.id
      } else if (event.name === 'unit') {
        this.data.currentObject.unit = event.id
      }
    },
    getSelectedObject (api, name) {
      console.log('from getSelectedObject: ' + api + ' ' + name)
      onGetSingle(api, name, this.data)
    },
    getPeople: function () {
      axios.get(process.env.API_URL + '/api/userdetail/' + this.$route.params.id + '/')
        .then(resp => {
          this.data.currentObject = resp.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    updatePeople: function () {
      onPutSingle('/api/userdetail/', this.data, this.getPeople)
    },
    changePassword: function () {
      this.data.errorMessage = ''
      axios.post(process.env.API_URL + '/api/people/' + this.$route.params.id + '/password_change', this.passwords)
        .then(resp => {
          if (resp.data.result) {
            this.result = resp.data.result
          }
        })
        .catch(err => {
          console.log(err)
          if (err.response && err.response.data) {
            var errors = err.response.data
            for (var value in errors) {
              this.data.errorMessage = errors[value][0]
            }
            console.log(err.response.data)
          }
        })
    },
    find (routerName) {
      this.$store.commit('setSavedState', { name: this.name, obj: this.object })
      this.$router.push({ name: routerName, query: { select: 'true' } })
    },
    getPeopleValue: function (property, jsonField) {
      const arr = jsonField.value.split('.')
      if (arr.length === 1) {
        return property[jsonField.name]
      } else {
        var value = property
        for (const item in arr) {
          if (value[arr[item]]) {
            value = value[arr[item]]
          } else {
            return ''
          }
        }
        return value
      }
    }
  },
  components: {
    Menu
  }
}
</script>

<style scoped>

</style>
