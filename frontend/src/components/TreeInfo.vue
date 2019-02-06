<template>
  <v-card>
    <v-card-title class="grey lighten-2" primary-title>
      {{title}}
    </v-card-title>
    <v-treeview
      :items="items"
      open-all
    >
      <template slot="label" slot-scope="{ item }">
        <div>
          {{ item.name + ' (' + item.user_count + ')'}}
        </div>
      </template>
    </v-treeview>
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
