<template>
  <Menu>
    <DataForm :resource="resource" action="detail" :id="id"></DataForm>
  </Menu>
</template>

<script>
import DataForm from '../components/DataForm'
import Menu from '../layouts/Menu'
export default {
  name: 'Resourcedetail',
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
    },
    id () {
      return this.$route.params.id
    }
  }
}
</script>

<style scoped>

</style>
