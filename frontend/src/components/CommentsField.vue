<template>
  <div>
    <div v-if="object[field.value]">
      <div v-for="comment in object[field.value][field.comment]" :key="comment.id">
        <v-textarea
          :id="field.name + '_textarea_' + comment.id"
          :label="getLabel(comment)"
          auto-grow
          readonly
          :value="comment">
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
import { onPost, onGetAll } from '../api/requests'

export default {
  name: 'CommentsField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      data: {
        objects: {},
        newObject: {
          user: 1,
          contact: 1,
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
  mounted () {
    this.getItems()
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
    onAdd () {
      onPost(this.field.api, this.data, null).then(resp => {
        this.getItems()
      })
    },
    getItems () {
      onGetAll(this.field.comment_api, 'objects', this.data)
    },
    getLabel (comment) {
      if (comment && comment.user && comment.time) {
        return comment.user.first_name + ' ' + comment.user.last_name + ', ' + comment.time
      } else {
        return ''
      }
    }
  }
}
</script>

<style scoped>

</style>
