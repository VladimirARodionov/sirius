<template>
  <Menu>
    <DirectoryDetail :object="data.currentObject" :title="this.$t('Edit unit')" name="editUnit" :errorMessage="data.errorMessage" :on-clicked="editObject" :names="names" />
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import DirectoryDetail from '../../components/directories/DirectoryDetail'
import { onGetSingle, onPutSingle } from '../../api/requests'

export default {
  name: 'EditUnit',
  data () {
    return {
      names: [
        { text: 'Name', type: 'input', name: 'name', required: true }
      ],
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  created: function () {
    this.data.currentObject.id = this.$route.params.id
    this.getObject()
  },
  methods: {
    getObject: function () {
      onGetSingle('/api/unit/', 'currentObject', this.data)
    },
    editObject: function () {
      this.fillChildren()
      onPutSingle('/api/unit/', this.data, this.getObject)
    },
    fillChildren () {
      let children = []
      for (const child in this.data.currentObject.children) {
        children.push(this.data.currentObject.children[child].id)
      }
      this.data.currentObject.children = children
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
