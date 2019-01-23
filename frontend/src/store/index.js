import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {},
    selectedObject: {}
  },
  mutations: {
    auth_request (state) {
      state.status = 'loading'
    },
    auth_success (state, token, user) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    auth_error (state) {
      state.status = 'error'
    },
    logout (state) {
      state.status = ''
      state.token = ''
    },
    clearSelectedObject (state) {
      state.selectedObject = {}
    },
    setSelectedObject (state, obj) {
      state.selectedObject = obj
    }
  },
  actions: {
    login ({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: process.env.API_URL + '/api/login/', data: user, method: 'POST' })
          .then(resp => {
            const token = resp.data.token
            const roles = resp.data.roles
            const permissions = resp.data.permissions
            localStorage.setItem('token', token)
            localStorage.setItem('roles', roles)
            Vue.prototype.$vrm.setRoles(roles)
            localStorage.setItem('permissions', permissions)
            Vue.prototype.$vrm.setPermissions(permissions)
            // Add the following line:
            axios.defaults.headers.common['Authorization'] = 'JWT ' + token
            commit('auth_success', token, user)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    register ({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: 'http://localhost:3000/register', data: user, method: 'POST' })
          .then(resp => {
            const token = resp.data.token
            const user = resp.data.user
            localStorage.setItem('token', token)
            // Add the following line:
            axios.defaults.headers.common['Authorization'] = token
            commit('auth_success', token, user)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error', err)
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    logout ({ commit }) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('roles')
        localStorage.removeItem('permissions')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },
    clearSelectedObject ({ commit }) {
      commit('clearSelectedObject')
    },
    setSelectedObject ({ commit }, obj) {
      commit('setSelectedObject', obj)
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    getSelectedObject: state => state.selectedObject
  }
})
