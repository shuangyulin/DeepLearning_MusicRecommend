<template>
	<div>
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="'>'">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index"><a>{{item.name}}</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
	
		<div class="news-preview-pv">
			<el-form :inline="true" :model="formSearch" class="list-form-pv">
				<el-form-item class="search-item">
					<el-input v-model="title" placeholder="标题"></el-input>
				</el-form-item>
				<el-button class="search-btn" type="primary" @click="getNewsList(1)">
					<span class="icon iconfont icon-chakan5"></span>
					搜索
				</el-button>
			</el-form>
			
			<!-- category -->
			<div class="category-list">
				<div class="item" @click="categoryClick(0)" :class="categoryIndex == 0 ? 'active' : ''">全部</div>
				<div v-for="(item,index) in categoryList" @click="categoryClick(index+1)" :key="index" class="item" :class="categoryIndex == index+1 ? 'active' : ''">{{item.typename}}</div>
			</div>
			<div class="list10 index-pv1">
				<div v-for="(item,index) in newsList" :key="index" class="list-item animation-box" @click="toNewsDetail(item)">
					<div class="img">
						<img class="image" :src="baseUrl + item.picture" >
					</div>
					<div class="infoBox">
						<div class="infoLeft">
							<div class="name">{{item.title}}</div>
							<div class="time_item">
								<span class="icon iconfont icon-shijian21"></span>
								<span class="label">发布时间：</span>
								<span class="text">{{item.addtime.split(' ')[0]}}</span>
							</div>
							<div class="publisher_item">
								<span class="icon iconfont icon-geren16"></span>
								<span class="label">发布人：</span>
								<span class="text">{{item.name}}</span>
							</div>
							<div class="like_item">
								<span class="icon iconfont icon-zan10"></span>
								<span class="label">点赞：</span>
								<span class="text">{{item.thumbsupnum}}</span>
							</div>
							<div class="collect_item">
								<span class="icon iconfont icon-shoucang10"></span>
								<span class="label">收藏：</span>
								<span class="text">{{item.storeupnum}}</span>
							</div>
							<div class="view_item">
								<span class="icon iconfont icon-chakan2"></span>
								<span class="label">浏览次数：</span>
								<span class="text">{{item.clicknum}}</span>
							</div>
						</div>
						<div class="desc">{{item.introduction}}</div>
					</div>
				</div>
			</div>
		
			<el-pagination
				background
				id="pagination" class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				:page-sizes="pageSizes"
				prev-text="上一页"
				next-text="下一页"
				:hide-on-single-page="false"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				@current-change="curChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				></el-pagination>

			<!-- 热门信息 -->
			<div class="hot">
				<div class="hot-title">热门信息</div>
				<div class="hot-list">
					<div class="hot-item" v-for="item in hotList" :key="item.id" @click="toNewsDetail(item)">
						<img :src="baseUrl + item.picture" alt="">
						<div class="hot-name">{{ item.title }}</div>
						<div class="hot-time">{{item.addtime}}</div>
					</div>
				</div>
			</div>
			<div class="idea1"></div>
		</div>
	</div>
</template>

