<template>
  <DataForm :program="program" :resource="resource" action="report"></DataForm>
</template>

<script>
import DataForm from '../components/DataForm'

export default {
  name: 'Report',
  components: {
    DataForm
  },
  computed: {
    resource () {
      return this.$route.params.resource
    },
    program () {
      return this.$route.params.program
    }
  }
}
</script>

<style scoped>

</style>
