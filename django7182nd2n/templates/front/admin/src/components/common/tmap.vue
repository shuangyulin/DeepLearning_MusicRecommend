<template>
	<div class="mapComponents" id="container"></div>
</template>

<script>
	import AMapLoader from "@amap/amap-jsapi-loader";
	window._AMapSecurityConfig = {
	  securityJsCode: "4d8f1bda690b722d8a547dabb51a9933",
	};
	export default {
		data() {
			return {
				map: null,
			}
		},
		mounted() {
			// this.initAMap();
		},
		props: ['longitude1','longitude2','latitude1','latitude2'],
		methods: {
			mapClose(){
				console.log(11)
				this.map.destroy();
			},
			initAMap(longitude1,longitude2,latitude1,latitude2) {
				let that = this
				AMapLoader.reset()
				AMapLoader.load({
						key: "5c1c06db19e483c5b00dc052ca37848b", // 申请好的Web端开发者Key，首次调用 load 时必填
						version: "2.0", // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
						// plugins: ['AMap.Driving'], // 需要使用的的插件列表，如比例尺'AMap.Scale'等
					})
					.then((AMap) => {
						this.map = new AMap.Map("container", {
							// 设置地图容器id
							// viewMode: "3D", // 是否为3D地图模式
							zoom: 14, // 初始化地图级别
							center: [longitude1, latitude1], //地图显示中心点坐标
						});
						if(longitude1&&longitude2&&latitude1&&latitude2){
							AMap.plugin('AMap.Driving',
								function() {
									var driving = new AMap.Driving({
										map: that.map,
									}); //驾车路线规划
									driving.search(
										new AMap.LngLat(longitude1, latitude1),
										new AMap.LngLat(longitude2, latitude2),
										function(status, result) {
											console.log(status)
											// result 即是对应的驾车导航信息，相关数据结构文档请参考  https://lbs.amap.com/api/javascript-api/reference/route-search#m_DrivingResult
											if (status === "complete") {
												console.log("绘制驾车路线完成", result);
											} else {
												console.log("获取驾车数据失败：" + result);
											}
										}
									);
								}
							);
						}else {
							this.$message.error('起终点经纬度不完整')
						}
					})
					.catch((e) => {
						console.log(e);
					});
			},
		}
	}
</script>

<style>
	.mapComponents{
		width: 100%;
		height: 500px;
	}
</style>