<script>
	export default {
		//数据集合
		data() {
			return {
				baseUrl: this.$config.baseUrl,
				breadcrumbItem: [
				  {
					name: '公告信息'
				  }
				],
				newsList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				layouts: '',
				title: '',
				categoryIndex: 0,
				categoryList: [],
				hotList: [],
			}
		},
		created() {
			this.getCategoryList()
			
			this.getHotList()
		},
		watch:{
			$route(newValue){
				this.getCategoryList()
			}
		},
		//方法集合
		methods: {
			getCategoryList(){
				this.$http.get('newstype/list', {}).then(res => {
					if (res.data.code == 0) {
						this.categoryList = res.data.data.list;
						if(this.$route.query.homeFenlei){
							for(let i=0;i<this.categoryList.length;i++) {
								if(this.$route.query.homeFenlei == this.categoryList[i].typename) {
									this.categoryIndex = i + 1;
									const currentRoute = this.$route;
									const routeWithoutQuery = { ...currentRoute };
									delete routeWithoutQuery.query;
									this.$router.replace(routeWithoutQuery)
									break;
								}
							}
						}
						this.getNewsList(1);
					}
				});
			},
			categoryClick(index) {
				this.categoryIndex = index
				this.getNewsList()
			},
			getNewsList(page) {
				let params = {page, limit: this.pageSize,sort:'addtime',order:'desc'};
				let searchWhere = {};
				if(this.title != '') searchWhere.title = '%' + this.title + '%';
				if(this.categoryIndex!=0){
					searchWhere.typename = this.categoryList[this.categoryIndex - 1].typename
				}
				this.$http.get('news/list', {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.newsList = res.data.data.list;
						this.total = res.data.data.total;
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			getHotList(){
				let params = {page:1, limit: 4,sort:'addtime',order:'desc'};
				this.$http.get('news/autoSort', {params: params}).then(res => {
					if (res.data.code == 0) {
						this.hotList = res.data.data.list;
					}
				});
			},
			curChange(page) {
				this.getNewsList(page);
			},
			prevClick(page) {
				this.getNewsList(page);
			},
			nextClick(page) {
				this.getNewsList(page);
			},
			toNewsDetail(item) {
				this.$router.push({path: '/index/newsDetail', query: {id: item.id}});
			}
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.news-preview-pv {
				margin: 0px auto;
				color: #333;
				background: none;
				display: flex;
				width: 1200px;
				font-size: 16px;
				justify-content: flex-start;
				align-items: flex-start;
				position: relative;
				flex-wrap: wrap;
				.list-form-pv {
						padding: 10px;
						background: none;
						display: flex;
						width: 100%;
						justify-content: center;
						align-items: center;
						flex-wrap: wrap;
						height: auto;
						.search-item {
								margin: 0 0px;
								.el-input {
										width: 100%;
									}
				.el-input /deep/ .el-input__inner {
										border: 1px solid #ccc;
										border-radius: 0px 0 0 0px;
										padding: 0 10px;
										margin: 0;
										color: #333;
										width: auto;
										font-size: 16px;
										border-width: 1px 0 1px 1px;
										line-height: 42px;
										min-width: 350px;
										height: 42px;
									}
			}
			.search-btn {
								cursor: pointer;
								border: 0;
								border-radius: 0 0px 0px 0;
								padding: 0px 15px;
								margin: 0 10px 0 0;
								color: #fff;
								background: #475a83;
								width: auto;
								font-size: inherit;
								line-height: 42px;
								height: 42px;
								.icon {
										margin: 0 3px 0 0;
										color: #fff;
										font-size: inherit;
									}
			}
		}
		.category-list {
						padding: 0px;
						margin: 40px 0px 0 0;
						background: #fff;
						display: flex;
						width: 100%;
						flex-wrap: wrap;
						height: auto;
						order: 6;
						.item {
								cursor: pointer;
								border: 0px solid #475a8350;
								padding: 10px 20px 10px 26px;
								margin: 0 10px 20px 0;
								color: inherit;
								display: flex;
								font-size: 16px;
								flex-wrap: wrap;
								clip-path: polygon(85% 0, 100% 50%, 85% 100%, 0% 100%, 15% 50%, 0% 0%);
								background: #eee;
								justify-content: center;
								align-items: center;
								min-width: 110px;
							}
			
			.item:hover {
								color: #fff;
								background: #475a83;
							}
			
			.item.active {
								clip-path: polygon(85% 0, 100% 50%, 85% 100%, 0% 100%, 15% 50%, 0% 0%);
								color: #fff;
								background: #475a83;
								font-size: 16px;
							}
		}
		.list10 {
						padding: 0;
						margin: 20px 0 0;
						color: #666;
						background: #fff;
						display: flex;
						width: 100%;
						font-size: 14px;
						justify-content: space-between;
						flex-wrap: wrap;
						height: auto;
						order: 8;
						.list-item {
								cursor: pointer;
								border: 0px solid #fff;
								padding: 0;
								margin: 0 0 20px;
								background: none;
								display: flex;
								width: 32%;
								position: relative;
								flex-wrap: wrap;
								height: auto;
								.img {
										padding: 0;
										overflow: hidden;
										width: 100%;
										height: 275px;
										img {
												object-fit: cover;
												display: block;
												width: 100%;
												height: 100%;
											}
				}
				.infoBox {
										padding: 10px;
										overflow: hidden;
										display: flex;
										width: 100%;
										flex-wrap: wrap;
										height: auto;
										.infoLeft {
												padding: 0;
												width: 100%;
												.name {
														padding: 0;
														overflow: hidden;
														color: #333;
														white-space: nowrap;
														font-weight: 600;
														display: inline-block;
														width: 100%;
														font-size: 16px;
														line-height: 30px;
														text-overflow: ellipsis;
													}
						.time_item {
														padding: 0 10px 0 0;
														display: inline-block;
														.icon {
																margin: 0 2px 0 0;
																display: none;
																line-height: 28px;
															}
							.label {
																line-height: 1.5;
															}
							.text {
																line-height: 1.5;
															}
						}
						.publisher_item {
														padding: 0 10px 0 0;
														display: inline-block;
														.icon {
																margin: 0 2px 0 0;
																display: none;
																line-height: 28px;
															}
							.label {
																line-height: 1.5;
															}
							.text {
																line-height: 28px;
															}
						}
						.like_item {
														padding: 0 10px 0 0;
														display: inline-block;
														.icon {
																margin: 0 2px 0 0;
																display: none;
																line-height: 28px;
															}
							.label {
																line-height: 1.5;
															}
							.text {
																line-height: 28px;
															}
						}
						.collect_item {
														padding: 0 10px 0 0;
														display: inline-block;
														.icon {
																margin: 0 2px 0 0;
																display: none;
																line-height: 28px;
															}
							.label {
																line-height: 1.5;
															}
							.text {
																line-height: 28px;
															}
						}
						.view_item {
														padding: 0 10px 0 0;
														display: inline-block;
														.icon {
																margin: 0 2px 0 0;
																display: none;
																line-height: 28px;
															}
							.label {
																line-height: 1.5;
															}
							.text {
																line-height: 28px;
															}
						}
					}
					.desc {
												margin: 10px 0 0;
												overflow: hidden;
												color: #666;
												width: 100%;
												font-size: 14px;
												line-height: 24px;
												height: 48px;
											}
				}
			}
			.list-item:hover {
								background: #475a83;
								.infoBox {
					.infoLeft {
						.name {
														color: #fff;
													}
						.time_item {
							.icon {
																color: #fff;
															}
							.label {
																color: #fff;
															}
							.text {
																color: #fff;
															}
						}
						.publisher_item {
							.icon {
																color: #fff;
															}
							.label {
																color: #fff;
															}
							.text {
																color: #fff;
															}
						}
						.like_item {
							.icon {
																color: #fff;
															}
							.label {
																color: #fff;
															}
							.text {
																color: #fff;
															}
						}
						.collect_item {
							.icon {
																color: #fff;
															}
							.label {
																color: #fff;
															}
							.text {
																color: #fff;
															}
						}
						.view_item {
							.icon {
																color: #fff;
															}
							.label {
																color: #fff;
															}
							.text {
																color: #fff;
															}
						}
					}
					.desc {
												color: #fff;
											}
				}
			}
		}
		.hot {
						background: none;
						width: 100%;
						height: auto;
						order: 80;
						.hot-title {
								padding: 0 0 20px;
								margin: 0 0 20px;
								color: #333;
								background: url(http://codegen.caihongy.cn/20240921/d1174ef38e674130b0bd28e07897ab45.png) no-repeat center bottom;
								width: 100%;
								font-size: 26px;
								position: relative;
								text-align: center;
							}
			.hot-list {
								padding: 0;
								background: none;
								display: flex;
								width: 100%;
								justify-content: space-between;
								flex-wrap: wrap;
								height: auto;
								.hot-item {
										cursor: pointer;
										border: 1px dashed #ddd;
										padding: 10px;
										margin: 0 0 20px;
										background: #fff;
										display: inline-block;
										width: calc(50% - 10px);
										height: auto;
										img {
												object-fit: cover;
												display: block;
												width: 110px;
												float: left;
												height: 110px;
											}
					.hot-name {
												padding: 4px 5px 0;
												overflow: hidden;
												color: #333;
												white-space: nowrap;
												width: calc(100% - 120px);
												font-size: 15px;
												line-height: 30px;
												text-overflow: ellipsis;
												float: right;
											}
					.hot-time {
												padding: 0 5px;
												color: #999;
												font-weight: 500;
												display: inline-block;
												width: calc(100% - 120px);
												font-size: inherit;
												line-height: 24px;
												float: right;
												text-align: right;
											}
				}
			}
		}
		.idea1 {
						background: #fff;
						width: 100%;
						height: 1px;
						order: 10;
					}
	}
	
	.index-pv1 .animation-box {
		transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
		z-index: initial;
	}
	
	.index-pv1 .animation-box:hover {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
	}
	
	.index-pv1 .animation-box img {
		transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
	}
	
	.index-pv1 .animation-box img:hover {
				transform: rotate(0deg) scale(0.98) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
</style>
