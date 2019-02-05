<template>
  <Menu>
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
          <InfoBox icon="people_outline" :title="$t('Total employees')" :value="data.employees"/>
          <InfoBox icon="chat" :title="$t('Total disciples')" :value="data.disciples"/>
          <InfoBox icon="people" :title="$t('Total users')" :value="data.users"/>
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
