<template>
  <Menu>
    <Directory title="Addresses" name="address" api="/api/address/" :headers="this.headers" :names="this.names" addRouter="addAddress" editRouter="editAddress" :select="select"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Addresses',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('City'), value: 'city' },
        { text: this.$i18n.translate('Village'), value: 'village' },
        { text: this.$i18n.translate('Street'), value: 'street' },
        { text: this.$i18n.translate('House'), value: 'house' },
        { text: this.$i18n.translate('Apartment'), value: 'apartment' }
      ],
      names: [
        { name: 'id' },
        { name: 'address_city.name' },
        { name: 'village' },
        { name: 'street' },
        { name: 'house' },
        { name: 'apartment' }
      ],
      select: 'false'
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getObjects()
      },
      deep: true
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
