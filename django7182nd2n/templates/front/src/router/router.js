import VueRouter from 'vue-router'
//引入组件
import Index from '../pages'
import Home from '../pages/home/home'
import Login from '../pages/login/login'
import Register from '../pages/register/register'
import Center from '../pages/center/center'
import Messages from '../pages/messages/list'
import Storeup from '../pages/storeup/list'
import News from '../pages/news/news-list'
import NewsDetail from '../pages/news/news-detail'
import payList from '../pages/pay'

import yonghuList from '../pages/yonghu/list'
import yonghuDetail from '../pages/yonghu/detail'
import yonghuAdd from '../pages/yonghu/add'
import yinleleixingList from '../pages/yinleleixing/list'
import yinleleixingDetail from '../pages/yinleleixing/detail'
import yinleleixingAdd from '../pages/yinleleixing/add'
import yinlexinxiList from '../pages/yinlexinxi/list'
import yinlexinxiDetail from '../pages/yinlexinxi/detail'
import yinlexinxiAdd from '../pages/yinlexinxi/add'
import gequxinxiList from '../pages/gequxinxi/list'
import gequxinxiDetail from '../pages/gequxinxi/detail'
import gequxinxiAdd from '../pages/gequxinxi/add'
import fensixinxiList from '../pages/fensixinxi/list'
import fensixinxiDetail from '../pages/fensixinxi/detail'
import fensixinxiAdd from '../pages/fensixinxi/add'
import gedaninfoList from '../pages/gedaninfo/list'
import gedaninfoDetail from '../pages/gedaninfo/detail'
import gedaninfoAdd from '../pages/gedaninfo/add'
import songinfoList from '../pages/songinfo/list'
import songinfoDetail from '../pages/songinfo/detail'
import songinfoAdd from '../pages/songinfo/add'
import gequxinxiforecastList from '../pages/gequxinxiforecast/list'
import gequxinxiforecastDetail from '../pages/gequxinxiforecast/detail'
import gequxinxiforecastAdd from '../pages/gequxinxiforecast/add'
import newstypeList from '../pages/newstype/list'
import newstypeDetail from '../pages/newstype/detail'
import newstypeAdd from '../pages/newstype/add'
import discussyinlexinxiList from '../pages/discussyinlexinxi/list'
import discussyinlexinxiDetail from '../pages/discussyinlexinxi/detail'
import discussyinlexinxiAdd from '../pages/discussyinlexinxi/add'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

//配置路由
export default new VueRouter({
	routes:[
		{
      path: '/',
      redirect: '/index/home'
    },
		{
			path: '/index',
			component: Index,
			children:[
				{
					path: 'home',
					component: Home
				},
				{
					path: 'center',
					component: Center,
				},
				{
					path: 'pay',
					component: payList,
				},
				{
					path: 'messages',
					component: Messages
				},
				{
					path: 'storeup',
					component: Storeup
				},
				{
					path: 'news',
					component: News
				},
				{
					path: 'newsDetail',
					component: NewsDetail
				},
				{
					path: 'yonghu',
					component: yonghuList
				},
				{
					path: 'yonghuDetail',
					component: yonghuDetail
				},
				{
					path: 'yonghuAdd',
					component: yonghuAdd
				},
				{
					path: 'yinleleixing',
					component: yinleleixingList
				},
				{
					path: 'yinleleixingDetail',
					component: yinleleixingDetail
				},
				{
					path: 'yinleleixingAdd',
					component: yinleleixingAdd
				},
				{
					path: 'yinlexinxi',
					component: yinlexinxiList
				},
				{
					path: 'yinlexinxiDetail',
					component: yinlexinxiDetail
				},
				{
					path: 'yinlexinxiAdd',
					component: yinlexinxiAdd
				},
				{
					path: 'gequxinxi',
					component: gequxinxiList
				},
				{
					path: 'gequxinxiDetail',
					component: gequxinxiDetail
				},
				{
					path: 'gequxinxiAdd',
					component: gequxinxiAdd
				},
				{
					path: 'fensixinxi',
					component: fensixinxiList
				},
				{
					path: 'fensixinxiDetail',
					component: fensixinxiDetail
				},
				{
					path: 'fensixinxiAdd',
					component: fensixinxiAdd
				},
				{
					path: 'gedaninfo',
					component: gedaninfoList
				},
				{
					path: 'gedaninfoDetail',
					component: gedaninfoDetail
				},
				{
					path: 'gedaninfoAdd',
					component: gedaninfoAdd
				},
				{
					path: 'songinfo',
					component: songinfoList
				},
				{
					path: 'songinfoDetail',
					component: songinfoDetail
				},
				{
					path: 'songinfoAdd',
					component: songinfoAdd
				},
				{
					path: 'gequxinxiforecast',
					component: gequxinxiforecastList
				},
				{
					path: 'gequxinxiforecastDetail',
					component: gequxinxiforecastDetail
				},
				{
					path: 'gequxinxiforecastAdd',
					component: gequxinxiforecastAdd
				},
				{
					path: 'newstype',
					component: newstypeList
				},
				{
					path: 'newstypeDetail',
					component: newstypeDetail
				},
				{
					path: 'newstypeAdd',
					component: newstypeAdd
				},
				{
					path: 'discussyinlexinxi',
					component: discussyinlexinxiList
				},
				{
					path: 'discussyinlexinxiDetail',
					component: discussyinlexinxiDetail
				},
				{
					path: 'discussyinlexinxiAdd',
					component: discussyinlexinxiAdd
				},
			]
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/register',
			component: Register
		},
	]
})
