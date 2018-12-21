import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import People from '../components/People.vue'
import Actions from '../components/Actions.vue'
import Reports from '../components/Reports.vue'
import Directories from '../components/directories/Directories.vue'
import PeopleDetails from '../components/PeopleDetails.vue'
import ImportUsers from '../components/ImportUsers.vue'
import ResetPasswordEmail from '../components/ResetPasswordEmail'
import ResetPasswordConfirm from '../components/ResetPasswordConfirm'
import Organizations from '../components/directories/Organizations'
import Units from '../components/directories/Units'
import Positions from '../components/directories/Positions'
import Categories from '../components/directories/Categories'
import Countries from '../components/directories/Countries'
import Regions from '../components/directories/Regions'
import Cities from '../components/directories/Cities'
import Competencies from '../components/directories/Competencies'
import Courses from '../components/directories/Courses'
import Payments from '../components/directories/Payments'
import ExportUsers from '../components/ExportUsers'

Vue.use(Router)

let router = new Router({
  mode: 'history',
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
