<template>
  <Menu>
    <Tree title="Faculties" name="faculty" api="/api/faculty/" addRouter="addFaculty" editRouter="editFaculty" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Tree from '../../components/directories/Tree'

export default {
  name: 'Faculties',
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
