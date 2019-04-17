<template>
  <div>
    <apexchart :type="field.chart_type" :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
import { onGetAll } from '../api/requests'

export default {
  name: 'ApexChart',
  props: {
    value: {},
    field: {}
  },
  data () {
    return {
      data: {
        loading: false,
        object: {}
      },
      options: {
        chart: {
          id: this.field.name
        },
        xaxis: {
          categories: []
        }
      },
      series: [{
        name: this.field.series_name,
        data: []
      }]
    }
  },
  mounted () {
    this.getItems()
  },
  methods: {
    getItems () {
      onGetAll(this.field.api, 'object', this.data).then(resp => {
        this.options = {
          chart: {
            id: this.field.name
          },
          xaxis: {
            categories: this.data.object.label
          }
        }
        this.series = [{
          name: this.field.series_name,
          data: this.data.object.data
        }]
      })
    }
  }
}
</script>

<style scoped>

</style>
