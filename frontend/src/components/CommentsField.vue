<template>
  <div>
    <div v-if="object[field.comment]">
      <div v-for="comment in object[field.comment]" :key="comment.id">
        <v-textarea
          :id="field.name + '_textarea_' + comment.id"
          :label="getLabel(comment)"
          auto-grow
          readonly
          rows="1"
          :value="comment.comment">
        </v-textarea>
      </div>
    </div>
    <v-textarea
      :id="field.name + '_textarea'"
      :label="$t(field.text) + (field.required?' *':'')"
      :error-messages="errorMessage[field.value]"
      counter
      auto-grow
      v-model="data.newObject.comment">
    </v-textarea>
    <v-btn
      :id="field.name + '_add_button'"
      @click="onAdd()">
      {{'Add' | translate}}
    </v-btn>
  </div>
</template>

<script>
import { onGetSingle, onPost } from '../api/requests'

export default {
  name: 'CommentsField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      data: {
        currentObject: {
          id: this.value.currentObject.id
        },
        newObject: {
          user: localStorage.getItem('user_id'),
          contact: this.$route.params.id,
          comment: ''
        }
      },
      object: this.value.currentObject,
      errorMessage: {}
    }
  },
  created () {
    this.$bus.on('error', this.onError)
  },
  beforeDestroy () {
    this.$bus.off('error', this.onError)
  },
  updated () {
    this.$bus.emit('changeObject', this.object)
  },
  watch: {
    value: {
      handler () {
        this.object = this.value.currentObject
        this.errorMessage = this.value.errorMessage
      },
      deep: true
    }
  },
  methods: {
    onError (data) {
      this.errorMessage = data
    },
    onGet () {
      this.data.currentObject.id = this.value.currentObject.id
      onGetSingle(this.field.contact_api, 'currentObject', this.data).then(resp => {
        this.object[this.field.comment] = this.data.currentObject[this.field.comment]
        this.data.newObject.comment = ''
      })
    },
    onAdd () {
      onPost(this.field.api, this.data, this.onGet)
    },
    getLabel (comment) {
      if (comment && comment.user_value && comment.time) {
        return comment.user_value.first_name + ' ' + comment.user_value.last_name + ', ' + comment.time
      } else {
        return ''
      }
    }
  }
}
</script>

<style scoped>

</style>
