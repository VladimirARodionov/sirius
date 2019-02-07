<template>
  <v-layout row wrap>
    <v-data-table
      :headers="getHeaders"
      :items="data.objects"
      :loading="data.loading"
      :total-items="data.totalObjects"
      :pagination.sync="pagination"
      :rows-per-page-items="[10, 20, 50, 100]"
      class="elevation-1"
    >
      <template slot="items" slot-scope="props">
        <tr v-on:click="selectObject(props.item)" v-bind:class="isActive(props.item)">
          <td v-for="fieldName in getNames" :key="fieldName.name">{{ getTableValue(props.item, fieldName) }}</td>
        </tr>
      </template>
    </v-data-table>

  </v-layout>
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
      search_term: '',
      pagination: {},
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
  methods: {
    getObjects: function () {
      onGet(this.api, this.data, this.pagination, this.search_term)
    },
    selectObject: function (obj) {
      this.data.currentObject = JSON.parse(JSON.stringify(obj))
      this.data.isSelected = true
    },
    isActive: function (obj) {
      return {
        'table-primary': this.data.currentObject.id === obj.id
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
      if (this.names) {
        return this.names
      } else {
        return this.defaultNames
      }
    },
    getHeaders: function () {
      if (this.headers) {
        return this.headers
      } else {
        return this.defaultHeaders
      }
    }
  },
  props: {
    id: {},
    api: String,
    headers: Array,
    names: Array
  }
}
</script>

<style scoped>

</style>
