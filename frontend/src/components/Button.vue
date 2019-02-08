<template>
  <div>
     <v-btn
       :id="field.name"
       v-if="field.action === 'add' || field.action === 'back' || selectedId"
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
  data () {
    return {
      selectedId: ''
    }
  },
  created () {
    this.$bus.on('select', this.onSelect)
  },
  beforeDestroy () {
    this.$bus.off('select', this.onSelect)
  },
  methods: {
    getAction (action) {
      if (action === 'back') {
        this.$router.go(-1)
      } else if (action === 'add') {
        this.$router.push('/' + this.$route.params.resource + '/add/' + this.selectedId)
      } else if (action === 'edit') {
        this.$router.push('/' + this.$route.params.resource + '/edit/' + this.selectedId)
      } else if (action === 'delete') {
        this.$router.push('/' + this.$route.params.resource + '/delete/' + this.selectedId)
      } else if (action === 'search') {

      } else if (action === 'save') {

      }
    },
    onSelect (data) {
      if (data) {
        this.selectedId = data.id
      } else {
        this.selectedId = ''
      }
    }
  }
}
</script>

<style scoped>

</style>
