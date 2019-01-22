<template>
  <Menu>
    <h1>{{'Addresses' | translate}}</h1>
    <div class="btn-toolbar justify-content-between mb-3">
      <div>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-on:click="goAddAddress()">{{'Add' |
          translate}}
        </button>
        <button class="btn btn-success" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="goEditAddress()">{{'Edit' | translate}}
        </button>
        <button class="btn btn-danger" v-roles="['admin_role', 'edit_role']" v-if="data.isSelected"
                v-on:click="data.deleteDialog = true">{{'Delete' | translate}}
        </button>
      </div>
      <div class="input-group">
        <input class="form-control mr-sm-2" type="text" placeholder="Search" v-model="search_term" aria-label="Search">
        <span class="input-group-btn">
          <button class="btn btn-success" v-on:click.prevent="getObjects()">{{'Search' | translate}}</button>
        </span>
      </div>
    </div>
    <div class="table-responsive">
      <v-data-table
        :headers="headers"
        :items="data.objects"
        :loading="data.loading"
        :total-items="data.totalObjects"
        :pagination.sync="pagination"
        :rows-per-page-items="[10, 20, 50, 100]"
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <tr v-on:click="selectObject(props.item)" v-bind:class="isActive(props.item)">
            <td>{{ props.item.id }}</td>
            <td>{{ props.item.address_city.name }}</td>
            <td>{{ props.item.village }}</td>
            <td>{{ props.item.street }}</td>
            <td>{{ props.item.house }}</td>
            <td>{{ props.item.apartment }}</td>
          </tr>
        </template>
      </v-data-table>

    </div>
    <!-- Delete Modal -->
    <DeleteDialog :dialog.sync="data.deleteDialog" :message="getDeleteMessage()" :on-clicked="deleteObject"/>
  </Menu>
</template>

<script>
import router from '../../router'
import Menu from '../../layouts/Menu'
import DeleteDialog from '../../components/dialogs/DeleteDialog'
import { onGet, onPost, onPut, onDelete } from '../../api/requests'

export default {
  name: 'Addresses',
  data () {
    return {
      headers: [
        { text: '#', value: 'id' },
        { text: this.$i18n.translate('City'), value: 'city' },
        { text: this.$i18n.translate('Village'), value: 'village' },
        { text: this.$i18n.translate('Street'), value: 'street' },
        { text: this.$i18n.translate('House'), value: 'house' },
        { text: this.$i18n.translate('Apartment'), value: 'apartment' }
      ],
      data: {
        objects: [],
        loading: false,
        totalObjects: 0,
        newObject: {},
        currentObject: {},
        isSelected: false,
        deleteDialog: false,
        deleteDialogErrorMessage: ''
      },
      city: {
        objects: [],
        loading: false
      },
      message: null,
      search_term: '',
      pagination: {},
      errors: []
    }
  },
  watch: {
    pagination: {
      handler () {
        this.getObjects()
      },
      deep: true
    }
  },
  methods: {
    getObjects: function () {
      onGet('/api/address/', this.data, this.pagination, this.search_term)
    },
    selectObject: function (obj) {
      this.data.currentObject = JSON.parse(JSON.stringify(obj))
      this.data.isSelected = true
    },
    isActive: function (obj) {
      return {
        'table-primary': this.data.currentObject.id === obj.id
      }
    },
    addObject: function () {
      onPost('/api/address/', this.data, this.getObjects)
    },
    updateObject: function () {
      onPut('/api/address/', this.data, this.getObjects)
    },
    deleteObject: function () {
      onDelete('/api/address/', this.data, this.getObjects)
    },
    getDeleteMessage: function () {
      return this.$t('Delete address') + ' ' + this.data.currentObject.id + ' ?'
    },
    goAddAddress: function () {
      router.push({ name: 'addAddress' })
    },
    goEditAddress: function () {
      if (this.data.currentObject !== '') {
        router.push({ name: 'editAddress', params: { id: this.data.currentObject.id } })
      }
    }
  },
  components: {
    DeleteDialog,
    Menu
  }
}
</script>

<style scoped>

</style>
