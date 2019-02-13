<template>
  <DataForm :program="program" :resource="resource" action="add"></DataForm>
</template>

<script>
import DataForm from '../components/DataForm'
export default {
  name: 'ResourceAdd',
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
    }
  }
}
</script>

<style scoped>

</style>
