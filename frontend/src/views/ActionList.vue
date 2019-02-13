<template>
  <DataForm :program="program" resource="action" action="list"></DataForm>
</template>

<script>
import DataForm from '../components/DataForm'
export default {
  name: 'ActionList',
  components: {
    DataForm
  },
  computed: {
    program () {
      return this.$route.params.program
    }
  }
}
</script>

<style scoped>

</style>
