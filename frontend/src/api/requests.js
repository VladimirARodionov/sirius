import axios from 'axios'

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
        getFunction()
      })
      .catch(err => {
        console.log(err)
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

export function onGetSingle (api, data) {
  data.errorMessage = ''
  if (data.currentObject.id) {
    axios.get(process.env.API_URL + api + data.currentObject.id + '/')
      .then(resp => {
        data.loading = false
        data.currentObject = resp.data
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
      getFunction()
    })
    .catch(err => {
      if (err.response && err.response.data) {
        const errors = err.response.data
        for (const value in errors) {
          if (errors[value] instanceof Array) {
            data.errorMessage = errors[value][0]
          } else {
            data.errorMessage = errors[value]
          }
        }
        console.log(err.response.data)
      }
    })
}

export function onPutSingle (api, data, getFunction) {
  data.errorMessage = ''
  if (data.currentObject !== '') {
    axios.put(process.env.API_URL + api + data.currentObject.id + '/', data.currentObject)
      .then(resp => {
        data.loading = false
        data.currentObject = resp.data
        getFunction()
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
