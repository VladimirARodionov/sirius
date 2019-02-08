<template>
  <div>
    <v-text-field
      type="text"
      :id="field.name"
      :label="$t(field.text)"
      append-icon="search"
      @keyup.enter.native="search()"
      @click:append="search()"
      v-model="search_term">
    </v-text-field>
  </div>
</template>

<script>
export default {
  name: 'Search',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      search_term: ''
    }
  },
  methods: {
    search () {
      this.$bus.emit('search', this.search_term)
    }
  }
}
</script>

<style scoped>

</style>
