<template>
  <Menu>
    <Directory title="Competencies" name="competency" api="/api/competency/"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import Directory from './Directory'

export default {
  name: 'Competencies',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
