<template>
  <div>
    <v-alert outline type="success" value="true" v-if="successMessage">
      {{successMessage}}
    </v-alert>
    <v-stepper v-model="step">
      <v-stepper-header>
        <template v-for="(item, index) in field.headers">
          <v-stepper-step
            :key="index + 1 + '-step'"
            :complete="step > (index + 1)"
            :step="index + 1"
          >
            {{ item.text | translate }}
          </v-stepper-step>

          <v-divider
            v-if="index !== (field.headers.length - 1)"
            :key="index + 1"
          ></v-divider>
        </template>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content v-for="(item, index) in field.fields" :key="index + 1 + '-content'" :step="index + 1">
          <v-card
            class="mb-5"
          >
            <div v-if="item.fields">
              <FormFieldFactory v-for="subfield in item.fields" :key="subfield.name"
                                v-model="value"
                                :field="subfield"/>
            </div>
            <div v-else>
              <FormFieldFactory
                v-model="value"
                :field="item"/>
            </div>
          </v-card>

          <v-btn
            color="primary"
            @click="onNext(index + 1, field.fields.length)"
          >
            {{((index + 1) === field.fields.length)? 'Submit' : 'Continue' | translate}}
          </v-btn>

          <v-btn
            flat
            @click="onBack(index + 1)">
            {{'Back' | translate}}
          </v-btn>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </div>
</template>

<script>

export default {
  name: 'Stepper',
  props: {
    value: {},
    field: {}
  },
  components: {
    FormFieldFactory: () => import('./FormFieldFactory.vue')
  },
  data () {
    return {
      step: 0,
      successMessage: '',
      data: {
        currentObject: {},
        loading: false,
        errorMessage: ''
      }
    }
  },
  created () {
    this.$bus.on('timeIntervalSuccess', this.onTimeIntervalSuccess)
    this.$bus.on('consultantSuccess', this.onConsultantSuccess)
    this.$bus.on('appointmentSuccess', this.onAppointmentSuccess)
  },
  beforeDestroy () {
    this.$bus.off('timeIntervalSuccess', this.onTimeIntervalSuccess)
    this.$bus.off('consultantSuccess', this.onConsultantSuccess)
    this.$bus.off('appointmentSuccess', this.onAppointmentSuccess)
  },
  methods: {
    onNext (index, total) {
      if (index === 1) {
        this.onGetTimeInterval()
      } else if (index === 2) {
        this.onGetConsultant()
      } else if (index === 3) {
        this.onSubmit()
      }
    },
    onBack (index) {
      if (index > 1) {
        this.step = index - 1
      }
    },
    onSubmit () {
      this.$bus.emit('saveObject')
    },
    onGetTimeInterval () {
      this.$bus.emit('getTimeInterval')
    },
    onGetConsultant () {
      this.$bus.emit('getConsultant')
    },
    onTimeIntervalSuccess () {
      this.step = this.step + 1
    },
    onConsultantSuccess () {
      this.step = this.step + 1
    },
    onAppointmentSuccess () {
      this.step = this.field.fields.length + 1
      this.successMessage = this.$t('Appointment successfully made')
    }
  }
}
</script>

<style scoped>

</style>
