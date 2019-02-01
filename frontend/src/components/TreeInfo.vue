<template>
  <v-card>
    <v-card-title class="grey lighten-2" primary-title>
      {{title}}
    </v-card-title>
    <v-treeview
      :items="items"
      :open-all="true"
    />
  </v-card>
</template>

<script>
export default {
  name: 'TreeInfo',
  data: () => ({
  }),
  props: {
    title: String,
    items: Array
  }
}
</script>

<style scoped>

</style>
