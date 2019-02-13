<template>
  <Menu program="zdravniza">
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
          <InfoBox icon="people_outline" :title="$t('Total employees')" :value="data.employees"/>
          <InfoBox icon="event_note" :title="$t('Total clients')" :value="data.clients"/>
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
        clients: 0,
        users: 0,
        faculty: [],
        unit: [],
        loading: false
      }
    }
  },
  mounted: function () {
    this.getEmployeeCount()
    this.getClientCount()
  },
  methods: {
    getEmployeeCount: function () {
      onGetCount('/api/zdravniza/count/', 'employees', this.data)
    },
    getClientCount: function () {
      onGetCount('/api/client/count/', 'clients', this.data)
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
