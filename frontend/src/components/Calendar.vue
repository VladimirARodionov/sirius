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
export default {
  name: 'Calendar',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      type: 'week',
      date: new Date().toISOString().substr(0, 10),
      typeOptions: [
        { text: 'Day', value: 'day' },
        { text: 'Week', value: 'week' },
        { text: 'Month', value: 'month' }
      ]
    }
  },
  mounted () {
    this.$refs[this.field.name].scrollToTime(new Date().getTime())
  }
}
</script>

<style scoped>

</style>
