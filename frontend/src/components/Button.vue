<template>
  <div>
     <v-btn
       :id="field.name"
       :color="field.color"
       :v-roles="field.roles"
       @click="getAction(field.action)">
       {{field.text | translate}}
     </v-btn>

  </div>
</template>

<script>
export default {
  name: 'Button',
  props: {
    value: {},
    field: {}
  },
  methods: {
    getAction (action) {
      if (action === 'back') {
        this.$router.go(-1)
      } else if (action === 'add') {
        // this.$router.push()
      } else if (action === 'edit') {

      } else if (action === 'delete') {

      } else if (action === 'search') {

      }
    }
  }
}
</script>

<style scoped>

</style>
