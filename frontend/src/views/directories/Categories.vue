<template>
  <Menu>
    <Directory title="Categories" name="category" api="/api/category/"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Categories',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
