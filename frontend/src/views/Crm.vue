<template>
  <Menu program="crm">
    <v-container grid-list-xl fluid p-0>
      <v-layout row wrap>
          <HotList :field="data.created_hotlist"/>
          <HotList :field="data.action_hotlist"/>
      </v-layout>
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
import HotList from '../components/HotList'
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
        loading: false,
        created_hotlist: {
          program: 'crm',
          resource: 'lead',
          api: '/api/info/lead/created/',
          icon: 'help_outline',
          title: 'Leads with status Created',
          show_id: true,
          show_name: true,
          show_date: false,
          show_time: false,
          show_action: false,
          show_consultant: true
        },
        action_hotlist: {
          program: 'crm',
          resource: 'lead',
          api: '/api/info/lead/action/',
          icon: 'done',
          title: 'Leads with action',
          show_id: true,
          show_name: true,
          show_date: true,
          show_time: true,
          show_action: true,
          show_consultant: true
        }
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
    TreeInfo,
    HotList
  }

}
</script>

<style scoped>

</style>
