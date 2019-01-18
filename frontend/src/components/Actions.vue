<template>
  <Menu>
    <nav class="nav flex-column">
      <router-link class="navbar" active-class="active" to="/actions/import/users">{{'Import users' | translate}}
      </router-link>
      <router-link class="navbar" active-class="active" to="/actions/export/users">{{'Export users' | translate}}
      </router-link>
    </nav>
  </Menu>
</template>

<script>
import Menu from './layouts/Menu'

export default {
  name: 'Actions',
  components: {
    Menu
  }
}
</script>

<style scoped>

</style>
