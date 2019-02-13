<template>
  <DataForm :program="program" resource="report" action="list"></DataForm>
</template>

<script>
import DataForm from '../components/DataForm'

export default {
  name: 'ReportList',
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
