<template>
  <div>
    <v-flex
      xs12
      class="mb-3"
    >
      <v-sheet>
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
                  class="my-event"
                  @click="open(event)"
                  v-html="event.title"
                ></div>
            </template>
          </template>
          <template
            slot="interval"
            slot-scope="{ date, time}"
          >
              <template v-for="event in objectsMap[date]">
              <!-- timed events -->
              <div
                v-if="time === getTime(event.start)"
                :key="event.id"
                class="my-event"
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
      let minutes = getMinutes(date)
      let time = getHours(date) + ':' + ((minutes < 10) ? ('0' + minutes) : minutes)
      return time
    },
    open (event) {
      this.$router.push('/' + this.$route.params.program + '/appointment/edit/' + event.description)
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
    clear:both;
  }

  .with-time {
      position: absolute;
      right: 4px;
      margin-right: 0px;
    }
</style>
