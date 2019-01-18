<template>
  <Menu>
    <Directory title="Countries" name="country" api="/api/country/"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import Directory from './Directory'

export default {
  name: 'Countries',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
