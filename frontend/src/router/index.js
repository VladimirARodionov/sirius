import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import SelectProgram from '../views/SelectProgram.vue'
import Actions from '../views/Actions.vue'
import Reports from '../views/Reports.vue'
import ImportUsers from '../views/ImportUsers.vue'
import ResetPasswordEmail from '../views/ResetPasswordEmail'
import ResetPasswordConfirm from '../views/ResetPasswordConfirm'
import ExportUsers from '../views/ExportUsers'
import ResourceList from '../views/ResourceList'
import ResourceAdd from '../views/ResourceAdd'
import ResourceEdit from '../views/ResourceEdit'
import ResourceDetail from '../views/ResourceDetail'

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
      name: 'selectprogram',
      component: SelectProgram,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/crm',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:resource/list',
      name: 'list',
      component: ResourceList,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:resource/add',
      name: 'addfirst',
      component: ResourceAdd,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:resource/add/:id',
      name: 'add',
      component: ResourceAdd,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:resource/edit/:id',
      name: 'edit',
      component: ResourceEdit,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:resource/detail/:id',
      name: 'detail',
      component: ResourceDetail,
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
