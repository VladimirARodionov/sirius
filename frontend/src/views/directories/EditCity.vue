<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Edit city')" :errorMessage="data.errorMessage" :on-clicked="editObject" :names="names" @onSelect_region="selectRegion"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPutSingle } from '../../api/requests'

export default {
  name: 'EditCity',
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
    editObject: function () {
      onPutSingle('/api/city/', this.data, this.getObject)
    },
    selectRegion: function (event) {
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
