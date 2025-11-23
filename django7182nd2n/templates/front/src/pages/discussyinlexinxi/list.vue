<template>
	<div>
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="'>'">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index"><a>{{item.name}}</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-jiantou33"></span>
				<span class="text">返回</span>
			</el-button>
		</div>
		<div class="list-preview">
			<el-form :inline="true" :model="formSearch" class="list-form-pv">
				<el-form-item class="list-item">
					<div class="lable">用户名：</div>
					<el-input v-model="formSearch.nickname" placeholder="用户名" @keydown.enter.native="getList(1, curFenlei)" clearable></el-input>
				</el-form-item>
				<el-form-item class="list-item">
					<div class="lable">评论内容：</div>
					<el-input v-model="formSearch.content" placeholder="评论内容" @keydown.enter.native="getList(1, curFenlei)" clearable></el-input>
				</el-form-item>
				<el-button class="list-search-btn" v-if=" true " type="primary" @click="getList(1, curFenlei)">
					查询
				</el-button>
				<el-button class="list-add-btn" v-if="btnAuth('discussyinlexinxi','新增')" type="primary" @click="add('/index/discussyinlexinxiAdd')">
					添加
				</el-button>
			</el-form>
			<div class="select2">
				<div class="select2-list" v-for="(item,index) in selectOptionsList" :key="index">
					<div class="label">{{item.name}}：</div>
					<div class="item-body">
						<div class="item" @click="selectClick2(item,-1)" :class="item.check ==-1 ? 'active' : ''">全部</div>
						<div class="item" @click="selectClick2(item,index1)" :class="item.check == index1 ? 'active' : ''" v-for="item1,index1 in item.list" :key="index1">{{item1}}</div>
					</div>
				</div>
			</div>
			<div class="list">
				<div class="list6">
					<div v-for="(item,index) in dataList" :key="index" :class="'list-item' + ((index%2) + 1)" @click.stop="toDetail(item)">
						<div class="imgbox">
						</div>
						<div class="infoBox">
							<div class="centerInfo">
							</div>
							<div class="bottomInfo">
								<div class="time_item">
									<span class="icon iconfont" :class="index%2==0?'icon-shijian21':'icon-shijian21'"></span>
									<span class="label">{{index%2==0?'发布时间：':'发布时间：'}}</span>
									<span class="text">{{index%2==0? item.addtime.split(' ')[0]: item.addtime.split(' ')[0]}}</span>
								</div>
								<div class="more_btn" @click.stop="toDetail(item)">
									<span class="text">{{index%2==0?'详情':'详情'}}</span>
									<span class="icon iconfont" :class="index%2==0?'icon-jiantou25':'icon-jiantou25'"></span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

	
			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				prev-text="上一页"
				next-text="下一页"
				:hide-on-single-page="false"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				:page-sizes="pageSizes"
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				></el-pagination>
			<div class="idea1"></div>
		</div>
		<el-dialog title="预览图" :visible.sync="previewVisible" width="50%">
			<img :src="previewImg" alt="" style="width: 100%;">
		</el-dialog>
	</div>
