<template>
  <Menu>
    <Directory title="Cities" name="city" api="/api/city/" :headers="this.headers" :names="this.names" addRouter="addCity" editRouter="editCity" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Cities',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('Region'), value: 'region' },
        { text: this.$i18n.translate('Name'), value: 'name' }
      ],
      names: [
        { name: 'id' },
        { name: 'city_region.name' },
        { name: 'name' }
      ],
      select: 'false'
    }
  },
  created () {
    if (this.$route.query && this.$route.query.select) {
      this.select = this.$route.query.select
    }
  },
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
