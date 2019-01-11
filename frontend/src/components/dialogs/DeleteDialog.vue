<template>
  <v-dialog v-model="dialog" persistent max-width="500">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title>{{'Delete confirm' | translate}}</v-card-title>
      <div class="alert alert-danger" v-if="errorMessage">
        {{errorMessage}}
      </div>
      <v-card-text> {{message}} </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="gray darken-1" @click.native="close">{{'No' | translate}}</v-btn>
        <v-btn color="red darken-1" @click.native="clicked()">{{'Delete' | translate}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'DeleteDialog',
  data () {
    return {
      errorMessage: ''
    }
  },
  methods: {
    clicked () {
      this.errorMessage = ''
      try {
        this.onClicked()
      } catch (err) {
        console.log(err)
        if (err.response && err.response.data) {
          var errors = err.response.data
          for (var value in errors) {
            if (value instanceof Array) {
              this.errorMessage = errors[value][0]
            } else {
              this.errorMessage = errors[value]
            }
          }
          console.log(err.response.data)
        }
      }
    },
    close () {
      this.$emit('update:dialog', false)
    }
  },
  props: {
    dialog: {
      default: false
    },
    message: String,
    onClicked: Function
  }
}
</script>

<style scoped>

</style>
