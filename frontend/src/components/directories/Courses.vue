<template>
  <Menu>
    <Directory title="Courses" name="course" api="/api/course/"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import Directory from './Directory'

export default {
  name: 'Courses',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
