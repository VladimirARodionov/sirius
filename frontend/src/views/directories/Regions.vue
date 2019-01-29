<template>
  <Menu>
    <Directory title="Regions" name="region" api="/api/region/" :headers="this.headers" :names="this.names" addRouter="addRegion" editRouter="editRegion" :select="this.select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Regions',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('Country'), value: 'country' },
        { text: this.$i18n.translate('Name'), value: 'name' }
      ],
      names: [
        { name: 'id' },
        { name: 'region_country.name' },
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
