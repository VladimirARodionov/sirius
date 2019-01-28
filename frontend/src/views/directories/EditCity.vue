<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Edit city')" name="editCity" :errorMessage="data.errorMessage" :on-clicked="editObject" :names="names" :onUpdate="onUpdate" :onSelect="onSelect"/>
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
        { text: 'Region', type: 'selector', name: 'region', routerName: 'regions', api: '/api/region/', required: true },
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
      onGetSingle('/api/city/', 'currentObject', this.data)
    },
    editObject: function () {
      onPutSingle('/api/city/', this.data, this.getObject)
    },
    onSelect: function (event) {
      if (event.name === 'region') {
        this.data.currentObject.region = event.id
      }
    },
    onUpdate: function (event) {
      this.data.currentObject = JSON.parse(JSON.stringify(event))
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
