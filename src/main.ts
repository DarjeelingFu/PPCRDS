import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { createNotivue } from 'notivue'

import './style.css'

import './demos/ipc'
// If you want use Node.js, the`nodeIntegration` needs to be enabled in the Main process.
// import './demos/node'

import Main from './components/Main.vue'
import About from './components/About.vue'

const routes = [
    { name: 'root', path: '/', component: Main },
    { name: 'about', path: '/about', component: About }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes
})

import 'notivue/notification.css' // Only needed if using built-in <Notification />
import 'notivue/animations.css' // Only needed if using default animations

const notivue = createNotivue(/* Options */)

const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus)
app.use(router)
app.use(notivue)
app.mount('#app').$nextTick(() => {postMessage({ payload: 'removeLoading' }, '*')})
