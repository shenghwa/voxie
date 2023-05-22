import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    login: 'Login',
    register: 'Register',
	service: 'Service',
	email: 'Email',
	password: 'password',
	new_account: 'Register new account',
	username: 'Username',
	send: 'Send',
	chat: 'Start to chat',
	upgrade: 'upgrade'
  },
  zh: {
    login: '登录',
    register: '注册',
	service: '客服',
	email: '邮箱',
	password: '密码',
	new_account: '注册新账户',
	username: '用户名',
	send: '发送',
	chat: '开始聊天',
	upgrade: '升级账户'
  }
}

const i18n = createI18n({
  locale: 'en', // 设置默认语言为英语
  messages // 引入翻译内容
})
 
const app = createApp(App)
app.use(router)
app.use(i18n)
app.mount('#app')
 
//此处也是vue3与vue2的区别之处
