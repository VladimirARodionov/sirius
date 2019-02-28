<template>
  <div>
    <v-flex
      xs12
      class="mb-3"
    >
      <v-sheet height="500">
        <v-calendar
          :ref="field.name"
          v-model="date"
          :type="type"
          color="primary"
          :weekdays="[1, 2, 3, 4, 5, 6, 0]"
          interval-minutes=30
          interval-count=48
          locale="ru"
          v-on:change="change(start, end)"
        ></v-calendar>
      </v-sheet>
    </v-flex>
    <v-layout wrap>
    <v-flex
      sm4
      xs12
      class="text-sm-left text-xs-center"
    >
      <v-btn @click="$refs[field.name].prev()">
        <v-icon
          dark
          left
        >
          keyboard_arrow_left
        </v-icon>
      </v-btn>
    </v-flex>
    <v-flex
      sm4
      xs12
      class="text-xs-center"
    >
      <v-select
        v-model="type"
        :items="typeOptions"
        label="Type"
      ></v-select>
    </v-flex>
    <v-flex
      sm4
      xs12
      class="text-sm-right text-xs-center"
    >
      <v-btn @click="$refs[field.name].next()">
        <v-icon
          right
          dark
        >
          keyboard_arrow_right
        </v-icon>
      </v-btn>
    </v-flex>
    </v-layout>
  </div>
</template>

<script>
import { onGetAll } from '../api/requests'
import moment from 'moment-timezone'

export default {
  name: 'Calendar',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      data: {
        objects: [],
        loading: false
      },
      type: 'week',
      date: new Date().toISOString().substr(0, 10),
      start: '',
      end: '',
      timezone: moment.tz.guess(),
      typeOptions: [
        { text: 'Day', value: 'day' },
        { text: 'Week', value: 'week' },
        { text: 'Month', value: 'month' }
      ]
    }
  },
  mounted () {
    this.$refs[this.field.name].scrollToTime(new Date().getTime())
    var current = new Date() // get current date
    this.start = current.getDate() - current.getDay() + 1
    this.end = this.start + 6 // end day is the first day + 6
    this.getItems()
  },
  methods: {
    getItems () {
      onGetAll(this.field.api + '?start=' + this.start + '&end=' + this.end + '&timezone=' + this.timezone, 'objects', this.data)
    },
    change (start, end) {
      this.start = start.date
      this.end = end.date
      this.getItems()
    }
  }
}
</script>

<style scoped>

</style>
