import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import People from '../views/People.vue'
import Actions from '../views/Actions.vue'
import Reports from '../views/Reports.vue'
import Directories from '../views/directories/Directories.vue'
import PeopleDetails from '../views/PeopleDetails.vue'
import ImportUsers from '../views/ImportUsers.vue'
import ResetPasswordEmail from '../views/ResetPasswordEmail'
import ResetPasswordConfirm from '../views/ResetPasswordConfirm'
import Organizations from '../views/directories/Organizations'
import Units from '../views/directories/Units'
import Positions from '../views/directories/Positions'
import Categories from '../views/directories/Categories'
import Countries from '../views/directories/Countries'
import Regions from '../views/directories/Regions'
import Cities from '../views/directories/Cities'
import Competencies from '../views/directories/Competencies'
import Courses from '../views/directories/Courses'
import Payments from '../views/directories/Payments'
import ExportUsers from '../views/ExportUsers'
import Addresses from '../views/directories/Addresses'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  base: '/sirius',
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/login/reset',
      name: 'resetPassword',
      component: ResetPasswordEmail
    },
    {
      path: '/login/:uidb64/:token/reset',
      name: 'resetPasswordConfirm',
      component: ResetPasswordConfirm
    },
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/people',
      name: 'people',
      component: People,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/reports',
      name: 'reports',
      component: Reports,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/actions',
      name: 'actions',
      component: Actions,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/actions/import/users',
      name: 'importUsers',
      component: ImportUsers,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/actions/export/users',
      name: 'exportUsers',
      component: ExportUsers,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories',
      name: 'directories',
      component: Directories,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/organizations',
      name: 'organizations',
      component: Organizations,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/units',
      name: 'units',
      component: Units,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/positions',
      name: 'positions',
      component: Positions,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/categories',
      name: 'categories',
      component: Categories,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/competencies',
      name: 'competencies',
      component: Competencies,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/countries',
      name: 'countries',
      component: Countries,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/regions',
      name: 'regions',
      component: Regions,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/cities',
      name: 'cities',
      component: Cities,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/addresses',
      name: 'addresses',
      component: Addresses,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/courses',
      name: 'courses',
      component: Courses,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/directories/payments',
      name: 'payments',
      component: Payments,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/people/:id/details',
      name: 'peopleDetails',
      component: PeopleDetails,
      meta: {
        requiresAuth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login')
  } else {
    next()
  }
})

export default router
