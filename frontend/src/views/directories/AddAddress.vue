<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add address')" name="addAddress" :errorMessage="data.errorMessage" :on-clicked="addObject" :names="names" :onSelect="onSelect"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddAddress',
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
  methods: {
    getObject: function () {
      onGetSingle('/api/address/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/address/', this.data, this.getObject)
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
