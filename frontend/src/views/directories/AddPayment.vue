<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add payment')" name="addPayment" :errorMessage="data.errorMessage" :on-clicked="addObject"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddPayment',
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
      onGetSingle('/api/payment/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/payment/', this.data, this.getObject)
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
