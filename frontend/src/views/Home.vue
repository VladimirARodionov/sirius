<template>
  <Menu>
    <v-container grid-list-xl fluid>
      <v-layout row wrap>
          <InfoBox icon="people_outline" :title="$t('Total employees')" :value="data.employees"/>
          <InfoBox icon="chat" :title="$t('Total disciples')" :value="data.disciples"/>
          <InfoBox icon="people" :title="$t('Total users')" :value="data.users"/>
      </v-layout>
      <v-layout>
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
      },
      items1: [
        {
          id: 1,
          name: 'Институт (50 человек)',
          children: [
            { id: 2, name: 'Кафедра1 (20 человек)' },
            { id: 3, name: 'Кафедра2 (20 человек)' },
            { id: 4, name: 'Кафедра3 (10 человек)' }
          ]
        },
        {
          id: 5,
          name: 'Троешколие (40 человек)',
          children: [
            {
              id: 6,
              name: 'Путь огня (40 человек)',
              children: [
                {
                  id: 7,
                  name: 'класс1 (20 человек)'
                },
                {
                  id: 8,
                  name: 'класс2 (20 человек)'
                }
              ]
            }
          ]
        },
        {
          id: 15,
          name: 'Академия (30 человек)',
          children: [
            { id: 16, name: 'Класс 1 (10 человек)' },
            { id: 17, name: 'Класс 2 (10 человек)' },
            { id: 18, name: 'Класс 3 (10 человек)' }
          ]
        }
      ],
      items2: [
        {
          id: 1,
          name: 'Отдел 1 (20  человек)',
          children: [
            { id: 2, name: 'Подотдел1 (7  человек)' },
            { id: 3, name: 'Подотдел2 (7 человек)' },
            { id: 4, name: 'Подотдел3 (6 человек)' }
          ]
        }
      ]
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
