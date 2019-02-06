<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Add unit')" name="addUnit" :errorMessage="data.errorMessage" :on-clicked="addObject" :names="names"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPostSingle } from '../../api/requests'

export default {
  name: 'AddUnit',
  data () {
    return {
      names: [
        { text: 'Name', type: 'input', name: 'name', required: true }
      ],
      data: {
        currentObject: { children: [] },
        loading: false,
        errorMessage: ''
      }
    }
  },
  created: function () {
    if (this.$route.params.id !== 0) {
      this.data.currentObject.parent = this.$route.params.id
    }
  },
  methods: {
    getObject: function () {
      onGetSingle('/api/unit/', 'currentObject', this.data)
    },
    addObject: function () {
      onPostSingle('/api/unit/', this.data, this.getObject)
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
