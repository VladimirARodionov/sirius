<template>
  <Menu>
    <Directory title="Organizations" name="organization" api="/api/organization/"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import Directory from './Directory'

export default {
  name: 'Organizations',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
