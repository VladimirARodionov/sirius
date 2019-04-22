import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import vuexI18n from 'vuex-i18n'
import 'bootstrap'
import 'vuetify/dist/vuetify.min.css'
import Vuetify from 'vuetify'
import ru from 'vuetify/lib/locale/ru'
import VRM from './vue-role-manager'
import 'bootstrap/dist/css/bootstrap.css'
import VueBus from 'vue-bus'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import VueApexCharts from 'vue-apexcharts'

Vue.use(VueBus)
Vue.use(VRM, { router: router, debug: true })

Vue.use(Vuetify, {
  lang: {
    locales: { ru },
    current: 'ru'
  }
})

Vue.prototype.$http = Axios

const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = 'JWT ' + token
  const roles = localStorage.getItem('roles')
  Vue.prototype.$vrm.setRoles(roles)
}

Vue.config.productionTip = false

Vue.use(vuexI18n.plugin, store,
  {
    moduleName: 'i18n',
    onTranslationNotFound (locale, key) {
      console.warn(`i18n :: Key '${key}' not found for locale '${locale}'`)
    }
  }
)

Vue.i18n.add('ru', require('./locale/ru.json'))

Vue.i18n.set('ru')

Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

var apexRu = require('apexcharts/src/locales/ru.json')
VueApexCharts.chart = {
  locales: [apexRu],
  defaultLocale: 'ru'
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
