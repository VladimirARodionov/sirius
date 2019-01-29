<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add course')" name="addCourse" :errorMessage="data.errorMessage" :on-clicked="addObject"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddCourse',
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
      onGetSingle('/api/course/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/course/', this.data, this.getObject)
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
