<template>
  <Menu>
    <AddressDetail :object="data.currentObject" :title="this.$t('Add address')" :errorMessage="data.errorMessage" :on-clicked="addObject"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import AddressDetail from '../../components/AddressDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddAddress',
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
      onGetSingle('/api/address/', this.data)
    },
    addObject: function () {
      onPostSingle('/api/address/', this.data, this.getObject)
    }
  },
  components: {
    Menu,
    AddressDetail
  }
}
</script>

<style scoped>

</style>
