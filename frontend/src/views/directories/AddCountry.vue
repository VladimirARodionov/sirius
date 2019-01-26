<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add country')" name="addCountry" :errorMessage="data.errorMessage" :on-clicked="addObject" :names="names"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddCountry',
  data () {
    return {
      names: [
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
      onGetSingle('/api/country/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/country/', this.data, this.getObject)
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
