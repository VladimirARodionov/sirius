<template>
  <div>
    <nav class="nav flex-column">
      <router-link class="navbar" active-class="active" to="/actions/import/users">{{'Import users' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/actions/export/users">{{'Export users' | translate}}</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Actions'
}
</script>

<style scoped>

</style>
