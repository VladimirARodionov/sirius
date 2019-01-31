<template>
  <Menu>
    <UserList :title="$t('List of users')" api="/api/user/" :headers="headers" :addTitle="$t('Add user')" :editTitle="$t('Edit')" :deleteMessagePrefix="$t('Delete user')" userDetailsRoute="userDetails"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import UserList from '../../components/UserList'

export default {
  name: 'User',
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
