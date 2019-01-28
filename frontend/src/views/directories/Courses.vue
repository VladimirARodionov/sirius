<template>
  <Menu>
    <Directory title="Courses" name="course" api="/api/course/" addRouter="addCourse" editRouter="editCourse" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Courses',
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
