<template>
  <v-card>
    <v-card-title class="grey lighten-2" primary-title>
      <v-icon size="40">
        {{field.icon}}
      </v-icon>&nbsp;
      <span class="info-box-text">{{field.title | translate}}</span>
    </v-card-title>
    <v-card-text>
     <router-link v-for="object in data.objects" :key="object.id"
       :id="field.name + '_' + object.id"
       class="navbar"
       active-class="active"
       :to="getObjectLink(object)">
       {{getObjectText(object)}}
     </router-link>
    </v-card-text>
  </v-card>
</template>

<script>
import { onGetAll } from '../api/requests'

export default {
  name: 'HotList',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      data: {
        objects: [],
        loading: false
      },
      errorMessage: {}
    }
  },
  created () {
    this.$bus.on('error', this.onError)
  },
  beforeDestroy () {
    this.$bus.off('error', this.onError)
  },
  mounted () {
    this.getItems()
  },
  methods: {
    onError (data) {
      this.errorMessage = data
    },
    getItems () {
      onGetAll(this.field.api, 'objects', this.data)
    },
    getObjectText (object) {
      let text = ''
      if (this.field.show_id) {
        text = text + '(#' + object.id + ')'
      }
      if (this.field.show_name) {
        text = text + ' ' + object.first_name + (object.last_name ? (' ' + object.last_name) : '')
      }
      if (this.field.show_date) {
        text = text + (object.action_date ? (' ' + object.action_date) : '')
      }
      if (this.field.show_time) {
        text = text + (object.action_time ? (' ' + object.action_time) : '')
      }
      if (this.field.show_consultant) {
        text = text + ' ' + this.$t('Consultant') + ':' + (object.consultant ? (object.consultant_value.first_name + ' ' + object.consultant_value.last_name) : this.$t('Not assigned'))
      }
      if (this.field.show_action) {
        text = text + (object.action ? (' ' + object.action) : '')
      }
      return text
    },
    getObjectLink (object) {
      return '/' + this.field.program + '/' + this.field.resource + '/edit/' + object.id
    }
  }
}
</script>

<style scoped>

</style>
