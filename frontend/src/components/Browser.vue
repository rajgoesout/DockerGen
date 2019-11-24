<template>
  <div id="root">
    <div class="columns is-multiline is-mobile">
      <div
        v-for="(item, index) in info"
        :key="index"
        class="column is-one-third"
      >
        <div class="card">
          <div class="card-content">
            <router-link
              class="buttonTxt"
              :to="{ path: $route.path + '/' + item[2] }"
            >
              <b-button
                v-if="item[1] == 'F'"
                size="is-medium"
                type="is-primary"
              >
                {{ item[2] }}
              </b-button>
              <b-button
                v-else
                size="is-medium"
                type="is-success"
              >
                {{ item[2] }}
              </b-button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const HOST = 'http://localhost:5000'
const API_URL = 'http://localhost:5000/browser'
const URL_PATH = '/'

export default {
  name: 'Browser',
  components: {},
  data() {
    return {
      info: null,
      urlPath: HOST + this.$route.path
    }
  },
  watch: {
    '$route.params.urlPath': function(newVal, oldVal) {
      console.log(this.urlPath)
      if (newVal !== null && newVal != undefined)
        this.urlPath = API_URL + '/' + newVal
      else this.urlPath = API_URL
      console.log(oldVal, newVal, this.urlPath)
      this.init()
    }
  },
  created() {
    this.init()
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      let requestUrl = API_URL
      console.log('UP', this.urlPath)
      if (this.urlPath !== null) requestUrl = this.urlPath
      console.log('rurl', requestUrl)
      if (requestUrl[requestUrl.length - 1] == '/') {
        console.log()
        requestUrl = requestUrl.substring(0, requestUrl.length - 1)
      }
      axios.get(requestUrl).then(response => {
        this.info = response.data.list
      })
      console.log('hello')
    },
    clickMe() {
      this.$buefy.notification.open('Clicked!!')
    }
  }
}
</script>

<style scoped>
#root {
  margin: 0 40px;
}

/* .column {
  border: 1px solid black;
}

.buttonTxt {
  font-size: 40px;
} */
</style>
