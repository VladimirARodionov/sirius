<template>
  <Menu>
    <Directory title="Payments" name="payment" api="/api/payment/"/>
  </Menu>
</template>

<script>
import Menu from '../../layouts/Menu'
import Directory from '../../components/directories/Directory'

export default {
  name: 'Payments',
  components: {
    Menu,
    Directory
  }
}
</script>

<style scoped>

</style>
