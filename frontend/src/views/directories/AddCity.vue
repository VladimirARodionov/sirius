<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add city')" :errorMessage="data.errorMessage" :on-clicked="addObject" :names="names" @onSelect_region="selectRegion"/>
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
        { text: 'Name', type: 'input', name: 'name', required: true },
        { text: 'Region', type: 'selector', name: 'region', routerName: 'regions', api: '/api/region/', required: true }
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
    selectRegion: function (event) {
      console.log('from addCity ' + JSON.stringify(event))
      this.data.currentObject.region = event
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
