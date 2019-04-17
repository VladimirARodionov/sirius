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
      begin_date: null,
      end_date: null,
      option: null,
      total: 0,
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
  created () {
    this.$bus.on('changeBeginDate', this.onChangeBeginDate)
    this.$bus.on('changeEndDate', this.onChangeEndDate)
    this.$bus.on('changeObject', this.onChangeObject)
    this.$bus.on('generateAction', this.onGenerateAction)
  },
  beforeDestroy () {
    this.$bus.off('changeBeginDate', this.onChangeBeginDate)
    this.$bus.off('changeEndDate', this.onChangeEndDate)
    this.$bus.off('changeObject', this.onChangeObject)
    this.$bus.off('generateAction', this.onGenerateAction)
  },
  mounted () {
    this.getItems()
  },
  methods: {
    getItems () {
      onGetAll(this.field.api, 'object', this.data).then(resp => {
        this.total = this.data.object.data.reduce((a, b) => a + b, 0)
        this.options = {
          chart: {
            id: this.field.name
          },
          xaxis: {
            categories: this.data.object.label
          },
          title: {
            text: this.$t('Total') + ': ' + this.total,
            align: 'center'
          }
        }
        this.series = [{
          name: this.field.series_name,
          data: this.data.object.data
        }]
      })
    },
    onChangeBeginDate (data) {
      this.begin_date = data
    },
    onChangeEndDate (data) {
      this.end_date = data
    },
    onChangeObject (data) {
      this.option = data[this.field.option_name] || 0
    },
    onGenerateAction () {
      let urlParameters = '?option=' + (this.option || 0)
      if (this.begin_date) {
        urlParameters = urlParameters + '&begin=' + this.begin_date
      }
      if (this.end_date) {
        urlParameters = urlParameters + '&end=' + this.end_date
      }
      onGetAll(this.field.api + urlParameters, 'object', this.data).then(resp => {
        this.total = this.data.object.data.reduce((a, b) => a + b, 0)
        this.options = {
          chart: {
            id: this.field.name
          },
          xaxis: {
            categories: this.data.object.label
          },
          title: {
            text: this.$t('Total') + ': ' + this.total,
            align: 'center'
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
