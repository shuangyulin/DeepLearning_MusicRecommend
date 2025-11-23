export default {
	baseUrl: 'http://localhost:8080/django7182nd2n/',
	name: '/django7182nd2n',
	indexNav: [
// frontMenu com.jlwl.entity.Menu@2ec1fb81
		{
			name: '音乐信息',
			url: '/index/yinlexinxi',
		},
// frontMenu com.jlwl.entity.Menu@7127ccde
		{
			name: '歌曲信息',
			url: '/index/gequxinxi',
		},
// frontMenu com.jlwl.entity.Menu@1c5b8e0b
		{
			name: '粉丝信息',
			url: '/index/fensixinxi',
		},
// frontMenu com.jlwl.entity.Menu@4f4b9946
		{
			name: '歌单信息',
			url: '/index/gedaninfo',
		},
		{
			name: '公告信息',
			url: '/index/news'
		},
		{
			name: '留言板',
			url: '/index/messages'
		},
	],
	cateList: [
		{
			name: '音乐信息',
			refTable: 'yinleleixing',
			refColumn: 'yinleleixing',
		},
		{
			name: '公告信息',
			refTable: 'newstype',
			refColumn: 'typename',
		},
	]
}
