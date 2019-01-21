<template>
  <Menu>
    <InfoBox icon="people_outline" title="Total users" :value="data.object"/>
  </Menu>
</template>

<script>
import Menu from './layouts/Menu'
import InfoBox from './InfoBox'
import { onGetCount } from '../api/requests'

export default {
  name: 'Home',
  data () {
    return {
      data: {
        object: 0,
        loading: false
      }
    }
  },
  mounted: function () {
    this.getCount()
  },
  methods: {
    getCount: function () {
      onGetCount('/api/user/count/', this.data)
    }
  },
  components: {
    Menu,
    InfoBox
  }

}
</script>

<style scoped>

</style>
