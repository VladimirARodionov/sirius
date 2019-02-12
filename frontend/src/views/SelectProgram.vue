<template>
  <Default>
    <DataForm resource="main" action="menu"></DataForm>
  </Default>
</template>

<script>
import DataForm from '../components/DataForm'
import Default from '../layouts/Default'
export default {
  name: 'SelectProgram',
  components: {
    Default,
    DataForm
  }
}

</script>
