<template>
  <Menu>
    <Tree title="Units" name="unit" api="/api/unit/" addRouter="addUnit" editRouter="editUnit" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Tree from '../../components/directories/Tree'

export default {
  name: 'Units',
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
    Tree
  }
}
</script>

<style scoped>

</style>
