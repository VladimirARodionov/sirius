<template>
  <div>
     <v-btn
       :id="field.name"
       v-if="(field.action !== 'edit' && field.action !== 'delete') || selectedId"
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
      selectedId: '',
      object: {}
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
        this.$bus.emit('delete', this.selectedId)
      } else if (action === 'save') {
        this.$bus.emit('save', this.selectedId)
      }
    },
    onSelect (data) {
      if (data) {
        this.selectedId = data.id
        this.object = data
      } else {
        this.selectedId = ''
        this.object = {}
      }
    }
  }
}
</script>

<style scoped>

</style>
