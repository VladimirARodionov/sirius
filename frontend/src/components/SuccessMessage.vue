<template>
  <div>
    <v-alert outline type="success" value="true">
      {{field.text | translate}}
    </v-alert>
  </div>
</template>

<script>
export default {
  name: 'SuccessMessage',
  props: {
    value: {},
    field: {}
  }
}
</script>

<style scoped>

</style>
