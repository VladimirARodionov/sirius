<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Edit address')" :errorMessage="data.errorMessage" :on-clicked="editObject" :names="names" :onSelect="onSelect"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPutSingle } from '../../api/requests'

export default {
  name: 'EditAddress',
  data () {
    return {
      names: [
        { text: 'City', type: 'selector', name: 'city', routerName: 'cities', api: '/api/city/', required: true },
        { text: 'Village', type: 'input', name: 'village' },
        { text: 'Street', type: 'input', name: 'street' },
        { text: 'House', type: 'input', name: 'house' },
        { text: 'Apartment', type: 'input', name: 'apartment' }
      ],
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
      onGetSingle('/api/address/', 'currentObject', this.data)
    },
    editObject: function () {
      onPutSingle('/api/address/', this.data, this.getObject)
    },
    onSelect: function (event) {
      if (event.name === 'city') {
        this.data.currentObject.city = event.id
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
