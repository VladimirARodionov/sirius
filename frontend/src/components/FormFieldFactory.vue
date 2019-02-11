<template>
   <div>
     <router-link
       v-if="field.type === 'menulist'" :id="field.name" class="navbar" active-class="active" :to="field.value">
       {{field.text | translate}}
     </router-link>
     <DataTable
       v-else-if="field.type === 'table'"
       :field="field"
       v-model="value"/>
     <DataTree
       v-else-if="field.type === 'tree'"
       :field="field"
       v-model="value"/>
     <v-layout
       v-else-if="field.type === 'group'"
       row pl-3
     >
      <div v-for="subfield in field.fields" :key="subfield.name">
        <!--<div>{{JSON.stringify(subfield) + ' ' + JSON.stringify(name) + ' ' + value[subfield.name]}}</div>-->
        <FormFieldFactory
          v-model="value"
          :field="subfield"/>
      </div>
     </v-layout>
     <Button
       v-else-if="field.type === 'button'"
       :field="field"
       v-model="value"/>
     <Search
       v-else-if="field.type === 'search'"
       :field="field"
       v-model="value"/>
     <TextField
       v-else-if="field.type === 'text'"
       :field="field"
       v-model="value"/>
     <DateField
       v-else-if="field.type === 'date'"
       :field="field"
       v-model="value"/>
     <SelectField
       v-else-if="field.type === 'select'"
       :field="field"
       v-model="value"/>
     <MultiSelectField
       v-else-if="field.type === 'multi-select'"
       :field="field"
       v-model="value"/>
      <v-card-actions
       v-else-if="field.type === 'actions'">
        <v-spacer></v-spacer>
          <v-layout row p-3>
          <FormFieldFactory v-for="subfield in field.fields" :key="subfield.name"
            v-model="value"
            :field="subfield"/>
            </v-layout>
      </v-card-actions>

   </div>
</template>

<script>
import DataTable from './DataTable'
import DataTree from './DataTree'
import Button from './Button'
import Search from './Search'
import TextField from './TextField'
import DateField from './DateField'
import SelectField from './SelectField'
import MultiSelectField from './MultiSelectField'

export default {
  name: 'FormFieldFactory',
  props: {
    value: {},
    field: {},
    toParent: Function
  },
  components: {
    DataTable,
    DataTree,
    Button,
    Search,
    TextField,
    DateField,
    SelectField,
    MultiSelectField
  },
  data () {
    return {
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
