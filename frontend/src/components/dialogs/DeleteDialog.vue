<template>
  <v-dialog v-model="dialog" persistent max-width="500">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title>{{'Delete confirm' | translate}}</v-card-title>
      <v-card-text> {{message}} </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="gray darken-1" @click.native="close">{{'No' | translate}}</v-btn>
        <v-btn color="red darken-1" @click="clicked()">{{'Delete' | translate}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'DeleteDialog',
  methods: {
    clicked () {
      this.onClicked()
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
