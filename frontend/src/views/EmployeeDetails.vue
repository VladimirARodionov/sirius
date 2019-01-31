<template>
  <Menu>
    <UserDetail :title="$t('Employee details')" api="/api/userdetail/" :names="names"/>
  </Menu>
</template>

<script>
import Menu from '../layouts/Menu'
import UserDetail from '../components/UserDetail'

export default {
  name: 'EmployeeDetails',
  data () {
    return {
      names: [
        { text: 'Last name', type: 'input', name: 'last_name', required: true },
        { text: 'First name', type: 'input', name: 'first_name', required: true },
        { text: 'Middle name', type: 'input', name: 'middle_name' },
        { text: 'Email', type: 'input', name: 'email' },
        { text: 'Mobile', type: 'input', name: 'mobile' },
        { text: 'Birthday', type: 'date', name: 'birthday' },
        { text: 'Address', type: 'selector', name: 'address', routerName: 'addresses', api: '/api/address/', value: 'address.address_city.name' },
        { text: 'Unit', type: 'selector', name: 'unit', routerName: 'units', api: '/api/unit/', value: 'unit.text' },
        { text: 'Categories', type: 'multi-selector', name: 'categories', routerName: 'categories', api: '/api/category/', updateApi: '/api/usercategory/update/', value: 'name', multiselect_value: 'category_value.name' },
        { text: 'Positions', type: 'multi-selector', name: 'positions', routerName: 'positions', api: '/api/position/', updateApi: '/api/userposition/update/', value: 'name', multiselect_value: 'position_value.name' }
      ]
    }
  },
  components: {
    Menu,
    UserDetail
  }
}
</script>

<style scoped>

</style>
