import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'
import Login from '../views/Login.vue'
import Crm from '../views/Crm.vue'
import Zdravniza from '../views/Zdravniza.vue'
import SelectProgram from '../views/SelectProgram.vue'
import ActionList from '../views/ActionList.vue'
import ReportList from '../views/ReportList.vue'
import ImportUsers from '../views/ImportUsers.vue'
import ResetPasswordEmail from '../views/ResetPasswordEmail'
import ResetPasswordConfirm from '../views/ResetPasswordConfirm'
import ExportUsers from '../views/ExportUsers'
import ExportLeads from '../views/ExportLeads'
import ResourceList from '../views/ResourceList'
import ResourceAdd from '../views/ResourceAdd'
import ResourceEdit from '../views/ResourceEdit'
import ResourceDetail from '../views/ResourceDetail'
import Appointment from '../views/Appointment'
import Lead from '../views/Lead'

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
      name: 'crm',
      component: Crm,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/zdravniza',
      name: 'zdravniza',
      component: Zdravniza,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/report/list',
      name: 'reportlist',
      component: ReportList,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/action/list',
      name: 'actionlist',
      component: ActionList,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/:resource/list',
      name: 'list',
      component: ResourceList,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/:resource/add',
      name: 'addfirst',
      component: ResourceAdd,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/:resource/add/:id',
      name: 'add',
      component: ResourceAdd,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/:resource/edit/:id',
      name: 'edit',
      component: ResourceEdit,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:program/:resource/detail/:id',
      name: 'detail',
      component: ResourceDetail,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/open/zdravniza/appointment',
      name: 'appointment',
      component: Appointment,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/open/crm/lead',
      name: 'lead',
      component: Lead,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/crm/import/user',
      name: 'importUsers',
      component: ImportUsers,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/crm/export/user',
      name: 'exportUsers',
      component: ExportUsers,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/crm/export/lead',
      name: 'exportLeads',
      component: ExportLeads,
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
