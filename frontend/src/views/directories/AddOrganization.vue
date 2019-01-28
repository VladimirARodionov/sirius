<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add organization')" name="addOrganization" :errorMessage="data.errorMessage" :on-clicked="addObject"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddOrganization',
  data () {
    return {
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  methods: {
    getObject: function () {
      onGetSingle('/api/organization/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/organization/', this.data, this.getObject)
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
