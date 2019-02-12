<template>
  <v-layout>
    <v-treeview
      :id="field.name + '_tree'"
      :items="data.objects"
      :loading="data.loading"
      :search="search_term"
      open-all
      activatable
      :active.sync="active"
    >
      <template slot="label" slot-scope="{ item }">
        <div>
          {{ item.name + ' (' + item.user_count + ')'}}
        </div>
      </template>
    </v-treeview>
  </v-layout>
</template>

<script>
import { onGetAll } from '../api/requests'

export default {
  name: 'DataTree',
  data () {
    return {
      data: {
        objects: [],
        loading: false,
        currentObject: { children: [] },
        isSelected: false
      },
      active: [],
      message: null,
      errorMessage: '',
      search_term: '',
      errors: []
    }
  },
  watch: {
    active: 'selectObject'
  },
  created () {
    this.$bus.on('search', this.searchChange)
    this.$bus.on('updateList', this.getObjects)
    this.getObjects()
  },
  beforeDestroy () {
    this.$bus.off('search', this.searchChange)
    this.$bus.off('updateList', this.getObjects)
  },
  methods: {
    getObjects: function () {
      onGetAll(this.field.api, 'objects', this.data)
    },
    selectObject: function (obj) {
      if (this.active.length) {
        let selectedObject = this.getNodeById(this.active[0], this.data.objects)
        this.data.currentObject = JSON.parse(JSON.stringify(selectedObject))
        this.fillChildren()
        this.data.isSelected = true
      } else {
        this.data.currentObject = { children: [] }
        this.data.isSelected = false
      }
      this.$bus.emit('selectObject', this.data.currentObject)
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
    },
    fillChildren () {
      let children = []
      for (const child in this.data.currentObject.children) {
        children.push(this.data.currentObject.children[child].id)
      }
      this.data.currentObject.children = children
    },
    searchChange (data) {
      this.search_term = data
    }
  },
  props: {
    field: {},
    value: {}
  }
}
</script>

<style scoped>

</style>
