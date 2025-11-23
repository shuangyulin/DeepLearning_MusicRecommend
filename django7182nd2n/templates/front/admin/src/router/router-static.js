import Vue from 'vue';
//配置路由
import VueRouter from 'vue-router'
Vue.use(VueRouter);
//1.创建组件
import Index from '@/views/index'
import Home from '@/views/home'
import Board from '@/views/board'
import Login from '@/views/login'
import NotFound from '@/views/404'
import UpdatePassword from '@/views/update-password'
import pay from '@/views/pay'
import register from '@/views/register'
import center from '@/views/center'
	import news from '@/views/modules/news/list'
	import yinleleixing from '@/views/modules/yinleleixing/list'
	import fensixinxi from '@/views/modules/fensixinxi/list'
	import yinlexinxi from '@/views/modules/yinlexinxi/list'
	import songinfo from '@/views/modules/songinfo/list'
	import gedaninfo from '@/views/modules/gedaninfo/list'
	import yonghu from '@/views/modules/yonghu/list'
	import discussyinlexinxi from '@/views/modules/discussyinlexinxi/list'
	import messages from '@/views/modules/messages/list'
	import config from '@/views/modules/config/list'
	import gequxinxi from '@/views/modules/gequxinxi/list'
	import gequxinxiforecast from '@/views/modules/gequxinxiforecast/list'
	import newstype from '@/views/modules/newstype/list'


//2.配置路由   注意：名字
export const routes = [{
	path: '/',
	name: '系统首页',
	component: Index,
	children: [{
		// 这里不设置值，是把main作为默认页面
		path: '/',
		name: '系统首页',
		component: Home,
		meta: {icon:'', title:'center', affix: true}
	}, {
		path: '/updatePassword',
		name: '修改密码',
		component: UpdatePassword,
		meta: {icon:'', title:'updatePassword'}
	}, {
		path: '/pay',
		name: '支付',
		component: pay,
		meta: {icon:'', title:'pay'}
	}, {
		path: '/center',
		name: '个人信息',
		component: center,
		meta: {icon:'', title:'center'}
	}
	,{
		path: '/news',
		name: '公告信息',
		component: news
	}
	,{
		path: '/yinleleixing',
		name: '音乐类型',
		component: yinleleixing
	}
	,{
		path: '/fensixinxi',
		name: '粉丝信息',
		component: fensixinxi
	}
	,{
		path: '/yinlexinxi',
		name: '音乐信息',
		component: yinlexinxi
	}
	,{
		path: '/songinfo',
		name: '歌曲信息',
		component: songinfo
	}
	,{
		path: '/gedaninfo',
		name: '歌单信息',
		component: gedaninfo
	}
	,{
		path: '/yonghu',
		name: '用户',
		component: yonghu
	}
	,{
		path: '/discussyinlexinxi',
		name: '音乐信息评论',
		component: discussyinlexinxi
	}
	,{
		path: '/messages',
		name: '留言板管理',
		component: messages
	}
	,{
		path: '/config',
		name: '轮播图管理',
		component: config
	}
	,{
		path: '/gequxinxi',
		name: '歌曲信息',
		component: gequxinxi
	}
	,{
		path: '/gequxinxiforecast',
		name: '播放数预测',
		component: gequxinxiforecast
	}
	,{
		path: '/newstype',
		name: '公告信息分类',
		component: newstype
	}
	]
	},
	{
		path: '/login',
		name: 'login',
		component: Login,
		meta: {icon:'', title:'login'}
	},
	{
		path: '/board',
		name: 'board',
		component: Board,
		meta: {icon:'', title:'board'}
	},
	{
		path: '/register',
		name: 'register',
		component: register,
		meta: {icon:'', title:'register'}
	},
	{
		path: '*',
		component: NotFound
	}
]
//3.实例化VueRouter  注意：名字
const router = new VueRouter({
	mode: 'hash',
	/*hash模式改为history*/
	routes // （缩写）相当于 routes: routes
})
const originalPush = VueRouter.prototype.push
//修改原型对象中的push方法
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}
export default router;
