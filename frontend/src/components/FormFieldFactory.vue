<template>
   <div>
     <router-link
       v-if="field.type === 'menulist'" :id="field.name" class="navbar" active-class="active" :to="value[field.name]">
       {{field.text | translate}}
     </router-link>
     <DataTable
       v-else-if="field.type === 'table'"
       :field="field"
       v-model="value"/>

     <v-layout
       v-else-if="field.type === 'group'"
     >
      <div v-for="subfield in field.fields" :key="subfield.name">
        <!--<div>{{JSON.stringify(subfield) + ' ' + JSON.stringify(name) + ' ' + value[subfield.name]}}</div>-->
        <FormFieldFactory
          v-model="value"
          :field="subfield" />
      </div>
     </v-layout>
     <Button
       v-else-if="field.type === 'button'"
       :field="field"
       v-model="value"/>
   </div>
</template>

<script>
import DataTable from './DataTable'
import Button from './Button'

export default {
  name: 'FormFieldFactory',
  props: {
    value: {},
    field: {}
  },
  components: {
    DataTable,
    Button
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
