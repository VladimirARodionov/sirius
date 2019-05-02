import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {},
    selectedObject: {},
    savedState: {},
    tableIndex: {}
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
    },
    clearSavedState (state, name) {
      state.savedState[name] = null
    },
    setSavedState (state, obj) {
      state.savedState[obj.resource] = {}
      state.savedState[obj.resource][obj.id] = obj.obj
    },
    clearTableIndex (state, table) {
      state.tableIndex[table] = null
    },
    setTableIndex (state, obj) {
      state.tableIndex[obj.resource] = {}
      state.tableIndex[obj.resource]['id'] = obj.id
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
            localStorage.setItem('token', token)
            localStorage.setItem('roles', roles)
            Vue.prototype.$vrm.setRoles(roles)
            localStorage.setItem('user_id', resp.data.user_id)
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
        localStorage.removeItem('user_id')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },
    clearSelectedObject ({ commit }) {
      commit('clearSelectedObject')
    },
    setSelectedObject ({ commit }, obj) {
      commit('setSelectedObject', obj)
    },
    clearSavedState ({ commit }, name) {
      commit('clearSavedState', name)
    },
    setSavedState ({ commit }, obj) {
      commit('setSavedState', obj)
    },
    clearTableIndex ({ commit }, name) {
      commit('clearTableIndex', name)
    },
    setTableIndex ({ commit }, obj) {
      commit('setTableIndex', obj)
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    getSelectedObject: state => state.selectedObject,
    getSavedState: state => state.savedState,
    getTableIndex: state => state.tableIndex
  }
})
