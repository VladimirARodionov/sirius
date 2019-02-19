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
       row p-3
     >
      <v-item-group multiple v-for="subfield in field.fields" :key="subfield.name">
        <FormFieldFactory
          v-model="value"
          :field="subfield"/>
      </v-item-group>
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
     <MultiSelectTreeField
       v-else-if="field.type === 'multi-select-tree'"
       :field="field"
       v-model="value"/>
     <MenuSelectField
       v-else-if="field.type === 'menuselect'"
       :field="field"
       v-model="value"/>
     <Stepper
       v-else-if="field.type === 'stepper'"
       :field="field"
       v-model="value">
     </Stepper>
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
import MultiSelectTreeField from './MultiSelectTreeField'
import MenuSelectField from './MenuSelectField'
import Stepper from './Stepper'

export default {
  name: 'FormFieldFactory',
  props: {
    value: {},
    field: {}
  },
  components: {
    DataTable,
    DataTree,
    Button,
    Search,
    TextField,
    DateField,
    SelectField,
    MultiSelectField,
    MultiSelectTreeField,
    MenuSelectField,
    Stepper
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
