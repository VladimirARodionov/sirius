<template>
  <Menu>
    <Directory title="Cities" name="city" api="/api/city/"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import Directory from './Directory'

export default {
  name: 'Cities',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
