<template>
  <div id="root">
    <b-button @click="generate()">
      Generate Dockerfile here
    </b-button>
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

const BASE_SERVER_URL = 'http://localhost:5000'
const API_URL = BASE_SERVER_URL + '/browser'
const COLLECTDATA_URL = BASE_SERVER_URL + '/collectdata'
const URL_PATH = '/'

export default {
  name: 'Browser',
  components: {},
  data() {
    return {
      info: null,
      urlPath: BASE_SERVER_URL + this.$route.path
    }
  },
  watch: {
    '$route.params.urlPath': function(newVal, oldVal) {
      if (newVal !== null && newVal != undefined)
        this.urlPath = API_URL + '/' + newVal
      else this.urlPath = API_URL
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
      if (this.urlPath !== null) requestUrl = this.urlPath
      if (requestUrl[requestUrl.length - 1] == '/') {
        requestUrl = requestUrl.substring(0, requestUrl.length - 1)
      }
      axios.get(requestUrl).then(response => {
        this.info = response.data.list
      })
    },
    clickMe() {
      this.$buefy.notification.open('Clicked!!')
    },
    generate() {
      console.log(this.urlPath)
      console.log(COLLECTDATA_URL)
      axios.post(COLLECTDATA_URL, {
        projectPath: this.urlPath,
        lang: 'nodejs',
        isWebProject: true,
        portNumber: 3000,
        imageName: 'myImg',
        serviceName: 'myService',
        composeProjectName: 'calmNComposed'
      })
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
