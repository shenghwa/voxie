import { createRouter,createWebHistory} from 'vue-router';
 
const router = createRouter({
    routes: [
        {
            path: '/components/login',             
            component:()=>import('../components/login.vue'), 
            name: 'login'
        },
		{
		    path: '/components/register',             
		    component:()=>import('../components/register.vue'), 
		    name: 'register'
		},
		{
		    path: '/components/contact',             
		    component:()=>import('../components/contact.vue'), 
		    name: 'contact'
		},
		{
		    path: '/components/history',             
		    component:()=>import('../components/history.vue'), 
		    name: 'history'
		},
    ],
    history: createWebHistory()
})
export default router;