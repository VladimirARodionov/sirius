<template>
  <Menu>
    <Directory title="Addresses" name="address" api="/api/address/" :headers="this.headers" :names="this.names" addRouter="addAddress" editRouter="editAddress" :select="select" :deleteMessage="deleteMessage"/>
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
  methods: {
    deleteMessage: function (name, object) {
      if (name && object) {
        return this.$t('Delete ' + name) +
        ' #' + object.id + ' ' +
        ((object.address_city) ? object.address_city.name : '') + ' ' +
        ((object.village) ? object.village : '') + ' ' +
        ((object.street) ? (this.$t('street') + ' ' + object.street) : '') + ' ' +
        ((object.house) ? (this.$t('house') + ' ' + object.house) : '') + ' ' +
        ((object.apartment) ? (this.$t('apartment') + ' ' + object.apartment) : '') + ' ' +
        ' ?'
      } else {
        return ''
      }
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
