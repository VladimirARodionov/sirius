<template>
  <Menu>
    <DataForm :resource="resource" action="add"></DataForm>
  </Menu>
</template>

<script>
import DataForm from '../components/DataForm'
import Menu from '../layouts/Menu'
export default {
  name: 'ResourceAdd',
  components: {
    Menu,
    DataForm
  },
  data () {
    return {}
  },
  computed: {
    resource () {
      return this.$route.params.resource
    }
  }
}
</script>

<style scoped>

</style>
