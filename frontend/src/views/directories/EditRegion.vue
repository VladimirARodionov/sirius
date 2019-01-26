<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Edit region')" name="editRegion" :errorMessage="data.errorMessage" :on-clicked="editObject" :names="names" :onSelect="onSelect"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPutSingle } from '../../api/requests'

export default {
  name: 'EditRegion',
  data () {
    return {
      names: [
        { text: 'Country', type: 'selector', name: 'country', routerName: 'countries', api: '/api/country/', required: true },
        { text: 'Name', type: 'input', name: 'name', required: true }
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
      onGetSingle('/api/region/', 'currentObject', this.data)
    },
    editObject: function () {
      onPutSingle('/api/region/', this.data, this.getObject)
    },
    onSelect: function (event) {
      if (event.name === 'country') {
        this.data.currentObject.country = event.id
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
