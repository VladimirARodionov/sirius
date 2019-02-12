<template>
  <v-data-table
    :id="field.name"
    :headers="getHeaders"
    :items="data.objects"
    :loading="data.loading"
    :total-items="data.totalObjects"
    :pagination.sync="pagination"
    :rows-per-page-items="[10, 20, 50, 100]"
    class="elevation-1"
  >
    <template slot="headers" slot-scope="props">
      <tr>
        <th
          v-for="header in props.headers"
          :key="header.text"
          :class="['column sortable', pagination.descending ? 'desc' : 'asc', header.value === pagination.sortBy ? 'active' : '']"
          @click="changeSort(header.value)"
        >
          {{ header.text | translate }}
          <v-icon small>arrow_upward</v-icon>
        </th>
      </tr>
    </template>
    <template slot="items" slot-scope="props">
      <tr v-on:click="selectObject(props.item)" v-bind:class="isActive(props.item)">
        <td v-for="fieldName in getNames" :key="fieldName.name">{{ getTableValue(props.item, fieldName) }}</td>
      </tr>
    </template>
  </v-data-table>
</template>

<script>
import { onGet } from '../api/requests'

export default {
  name: 'DataTable',
  data () {
    return {
      defaultHeaders: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('Name'), value: 'name' }
      ],
      defaultNames: [
        { name: 'id' },
        { name: 'name' }
      ],
      data: {
        objects: [],
        loading: false,
        totalObjects: 0,
        newObject: {},
        currentObject: {},
        isSelected: false
      },
      message: null,
      errorMessage: '',
      pagination: {}, // TODO save to vuex on edit add delete detail
      search_term: '', // TODO save to vuex on edit add delete detail?
      errors: []
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getObjects()
      },
      deep: true
    }
  },
  created () {
    this.$bus.on('search', this.searchChange)
    this.$bus.on('updateList', this.getObjects)
  },
  beforeDestroy () {
    this.$bus.off('search', this.searchChange)
    this.$bus.off('updateList', this.getObjects)
  },
  methods: {
    getObjects: function () {
      onGet(this.field.api, this.data, this.pagination, this.search_term).then(resp => {
        if (this.data.currentObject.id) {
          let visible = false
          for (const obj in this.data.objects) {
            if (this.data.objects[obj].id === this.data.currentObject.id) {
              visible = true
              break
            }
          }
          if (!visible) {
            this.data.currentObject = {}
            this.data.isSelected = false
            this.$bus.emit('selectObject', this.data.currentObject)
          }
        }
      })
    },
    selectObject: function (obj) {
      this.data.currentObject = JSON.parse(JSON.stringify(obj))
      this.data.isSelected = true
      this.$bus.emit('selectObject', this.data.currentObject)
    },
    isActive: function (obj) {
      return {
        'table-primary': this.data.currentObject.id === obj.id
      }
    },
    searchChange (data) {
      this.search_term = data
      this.getObjects()
    },
    changeSort (column) {
      if (this.pagination.sortBy === column) {
        this.pagination.descending = !this.pagination.descending
      } else {
        this.pagination.sortBy = column
        this.pagination.descending = false
      }
    },
    getTableValue: function (property, jsonField) {
      const arr = jsonField.name.split('.')
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
  computed: {
    getNames: function () {
      if (this.field.names) {
        return this.field.names
      } else {
        return this.defaultNames
      }
    },
    getHeaders: function () {
      if (this.field.headers) {
        return this.field.headers
      } else {
        return this.defaultHeaders
      }
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
