<template>
  <Menu>
    <Directory title="Regions" name="region" api="/api/region/"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Regions',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
