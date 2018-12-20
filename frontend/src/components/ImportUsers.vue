<template>
        <div id="starting">
        <h1>{{ 'Import users' | translate}}</h1>
            <div container v-if="result">
                <div class="row">
                    <div class="col col-lg-6">

                            <div class="alert alert-success" v-if="result.success">
                                <p>{{ 'Success' | translate}}</p>
                                <div>{{ 'Added records' | translate}}: {{ result.num_success }} </div>
                                <div>{{ 'Existing records' | translate}}: {{ result.num_exists }} </div>
                                <div>{{ 'Failed records' | translate}}: {{ result.num_failed }} </div>
                            </div>
                            <div class="alert alert-danger" v-else-if="result.error">
                                <p>{{ 'Failure' | translate}}</p>
                                <div>{{ result.error }}</div>
                            </div>
                    </div>
                </div>
            </div>

        <form v-roles="['admin_role', 'edit_role']"  @submit.prevent="importUsers()">
            <input type="file" id="filename" name="filename">

            <div class="mt-3">
                <button type="submit" class="btn btn-primary">{{ 'Import' | translate}}</button>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ImportUsers',
  data () {
    return {
      result: {}
    }
  },
  methods: {
    importUsers: function () {
      var formData = new FormData()
      var filename = document.querySelector('#filename')
      formData.append('filename', filename.files[0])
      axios.post(process.env.API_URL + '/api/import/user/', formData, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(resp => {
          if (resp.data.result) {
            this.result = resp.data.result
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style scoped>

</style>
