<template>
   <div>
     <router-link
       v-if="field.type === 'menulist'" :id="id" class="navbar" active-class="active" :to="value[field.name]">
       {{text | translate}}
     </router-link>
     <DataTable
       v-else-if="field.type === 'table'"
       :id="id"
       :api="field.api"
       :headers="field.headers"
       :names="field.names"
     >
     </DataTable>
     <v-layout
       v-else-if="field.type === 'group'"
       row
       wrap
     >
      <div v-for="subfield in field.fields" :key="subfield.name">
        <!--<div>{{JSON.stringify(subfield) + ' ' + JSON.stringify(name) + ' ' + value[subfield.name]}}</div>-->
        <FormFieldFactory v-model="value[subfield.name]" :id="getFieldId(subfield.name)"
        :name="subfield.name" :text="subfield.text" :field="subfield" :key="id + '_' +subfield.name" />
      </div>
     </v-layout>
     <v-btn
       v-else-if="field.type === 'button'"
       :color="field.color"
       @click="getAction(field.action)">
       {{field.text | translate}}
     </v-btn>
   </div>
</template>

<script>
import DataTable from './DataTable'

export default {
  name: 'FormFieldFactory',
  props: {
    id: {
      required: true
    },
    parent: {},
    value: {},
    field: {},
    state: {},
    name: {},
    text: {}
  },
  components: {
    DataTable
  },
  methods: {
    getFieldId (name) {
      return `input_${name}`
    },
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
