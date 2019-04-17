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
     <TextAreaField
       v-else-if="field.type === 'textarea'"
       :field="field"
       v-model="value"/>
     <BirthdayField
       v-else-if="field.type === 'birthday'"
       :field="field"
       v-model="value"/>
     <AppointmentDateField
       v-else-if="field.type === 'appointmentdate'"
       :field="field"
       v-model="value"/>
     <BeginDateField
       v-else-if="field.type === 'begindate'"
       :field="field"
       v-model="value"/>
     <EndDateField
       v-else-if="field.type === 'enddate'"
       :field="field"
       v-model="value"/>
     <SelectField
       v-else-if="field.type === 'select'"
       :field="field"
       v-model="value"/>
     <AppointmentSelectField
       v-else-if="field.type === 'appointmentselect'"
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
     <SuccessMessage
       v-else-if="field.type === 'successmessage'"
       :field="field"
       v-model="value"/>
     <Calendar
       v-else-if="field.type === 'calendar'"
       :field="field"
       v-model="value"/>
     <Stepper
       v-else-if="field.type === 'stepper'"
       :field="field"
       v-model="value">
     </Stepper>
     <CommentsField
       v-else-if="field.type === 'comments'"
       :field="field"
       v-model="value">
     </CommentsField>
     <HotList
       v-else-if="field.type === 'hotlist'"
       :field="field"
       v-model="value">
     </HotList>
     <ApexChart
       v-else-if="field.type === 'chart'"
       :field="field"
       v-model="value">
     </ApexChart>
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
import TextAreaField from './TextAreaField'
import BirthdayField from './BirthdayField'
import AppointmentDateField from './AppointmentDateField'
import BeginDateField from './BeginDateField'
import EndDateField from './EndDateField'
import SelectField from './SelectField'
import AppointmentSelectField from './AppointmentSelectField'
import MultiSelectField from './MultiSelectField'
import MultiSelectTreeField from './MultiSelectTreeField'
import MenuSelectField from './MenuSelectField'
import Stepper from './Stepper'
import SuccessMessage from './SuccessMessage'
import Calendar from './Calendar'
import CommentsField from './CommentsField'
import HotList from './HotList'
import ApexChart from './ApexChart'

export default {
  name: 'FormFieldFactory',
  props: {
    value: {},
    field: {}
  },
  components: {
    ApexChart,
    CommentsField,
    SuccessMessage,
    DataTable,
    DataTree,
    Button,
    Search,
    TextField,
    TextAreaField,
    BirthdayField,
    AppointmentDateField,
    SelectField,
    AppointmentSelectField,
    MultiSelectField,
    MultiSelectTreeField,
    MenuSelectField,
    Stepper,
    Calendar,
    HotList,
    BeginDateField,
    EndDateField
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
