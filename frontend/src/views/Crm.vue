<template>
  <Menu program="crm">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
          <InfoBox icon="people_outline" :title="$t('Total employees')" :value="data.employees"/>
          <InfoBox icon="chat" :title="$t('Total disciples')" :value="data.disciples"/>
          <InfoBox icon="people" :title="$t('Total users')" :value="data.users"/>
          <InfoBox icon="people_outline" :title="$t('Total consultants')" :value="data.consultants"/>
          <InfoBox icon="person_add" :title="$t('Total leads')" :value="data.leads"/>
      </v-layout>
      <v-layout row wrap>
          <TreeInfo :title="$t('Employees')" :items="data.unit"/>
          <TreeInfo :title="$t('Disciples')" :items="data.faculty"/>
      </v-layout>
    </v-container>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import InfoBox from '../components/InfoBox'
import TreeInfo from '../components/TreeInfo'
import { onGetCount, onGetAll } from '../api/requests'

export default {
  name: 'Home',
  data () {
    return {
      data: {
        employees: 0,
        disciples: 0,
        users: 0,
        consultants: 0,
        leads: 0,
        faculty: [],
        unit: [],
        loading: false
      }
    }
  },
  mounted: function () {
    this.getEmployeeCount()
    this.getDiscipleCount()
    this.getUserCount()
    this.getConsultantCount()
    this.getLeadCount()
    this.getUnitTreeCount()
    this.getFacultyTreeCount()
  },
  methods: {
    getEmployeeCount: function () {
      onGetCount('/api/employee/count/', 'employees', this.data)
    },
    getDiscipleCount: function () {
      onGetCount('/api/disciple/count/', 'disciples', this.data)
    },
    getUserCount: function () {
      onGetCount('/api/user/count/', 'users', this.data)
    },
    getConsultantCount: function () {
      onGetCount('/api/crmconsultant/count/', 'consultants', this.data)
    },
    getLeadCount: function () {
      onGetCount('/api/lead/count/', 'leads', this.data)
    },
    getUnitTreeCount: function () {
      onGetAll('/api/unit/', 'unit', this.data)
    },
    getFacultyTreeCount: function () {
      onGetAll('/api/faculty/', 'faculty', this.data)
    }
  },
  components: {
    Menu,
    InfoBox,
    TreeInfo
  }

}
</script>

<style scoped>

</style>
