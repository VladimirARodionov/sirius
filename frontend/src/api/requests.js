import axios from 'axios'
import Vue from 'vue'
import vuetifyToast from 'vuetify-toast'

export function onGet (api, data, pagination, searchTerm) {
  data.loading = true
  let apiUrl = api + '?page=' + pagination.page + '&page_size=' + pagination.rowsPerPage
  if (searchTerm) {
    apiUrl = apiUrl + '&search=' + searchTerm
  }
  if (pagination.sortBy) {
    const direction = pagination.descending ? '-' : ''
    apiUrl = apiUrl + '&ordering=' + direction + pagination.sortBy
  }
  axios.get(process.env.API_URL + apiUrl)
    .then(resp => {
      data.objects = resp.data.results
      data.totalObjects = resp.data.count
      data.currentObject = {}
      data.isSelected = false
      data.loading = false
    })
    .catch(err => {
      data.loading = false
      console.log(err)
    })
}

export function onPost (api, data, getFunction) {
  data.addDialogErrorMessage = ''
  axios.post(process.env.API_URL + api, data.newObject)
    .then(resp => {
      data.loading = false
      data.addDialog = false
      vuetifyToast.success(Vue.i18n.translate('Success'), { icon: 'check_circle_outline' })
      getFunction()
    })
    .catch(err => {
      if (err.response && err.response.data) {
        const errors = err.response.data
        for (const value in errors) {
          if (errors[value] instanceof Array) {
            data.addDialogErrorMessage = errors[value][0]
          } else {
            data.addDialogErrorMessage = errors[value]
          }
        }
        vuetifyToast.error(Vue.i18n.translate('Error'), { icon: 'highlight_off' })
        console.log(err.response.data)
      }
    })
}

export function onPut (api, data, getFunction) {
  data.editDialogErrorMessage = ''
  if (data.currentObject !== '') {
    axios.put(process.env.API_URL + api + data.currentObject.id + '/', data.currentObject)
      .then(resp => {
        data.loading = false
        data.currentObject = resp.data
        data.editDialog = false
        vuetifyToast.success(Vue.i18n.translate('Success'), { icon: 'check_circle_outline' })
        getFunction()
      })
      .catch(err => {
        console.log(err)
        if (err.response && err.response.data) {
          const errors = err.response.data
          for (const value in errors) {
            if (errors[value] instanceof Array) {
              data.editDialogErrorMessage = errors[value][0]
            } else {
              data.editDialogErrorMessage = errors[value]
            }
            vuetifyToast.error(Vue.i18n.translate('Error'), { icon: 'highlight_off' })
            console.log(err.response.data)
          }
        }
      })
  }
}

export function onDelete (api, data, getFunction) {
  data.deleteDialogErrorMessage = ''
  data.deleteDialog = false
  if (data.object !== '') {
    axios.delete(process.env.API_URL + api + data.currentObject.id + '/')
      .then(resp => {
        data.object = ''
        data.isSelected = false
        vuetifyToast.success(Vue.i18n.translate('Success'), { icon: 'check_circle_outline' })
        getFunction()
      })
      .catch(err => {
        console.log(err)
        vuetifyToast.error(Vue.i18n.translate('Error'), { icon: 'highlight_off' })
        if (err.response && err.response.data) {
          const errors = err.response.data
          for (const value in errors) {
            if (errors[value] instanceof Array) {
              data.deleteDialogErrorMessage = errors[value][0]
            } else {
              data.deleteDialogErrorMessage = errors[value]
            }
            console.log(err.response.data)
          }
        }
      })
  }
}

export function onGetCount (api, data) {
  data.loading = true
  axios.get(process.env.API_URL + api)
    .then(resp => {
      data.object = resp.data.count
      data.loading = false
    })
    .catch(err => {
      data.loading = false
      console.log(err)
    })
}

export function onGetSingle (api, name, data) {
  data.errorMessage = ''
  if (data[name] && data[name].id) {
    axios.get(process.env.API_URL + api + data[name].id + '/')
      .then(resp => {
        data.loading = false
        Vue.set(data, name, resp.data)
      })
      .catch(err => {
        console.log(err)
        if (err.response && err.response.data) {
          const errors = err.response.data
          for (const value in errors) {
            if (errors[value] instanceof Array) {
              data.errorMessage = errors[value][0]
            } else {
              data.errorMessage = errors[value]
            }
            console.log(err.response.data)
          }
        }
      })
  }
}

export function onPostSingle (api, data, getFunction) {
  data.errorMessage = ''
  axios.post(process.env.API_URL + api, data.currentObject)
    .then(resp => {
      data.loading = false
      data.currentObject = resp.data
      vuetifyToast.success(Vue.i18n.translate('Success'), { icon: 'check_circle_outline' })
      getFunction()
    })
    .catch((error) => {
      // Error
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        // console.log(error.response.data);
        // console.log(error.response.status);
        // console.log(error.response.headers);
        data.errorMessage = error.response.data
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        data.errorMessage = error.request
        console.log(error.request)
      } else {
        // Something happened in setting up the request that triggered an Error
        data.errorMessage = error.message
        console.log('Error', error.message)
      }
      vuetifyToast.error(Vue.i18n.translate('Error'), { icon: 'highlight_off' })
    })
}

export function onPutSingle (api, data, getFunction) {
  data.errorMessage = ''
  if (data.currentObject !== '') {
    axios.put(process.env.API_URL + api + data.currentObject.id + '/', data.currentObject)
      .then(resp => {
        data.loading = false
        data.currentObject = resp.data
        vuetifyToast.success(Vue.i18n.translate('Success'), { icon: 'check_circle_outline' })
        getFunction()
      })
      .catch((error) => {
        // Error
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          // console.log(error.response.data);
          // console.log(error.response.status);
          // console.log(error.response.headers);
          data.errorMessage = error.response.data
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // http.ClientRequest in node.js
          data.errorMessage = error.request
          console.log(error.request)
        } else {
          // Something happened in setting up the request that triggered an Error
          data.errorMessage = error.message
          console.log('Error', error.message)
        }
        vuetifyToast.error(Vue.i18n.translate('Error'), { icon: 'highlight_off' })
      })
  }
}
