<template>
  <v-card max-width="220">
    <v-card-title class="grey lighten-2" primary-title>
      <v-icon size="40">
        {{icon}}
      </v-icon>&nbsp;
      <span class="info-box-text">{{title | translate}}</span>
    </v-card-title>
    <v-card-text class="headline font-weight-bold">
      {{value}}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'InfoBox',
  props: {
    icon: String,
    title: String,
    value: Number
  }
}
</script>

<style scoped>

</style>
