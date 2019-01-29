<template>
  <Menu>
    <Directory title="Organizations" name="organization" api="/api/organization/" addRouter="addOrganization" editRouter="editOrganization" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Organizations',
  data () {
    return {
      select: 'false'
    }
  },
  created () {
    if (this.$route.query && this.$route.query.select) {
      this.select = this.$route.query.select
    }
  },
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
