<template>
  <Menu>
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
          <InfoBox icon="people_outline" title="Total employees" :value="data.employees"/>
          <InfoBox icon="chat" title="Total disciples" :value="data.disciples"/>
          <InfoBox icon="people" title="Total users" :value="data.users"/>
      </v-layout>
    </v-container>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import InfoBox from '../components/InfoBox'
import { onGetCount } from '../api/requests'

export default {
  name: 'Home',
  data () {
    return {
      data: {
        employees: 0,
        disciples: 0,
        users: 0,
        loading: false
      }
    }
  },
  mounted: function () {
    this.getEmployeeCount()
    this.getDiscipleCount()
    this.getUserCount()
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
    }
  },
  components: {
    Menu,
    InfoBox
  }

}
</script>

<style scoped>

</style>
