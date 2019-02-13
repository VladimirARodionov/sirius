<template>
  <Menu program="crm">
    <h1>{{ 'Export users' | translate}}</h1>
    <div container v-if="result">
      <div class="row">
        <div class="col col-lg-6">

          <div class="alert alert-success" v-if="result.success">
            <p>{{ 'Success' | translate}}</p>
          </div>
          <div class="alert alert-danger" v-else-if="result.error">
            <p>{{ 'Failure' | translate}}</p>
            <div>{{ result.error }}</div>
          </div>
        </div>
      </div>
    </div>

    <form v-roles="['admin_role', 'user_role']" @submit.prevent="exportUsers()">
      <div class="mt-3">
        <button type="submit" class="btn btn-primary">{{ 'Export' | translate}}</button>
      </div>
    </form>
  </Menu>
</template>

<script>
import axios from 'axios'
import Menu from '../layouts/Menu'

export default {
  name: 'ExportUsers',
  data () {
    return {
      result: {}
    }
  },
  methods: {
    exportUsers: function () {
      axios.get(process.env.API_URL + '/api/export/user/', { responseType: 'blob' })
        .then(resp => {
          const url = window.URL.createObjectURL(new Blob([resp.data]))
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', 'users.xls')
          document.body.appendChild(link)
          link.click()
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  components: {
    Menu
  }
}
</script>

<style scoped>

</style>
