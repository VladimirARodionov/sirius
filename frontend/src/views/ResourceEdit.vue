<template>
  <DataForm :program="program" :resource="resource" action="edit" :id="id"></DataForm>
</template>

<script>
import DataForm from '../components/DataForm'
export default {
  name: 'ResourceEdit',
  components: {
    DataForm
  },
  data () {
    return {}
  },
  computed: {
    resource () {
      return this.$route.params.resource
    },
    program () {
      return this.$route.params.program
    },
    id () {
      return this.$route.params.id
    }
  }
}
</script>

<style scoped>

</style>
