import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import People from '../components/People.vue'
// import Actions from '../components/Actions.vue'
import Reports from '../components/Reports.vue'
import Directories from '../components/Directories.vue'
import PeopleDetails from '../components/PeopleDetails.vue'
import ImportUsers from '../components/ImportUsers.vue'
import ResetPasswordEmail from '../components/ResetPasswordEmail'
import ResetPasswordConfirm from '../components/ResetPasswordConfirm'
import Organizations from '../components/Organizations'
import Units from '../components/Units'

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
      component: ImportUsers,
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
