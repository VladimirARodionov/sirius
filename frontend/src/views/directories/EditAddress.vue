<template>
  <Menu>
    <AddressDetail :object="data.currentObject" :title="this.$t('Edit address')" :errorMessage="data.errorMessage" :on-clicked="editObject" @onSelectCity="selectCity"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import AddressDetail from '../../components/AddressDetail'
import { onGetSingle, onPutSingle } from '../../api/requests'

export default {
  name: 'EditAddress',
  data () {
    return {
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  mounted: function () {
    this.data.currentObject.id = this.$route.params.id
    this.getObject()
  },
  methods: {
    getObject: function () {
      onGetSingle('/api/address/', this.data)
    },
    editObject: function () {
      onPutSingle('/api/address/', this.data, this.getObject)
    },
    selectCity: function (event) {
      this.data.currentObject.city = event
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
