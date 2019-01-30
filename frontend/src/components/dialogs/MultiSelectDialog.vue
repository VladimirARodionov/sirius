<template>
  <v-dialog v-model="intDialogVisible" persistent max-width="500">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title> {{getTitle}} </v-card-title>
        <v-alert outline type="error" value="true" v-if="errorMessage">
          {{errorMessage}}
        </v-alert>
      <v-card-text>
        <v-list
          subheader
          two-line
        >
          <!--<v-subheader>Hangout notifications</v-subheader>-->
          <v-list-tile v-for="field_name in data[json.name]" :key="field_name.id">
            <v-list-tile-action>
              <v-checkbox v-model="data['selected'][field_name.id]"></v-checkbox>
            </v-list-tile-action>
            <v-list-tile-content @click="data['selected'][field_name.id] = !(data['selected'][field_name.id])">
              <v-list-tile-title>{{getValue(data, field_name.id)}}</v-list-tile-title>
              <!--<v-list-tile-sub-title>Allow notifications</v-list-tile-sub-title>-->
            </v-list-tile-content>
          </v-list-tile>
        </v-list>

      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="gray darken-1" @click.native="close">{{'Close' | translate}}</v-btn>
        <v-btn color="green darken-1" @click="clicked()">{{'Save' | translate}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { onGetMax, onPostSingle } from '../../api/requests'
export default {
  name: 'MultiSelectDialog',
  data () {
    return {
      data: {
        selected: {}
      },
      errorMessage: ''
    }
  },
  computed: {
    getTitle () {
      if (this.json.text) {
        return this.$t(this.json.text)
      } else {
        return ''
      }
    },
    intDialogVisible: {
      get: function () {
        if (this.dialog) {
          this.getMultiSelectItems()
          this.getCurrentSelectedItems()
        }
        return this.dialog
      }
    }
  },
  methods: {
    clicked () {
      // this.onClicked()
      this.updateSelected()
    },
    close () {
      this.$emit('update:dialog', false)
    },
    getArrayValueById: function (arr, id, valueName) {
      for (const item in arr) {
        if (arr[item].id === id) {
          return arr[item][valueName]
        }
      }
    },
    getValue: function (property, name) {
      return this.getArrayValueById(property[this.json.name], name, this.json.value)
    },
    getItems: function () {
      let arr = []
      if (this.data[this.json.name]) {
        for (const item in this.data[this.json.name]) {
          arr.push(this.getValue(this.data[this.json.name][item]))
        }
      }
      return arr
    },
    getMultiSelectItems: function () {
      onGetMax(this.json.api, this.json.name, this.data)
    },
    getCurrentSelectedItems: function () {
      if (this.currentSelected && this.currentSelected instanceof Array) {
        for (const item in this.currentSelected) {
          if (this.currentSelected[item]) {
            this.data['selected'][this.currentSelected[item]] = true
          }
        }
      }
    },
    updateSelected () {
      this.data.currentObject = { forId: this.forId, selected: this.data.selected }
      onPostSingle(this.json.updateApi, this.data, this.getFunction)
    }
  },
  props: {
    dialog: {
      default: false
    },
    json: Object,
    forId: String,
    forName: String,
    currentSelected: Array,
    getFunction: Function
  }
}
</script>

<style scoped>

</style>
