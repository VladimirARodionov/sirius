<template>
  <div>
    <nav class="nav flex-column">
      <router-link class="navbar" active-class="active" to="/directories/organizations">{{'Organizations' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/units">{{'Units' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/positions">{{'Positions' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/categories">{{'Categories' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/competencies">{{'Competencies' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/countries">{{'Countries' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/regions">{{'Regions' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/cities">{{'Cities' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/courses">{{'Courses' | translate}}</router-link>
      <router-link class="navbar" active-class="active" to="/directories/payments">{{'Payments' | translate}}</router-link>
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
