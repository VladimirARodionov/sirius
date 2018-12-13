import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import vuexI18n from 'vuex-i18n'
import 'bootstrap'

Vue.prototype.$http = Axios

const token = localStorage.getItem('user-token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
  Vue.prototype.$http.defaults.headers.common['crossDomain'] = true
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

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
