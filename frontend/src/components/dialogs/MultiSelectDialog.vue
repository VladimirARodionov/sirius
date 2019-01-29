<template>
  <v-dialog v-model="dialog" persistent max-width="500">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title> {{json.text}} </v-card-title>
        <v-alert outline type="error" value="true" v-if="errorMessage">
          {{errorMessage}}
        </v-alert>
      <v-card-text>
        <v-list
          subheader
          two-line
        >
          <v-subheader>Hangout notifications</v-subheader>

          <v-list-tile @click="">
            <v-list-tile-action>
              <v-checkbox v-model="notifications"></v-checkbox>
            </v-list-tile-action>

            <v-list-tile-content @click="notifications = !notifications">
              <v-list-tile-title>Notifications</v-list-tile-title>
              <v-list-tile-sub-title>Allow notifications</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile @click="">
            <v-list-tile-action>
              <v-checkbox v-model="sound"></v-checkbox>
            </v-list-tile-action>

            <v-list-tile-content @click="sound = !sound">
              <v-list-tile-title>Sound</v-list-tile-title>
              <v-list-tile-sub-title>Hangouts message</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile @click="">
            <v-list-tile-action>
              <v-checkbox v-model="video"></v-checkbox>
            </v-list-tile-action>

            <v-list-tile-content @click="video = !video">
              <v-list-tile-title>Video sounds</v-list-tile-title>
              <v-list-tile-sub-title>Hangouts video call</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile @click="">
            <v-list-tile-action>
              <v-checkbox v-model="invites"></v-checkbox>
            </v-list-tile-action>

            <v-list-tile-content @click="invites = !invites">
              <v-list-tile-title>Invites</v-list-tile-title>
              <v-list-tile-sub-title>Notify when receiving invites</v-list-tile-sub-title>
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
import { onGetMax } from '../../api/requests'
export default {
  name: 'MultiSelectDialog',
  data () {
    return {
      data: {},
      errorMessage: ''
    }
  },
  methods: {
    clicked () {
      // this.onClicked()
    },
    close () {
      this.$emit('update:dialog', false)
    },
    getValue: function (property) {
      const arr = this.json.value.split('.')
      if (arr.length === 1) {
        return property[this.json.value]
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
    }
  },
  props: {
    dialog: {
      default: false
    },
    json: Object
  }
}
</script>

<style scoped>

</style>
