<template>
  <v-list two-line>
    <v-list-tile avatar class="elevation-1" @click="goList()">
      <v-list-tile-avatar>
        <v-icon large>{{ field.icon }}</v-icon>
      </v-list-tile-avatar>

      <v-list-tile-content>
        <v-list-tile-title>{{ field.text | translate }}</v-list-tile-title>
        <v-list-tile-sub-title>{{ field.subtext | translate }}</v-list-tile-sub-title>
      </v-list-tile-content>

      <v-list-tile-action>
        <v-icon>chevron_right</v-icon>
      </v-list-tile-action>
    </v-list-tile>
  </v-list>
</template>

<script>
export default {
  name: 'MenuSelectField',
  props: {
    value: {},
    field: {}
  },
  methods: {
    goList () {
      this.$router.push(this.field.value)
    }
  }
}
</script>

<style scoped>
</style>
