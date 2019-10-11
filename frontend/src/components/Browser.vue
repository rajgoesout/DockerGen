<template>
  <div>
    <div v-for="(item, index) in listItems" :key="index">
      {{ item }}
    </div>
  </div>
</template>
<script>
export default {
  name: 'Browser',
  components: {},
  data() {
    return {
      listItems: []
    }
  }
}
</script>
<style scoped></style>
