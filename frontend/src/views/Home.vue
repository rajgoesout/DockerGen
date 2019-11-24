<template>
  <div class="home">
    <Browser />
  </div>
</template>

<script>
// @ is an alias to /src
import Browser from '@/components/Browser.vue'

export default {
  name: 'Home',
  components: {
    Browser
  }
}
</script>