</template>
<script>
	export default {
		//数据集合
		data() {
			return {
				selectIndex2: 0,
				selectOptionsList: [],
				layouts: '',
				swiperIndex: -1,
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '音乐信息评论表'
					}
				],
				formSearch: {
					nickname: '',
					content: '',
				},
				fenlei: [],
				feileiColumn: '',
				dataList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				curFenlei: '全部',
				isPlain: false,
				indexQueryCondition: '',
				timeRange: [],
				centerType:false,
				previewImg: '',
				previewVisible: false,
				sortType: 'id',
				sortOrder: 'desc',
			}
		},
		async created() {
			if(this.$route.query.centerType&&this.$route.query.centerType!=0){
				this.centerType = true
			}
			this.baseUrl = this.$config.baseUrl;
			await this.getFenlei();
			let fenlei = '全部'
			if(this.$route.query.homeFenlei){
				fenlei = this.$route.query.homeFenlei
			}
			this.getList(1, fenlei);
		},
		watch:{
			$route(newValue){
				this.getList(1, newValue.query.homeFenlei);
			}
		},
		//方法集合
		methods: {
			selectClick2(row,index) {
				row.check = index
				if(index == -1){
					this.formSearch[row.tableName] = ''
				}else {
					this.formSearch[row.tableName] = row.list[index]
				}
				this.getList()
			},
			add(path) {
				let query = {}
				if(this.centerType){
					query.centerType = 1
				}
				this.$router.push({path: path,query:query});
			},
			async getFenlei() {
			},
			getList(page, fenlei, ref = '') {
				let params = {
					page,
					limit: this.pageSize,
				};
				let searchWhere = {};
				if (this.formSearch.nickname != '') searchWhere.nickname = '%' + this.formSearch.nickname + '%';
				if (this.formSearch.content != '') searchWhere.content = '%' + this.formSearch.content + '%';
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`discussyinlexinxi/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.dataList = res.data.data.list;
						this.total = Number(res.data.data.total);
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			sortClick(type){
				if(this.sortType==type){
					if(this.sortOrder == 'desc'){
						this.sortOrder = 'asc'
					}else{
						this.sortOrder = 'desc'
					}
				}else{
					this.sortType = type
					this.sortOrder = 'desc'
				}
				this.getList(1, '全部')
			},
			curChange(page) {
				this.getList(page);
			},
			prevClick(page) {
				this.getList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getList(1);
			},
			nextClick(page) {
				this.getList(page);
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
			},
			toDetail(item) {
				let params = {
					id: item.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/discussyinlexinxiDetail', query: params});
			},
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			backClick() {
				this.$router.push({path: '/index/center'});
			},
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.list-preview {
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
			padding: 0;
			margin: 20px 0;
			color: inherit;
			background: none;
			display: flex;
			width: 100%;
			font-size: inherit;
			flex-wrap: wrap;
			height: auto;
			.list-item {
				padding: 0;
				margin: 0 0px 10px 0;
				display: flex;
				font-size: inherit;
				align-items: center;
				flex-wrap: wrap;
				/deep/.el-form-item__content {
					display: flex;
				}
				.lable {
					padding: 0 10px;
					color: #333;
					white-space: nowrap;
					display: inline-block;
					width: auto;
					font-size: 16px;
					line-height: 40px;
				}
				.el-input {
					width: auto;
				}
				.datetimerange {
					border: 1px solid #ccc;
					border-radius: 8px;
					padding: 3px 3px;
					background: #fff;
					width: auto;
					justify-content: center;
				}
				.el-input /deep/ .el-input__inner {
					border: 1px solid #ccc;
					border-radius: 4px;
					padding: 0 10px;
					margin: 0 5px 0 0;
					color: #333;
					width: auto;
					font-size: 16px;
					line-height: 40px;
					height: 40px;
				}
				.el-select {
					width: 100%;
				}
				.el-select /deep/ .el-input__inner {
				}
				.el-date-editor {
					width: auto;
				}
				.el-date-editor /deep/ .el-input__inner {
					border: 1px solid #ccc;
					border-radius: 4px;
					padding: 0 0px 0 30px;
					margin: 0;
					color: #333;
					width: auto;
					font-size: 16px;
					line-height: 40px;
					height: 40px;
				}
			}
			.list-search-btn {
				cursor: pointer;
				border: 0;
				border-radius: 4px;
				padding: 0px 15px;
				margin: 0 10px 0 10px;
				color: #fff;
				background: #475a83;
				width: auto;
				font-size: inherit;
				line-height: 40px;
				height: 40px;
				i {
					margin: 0 10px 0 0;
					color: #fff;
					font-size: inherit;
				}
			}
			.list-add-btn {
				cursor: pointer;
				border: 0;
				border-radius: 4px;
				padding: 0px 15px;
				margin: 0 10px 0 0;
				color: #333;
				background: #e6cca6;
				width: auto;
				font-size: inherit;
				line-height: 40px;
				height: 40px;
				i {
					margin: 0 10px 0 0;
					color: #fff;
					font-size: inherit;
				}
			}
		}
		.select2 {
			border: 1px solid #999;
			padding: 10px;
			margin: 10px auto 0;
			background: none;
			width: 100%;
			font-size: 15px;
			height: auto;
			.select2-list {
				padding: 5px 5px;
				margin: 0 0 10px;
				background: none;
				width: 100%;
				height: auto;
				.label {
					padding: 0 5px;
					color: #333;
					font-weight: 500;
					display: inline-block;
					font-size: inherit;
					line-height: 32px;
				}
				.item-body {
					display: inline-block;
					width: auto;
					flex-wrap: wrap;
					height: auto;
					.item {
						border-radius: 4px;
						padding: 0 5px;
						color: inherit;
						background: none;
						display: inline-block;
						font-size: inherit;
						line-height: 32px;
						text-align: center;
						min-width: 50px;
					}
					.item:hover {
						cursor: pointer;
						color: #333;
						background: #475a8330;
					}
					.item.active {
						cursor: pointer;
						color: #333;
						background: #475a8330;
						display: inline-block;
						min-width: 50px;
						text-align: center;
					}
				}
			}
		}
		.sort_view {
			padding: 5px 20px;
			margin: 0px auto 20px;
			color: inherit;
			background: none;
			width: 100%;
			font-size: inherit;
			border-color: #eee;
			border-width: 1px;
			border-style: outset;
			order: 3;
			.click-sort-btn {
				border: 0;
				border-radius: 8px;
				padding: 0 5px;
				margin: 0 5px;
				color: inherit;
				background: none;
				font-size: inherit;
				.icon {
					margin: 0 2px 0 0;
					color: inherit;
					font-size: inherit;
					line-height: 40px;
				}
				.text {
					color: inherit;
					font-size: inherit;
					line-height: 40px;
				}
			}
		}
		.list {
			margin: 0px 0 0;
			overflow: hidden;
			background: #fff;
			width: calc(100% - 0px);
			clear: both;
			font-size: 15px;
			order: 8;
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
				
			.index-pv1 .animation-box:hover {
				transform: rotate(0) scale(1.2) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
				
			.index-pv1 .animation-box img {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
			}
			
			.index-pv1 .animation-box img:hover {
				transform: rotate(0) scale(0.8) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list6 {
				margin: 20px auto 0;
				overflow: hidden;
				display: flex;
				width: 100%;
				clear: both;
				justify-content: space-between;
				flex-wrap: wrap;
				.list-item1 {
					margin: 0 0 30px;
					display: flex;
					width: 49%;
					border-color: #ddd;
					border-width: 0px;
					border-style: solid;
					height: 250px;
					.imgbox {
						overflow: hidden;
						width: 50%;
						float: left;
						height: 100%;
						.image {
							object-fit: cover;
							width: 100%;
							transition: all 0.6s;
							height: 100%;
						}
					}
					.infoBox {
						padding: 10px 10px 10px 20px;
						flex-direction: column;
						background: #475a8310;
						flex: 1;
						display: flex;
						width: 50%;
						justify-content: center;
						position: relative;
						float: right;
						flex-wrap: wrap;
						height: 100%;
						.name {
							border: 0px solid #eee;
							padding: 0;
							color: #333;
							background: none;
							font-weight: normal;
							width: 100%;
							font-size: 15px;
							line-height: 24px;
						}
						.price {
							margin: 0px 0 0;
							color: #f00;
							font-size: 16px;
							line-height: 1.5;
							.price_text {
								font-size: 20px;
							}
						}
						.centerInfo {
							padding: 5px 0;
							margin: 0px 0 0;
							color: #666;
							display: flex;
							width: 100%;
							font-size: 14px;
							flex-wrap: wrap;
							.publisher_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
						}
						.bottomInfo {
							margin: 0px 0 0;
							display: flex;
							justify-content: space-between;
							align-items: center;
							flex-wrap: wrap;
							.time_item {
								padding: 0;
								color: #666;
								font-size: 14px;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.more_btn {
								border: 0px solid #fff;
								border-radius: 20px;
								padding: 0px;
								background: none;
								display: none;
								width: 100%;
								text-align: right;
								.text {
									color: #999;
								}
								.icon {
									color: #999;
								}
							}
						}
					}
				}
				.list-item1:hover {
					cursor: pointer;
					background: none;
					.imgbox {
						.image {
							transform: scale(1.05);
						}
					}
					.infoBox {
						background: #475a83;
						.name {
							border: 0px solid #ffffff50;
							color: #fff;
							background: none;
						}
						.price {
							color: #fff;
							.price_text {
							}
						}
						.centerInfo {
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
						.bottomInfo {
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
							.more_btn {
								.text {
									color: #333;
								}
								.icon {
									color: #333;
								}
							}
						}
					}
				}
				.list-item2 {
					margin: 0 0 30px;
					display: flex;
					width: 49%;
					border-color: #ddd;
					border-width: 0px;
					border-style: solid;
					height: 250px;
					.imgbox {
						overflow: hidden;
						width: 50%;
						float: right;
						height: 100%;
						order: 2;
						.image {
							object-fit: cover;
							width: 100%;
							transition: all 0.6s;
							height: 100%;
						}
					}
					.infoBox {
						padding: 10px 10px 10px 20px;
						flex-direction: column;
						background: #475a8310;
						flex: 1;
						display: flex;
						width: 50%;
						justify-content: center;
						position: relative;
						float: left;
						flex-wrap: wrap;
						height: 100%;
						.name {
							border: 0px solid #eee;
							padding: 0;
							color: #333;
							background: none;
							font-weight: normal;
							width: 100%;
							font-size: 15px;
							line-height: 24px;
						}
						.price {
							margin: 0px 0 0;
							color: #f00;
							font-size: 16px;
							line-height: 1.5;
							.price_text {
								font-size: 20px;
							}
						}
						.centerInfo {
							padding: 5px 0;
							margin: 0px 0 0;
							color: #666;
							display: flex;
							width: 100%;
							font-size: 14px;
							flex-wrap: wrap;
							.publisher_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0;
								display: inline-block;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
						}
						.bottomInfo {
							margin: 0px 0 0;
							display: flex;
							justify-content: space-between;
							align-items: center;
							flex-wrap: wrap;
							.time_item {
								padding: 0;
								color: #666;
								font-size: 14px;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									display: none;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.more_btn {
								border: 0px solid #fff;
								border-radius: 20px;
								padding: 0;
								display: none;
								width: 100%;
								text-align: right;
								.text {
									color: inherit;
									font-size: inherit;
								}
								.icon {
									color: inherit;
									font-size: inherit;
								}
							}
						}
					}
				}
				.list-item2:hover {
					cursor: pointer;
					background: none;
					.imgbox {
						.image {
							transform: scale(1.05);
						}
					}
					.infoBox {
						background: #475a83;
						.name {
							border: 0px solid #ffffff50;
							color: #fff;
							background: none;
						}
						.price {
							color: #fff;
							.price_text {
							}
						}
						.centerInfo {
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
						.bottomInfo {
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
							.more_btn {
								.text {
									color: #333;
								}
								.icon {
									color: #333;
								}
							}
						}
					}
				}
			}
		}
		.idea1 {
			background: #fff;
			width: 100%;
			order: 6;
			height: 1px;
		}
	}
</style>
