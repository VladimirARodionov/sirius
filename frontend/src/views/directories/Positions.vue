<template>
  <Menu>
    <Directory title="Positions" name="position" api="/api/position/"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Positions',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
