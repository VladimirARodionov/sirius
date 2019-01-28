<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Edit category')" name="editCategory" :errorMessage="data.errorMessage" :on-clicked="editObject"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPutSingle } from '../../api/requests'

export default {
  name: 'EditCategory',
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
      onGetSingle('/api/category/', 'currentObject', this.data)
    },
    editObject: function () {
      onPutSingle('/api/category/', this.data, this.getObject)
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
