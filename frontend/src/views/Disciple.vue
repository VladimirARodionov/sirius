<template>
  <Menu>
    <UserList :title="$t('List of disciples')" api="/api/disciple/" :headers="headers" :addTitle="$t('Add disciple')" :editTitle="$t('Edit')" :deleteMessagePrefix="$t('Delete disciple')" userDetailsRoute="discipleDetails"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import UserList from '../components/UserList'

export default {
  name: 'Disciple',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('First name'), value: 'first_name' },
        { text: this.$i18n.translate('Last name'), value: 'last_name' },
        { text: this.$i18n.translate('Email'), value: 'email' }
      ]
    }
  },
  components: {
    Menu,
    UserList
  }
}
</script>

<style scoped>

</style>
