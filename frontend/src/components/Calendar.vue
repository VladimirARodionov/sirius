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
          v-on:change="change"
        >
          <template
            slot="day"
            slot-scope="{ date }"
          >
            <template v-for="event in objectsMap[date]">
                <div
                  :key="event.id"
                  v-ripple
                  v-html="event.title"
                ></div>
            </template>
          </template>
          <template
            slot="dayBody"
            slot-scope="{ date, timeToY, minutesToPixels }"
          >
            <template v-for="event in objectsMap[date]">
              <!-- timed events -->
              <div
                v-if="event.start"
                :key="event.id"
                :style="{ top: timeToY(getTime(event.start)) + 'px', height: minutesToPixels(event.duration) + 'px' }"
                class="my-event with-time"
                @click="open(event)"
                v-html="event.title"
              ></div>
            </template>
          </template>
        </v-calendar>
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
import startOfWeek from 'date-fns/start_of_week'
import endOfWeek from 'date-fns/end_of_week'
import getHours from 'date-fns/get_hours'
import getMinutes from 'date-fns/get_minutes'

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
      start: startOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().substr(0, 10),
      end: endOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().substr(0, 10),
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
    // let startAndEnd = this.startAndEndOfWeek(new Date())
    // this.start = startAndEnd[0].toISOString().substr(0, 10)
    // this.end = startAndEnd[1].toISOString().substr(0, 10)
    // this.getItems()
  },
  methods: {
    getItems () {
      onGetAll(this.field.api + '?start=' + this.start + '&end=' + this.end + '&timezone=' + this.timezone, 'objects', this.data)
    },
    change (obj) {
      this.start = obj.start.date
      let tomorrow = new Date(obj.end.date)
      tomorrow.setDate(tomorrow.getDate() + 1)
      this.end = tomorrow.toISOString().substr(0, 10)
      this.getItems()
    },
    getTime (date) {
      let time = getHours(date) + ':' + getMinutes(date)
      return time
    }
  },
  computed: {
    // convert the list of events into a map of lists keyed by date
    objectsMap () {
      const map = {}
      this.data.objects.forEach(e => (map[new Date(e.start).toISOString().substr(0, 10)] = map[new Date(e.start).toISOString().substr(0, 10)] || []).push(e))
      return map
    }
  }
}
</script>

<style scoped>
  .my-event {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    background-color: #1867c0;
    color: #ffffff;
    border: 1px solid #1867c0;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 4px;
    margin-right: 8px;
    position: relative;
  }

  .with-time {
      position: absolute;
      right: 4px;
      margin-right: 0px;
    }
</style>
