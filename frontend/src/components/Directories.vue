<template>
  <div>
    <nav class="nav flex-column">
      <router-link class="navbar" active-class="active" to="/directories/organizations">{{'Organizations' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/units">{{'Units' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/positions">{{'Positions' | translate}}</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Directories'
}
</script>

<style scoped>

</style>
