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
      v-model="currentObject">
    </v-textarea>
    <v-btn
      :id="field.name + '_add_button'"
      @click="onAdd()">
      {{'Add' | translate}}
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'CommentsField',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      object: this.value.currentObject,
      errorMessage: {},
      currentObject: ''
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
    onAdd () {

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
