<template>
  <Menu>

    <Directory title="Cities" name="city" api="/api/city/" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Cities',
  data () {
    return {
      select: false
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
