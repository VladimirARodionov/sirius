<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add city')" :errorMessage="data.errorMessage" :on-clicked="addObject" :names="names" :onSelect="onSelect"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddCity',
  data () {
    return {
      names: [
        { text: 'Region', type: 'selector', name: 'region', routerName: 'regions', api: '/api/region/', required: true },
        { text: 'Name', type: 'input', name: 'name', required: true }
      ],
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  methods: {
    getObject: function () {
      onGetSingle('/api/city/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/city/', this.data, this.getObject)
    },
    onSelect: function (event) {
      if (event.name === 'region') {
        this.data.currentObject.region = event.id
      }
    }
  },
  components: {
    Menu,
    DirectoryDetail
  }
}
</script>

<style scoped>

</style>
