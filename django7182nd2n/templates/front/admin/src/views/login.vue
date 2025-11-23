<template>
	<div>
		<div class="login-container">
			<el-form class="login_form animate__animated animate__">
				<div class="login_form2">
					<div class="title-container">基于深度学习的音乐推荐系统</div>
					<div v-if="loginType==1" class="list-item">
						<div class="lable">
							账号：
						</div>
						<input placeholder="请输入账号：" name="username" type="text" v-model="rulesForm.username">
					</div>
					<div v-if="loginType==1" class="list-item">
						<div class="lable">
							密码：
						</div>
						<div class="password-box">
							<input placeholder="请输入密码：" name="password" :type="showPassword?'text':'password'" v-model="rulesForm.password">
							<span class="icon iconfont" :class="showPassword?'icon-liulan13':'icon-liulan17'" @click="showPassword=!showPassword"></span>
						</div>
					</div>

					<div class="list-item select" v-if="roles.length>1">
						<div class="lable">
							角色：
						</div>
						<el-select v-model="rulesForm.role" placeholder="请选择角色：">
							<el-option v-if="loginType==1||(loginType==2&&item.roleName!='管理员')" v-for="item in roles" :key="item.roleName" :label="item.roleName" :value="item.roleName" />
						</el-select>
					</div>

		
					<div class="login-btn">
						<div class="login-btn1">
							<el-button v-if="loginType==1" type="primary" @click="login()" class="loginInBt">登录</el-button>
						</div>
						<div class="login-btn2">
						</div>
						<div class="login-btn3">
						</div>
					</div>
				</div>
			</el-form>
		</div>
	</div>
</template>
<script>
	import 'animate.css'
	import menu from "@/utils/menu";
	export default {
		data() {
			return {
				verifyCheck2: false,
				flag: false,
				baseUrl:this.$base.url,
				loginType: 1,
				rulesForm: {
					username: "",
					password: "",
					role: "",
				},
				menus: [],
				roles: [],
				tableName: "",
				showPassword: false,
			};
		},
		mounted() {
			let menus = menu.list();
			this.menus = menus;

			for (let i = 0; i < this.menus.length; i++) {
				if (this.menus[i].hasBackLogin=='是') {
					this.roles.push(this.menus[i])
				}
			}

		},
		created() {

		},
		destroyed() {
		},
		components: {
		},
		methods: {

			//注册
			register(tableName){
				this.$storage.set("loginTable", tableName);
				this.$router.push({path:'/register',query:{pageFlag:'register'}})
			},
			// 登陆
			login() {

				if (!this.rulesForm.username) {
					this.$message.error("请输入用户名");
					return;
				}
				if (!this.rulesForm.password) {
					this.$message.error("请输入密码");
					return;
				}
				if(this.roles.length>1) {
					if (!this.rulesForm.role) {
						this.$message.error("请选择角色");
						return;
					}

					let menus = this.menus;
					for (let i = 0; i < menus.length; i++) {
						if (menus[i].roleName == this.rulesForm.role) {
							this.tableName = menus[i].tableName;
						}
					}
				} else {
					this.tableName = this.roles[0].tableName;
					this.rulesForm.role = this.roles[0].roleName;
				}
		
				this.loginPost()
			},
			loginPost() {
				this.$http({
					url: `${this.tableName}/login?username=${this.rulesForm.username}&password=${this.rulesForm.password}`,
					method: "post"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.$storage.set("Token", data.token);
						this.$storage.set("role", this.rulesForm.role);
						this.$storage.set("sessionTable", this.tableName);
						this.$storage.set("adminName", this.rulesForm.username);
						if(this.boardAuth('hasBoard','查看',this.rulesForm.role)) {
							this.$router.replace({ path: "/board" });
						}else {
							this.$router.replace({ path: "/" });
						}
					} else {
						this.$message.error(data.msg);
					}
				});
			},
		}
	}
</script>

<style lang="scss" scoped>
.login-container {
	min-height: 100vh;
	position: relative;
	background-repeat: no-repeat;
	background-position: center center;
	background-size: cover;
	background: url(http://codegen.caihongy.cn/20241122/3afd27dffe9d48fe81e8299759ba0da6.jpg) no-repeat right top / cover !important;
	background: url(http://codegen.caihongy.cn/20241122/3afd27dffe9d48fe81e8299759ba0da6.jpg) no-repeat right top / cover !important;
	display: flex;
	width: 100%;
	min-height: 100vh;
	justify-content: flex-start;
	align-items: center;

	.login_form {
		border-radius: 12px;
		padding: 40px;
		margin: 0 0 0 10%;
		z-index: 1000;
		flex-direction: column;
		background: #0d0d0d;
		display: flex;
		width: 750px;
		align-items: center;
		position: relative;
		flex-wrap: wrap;
		height: auto;
		.login_form2 {
			width: 100%;
		}
		.title-container {
			padding: 0 0px;
			margin: 0 0 20px 0px;
			color: #fff;
			white-space: nowrap;
			background: noner;
			font-weight: 600;
			width: 100%;
			font-size: 22px;
			line-height: 40px;
			text-align: left;
		}
		.list-item {
			padding: 0;
			margin: 0 0 10px;
			display: flex;
			width: calc(100% - 0px);
			align-items: center;
			position: relative;
			flex-wrap: wrap;
			.lable {
				padding: 0 20px 0 0;
				color: #999;
				background: none;
				width: 100%;
				font-size: 16px;
				line-height: 44px;
				text-align: left;
			}
			input {
				border-radius: 0px;
				padding: 0 0px;
				color: #999;
				background: none;
				width: 100%;
				font-size: 16px;
				border-color: #999;
				border-width: 0 0 1px;
				border-style: solid;
				height: 44px;
			}
			input:focus {
				border-radius: 0px;
				padding: 0 0px;
				outline: none;
				color: #05ce65;
				background: none;
				width: 100%;
				font-size: 16px;
				border-color: #05ce65;
				border-width: 0 0 1px;
				border-style: solid;
				height: 44px;
			}
			.password-box {
				display: flex;
				width: 100%;
				position: relative;
				align-items: center;
				input {
					border-radius: 0px;
					padding: 0 0px;
					color: #999;
					background: none;
					width: 100%;
					font-size: 16px;
					border-color: #999;
					border-width: 0 0 1px;
					border-style: solid;
					height: 44px;
				}
				input:focus {
					border-radius: 0px;
					padding: 0 0px;
					outline: none;
					color: #05ce65;
					background: none;
					width: 100%;
					font-size: 16px;
					border-color: #05ce65;
					border-width: 0 0 1px;
					border-style: solid;
					height: 44px;
				}
				.iconfont {
					cursor: pointer;
					z-index: 1;
					color: #ccc;
					top: 0;
					font-size: 16px;
					line-height: 44px;
					position: absolute;
					right: 12px;
				}
			}
			input::placeholder {
				color: #fff;
				font-size: 16px;
			}
			/deep/ .el-select {
				width: 100%;
			}
			/deep/ .el-select .el-input__inner {
				border-radius: 0px;
				padding: 0 0px;
				color: #fff;
				background: none;
				width: 100%;
				font-size: 16px;
				border-color: #999;
				border-width: 0 0 1px;
				border-style: solid;
				height: 44px;
			}
			/deep/ .el-select .is-focus .el-input__inner {
				border-radius: 0px;
				padding: 0 0px;
				outline: none;
				color: #05ce65;
				background: none;
				width: 100%;
				font-size: 16px;
				border-color: #05ce65;
				border-width: 0 0 1px;
				border-style: solid;
				height: 44px;
			}
			/deep/ .el-select .el-input__inner::placeholder{
				color: #fff;
				font-size: 16px;
			}
		}
		.login-btn {
			margin: 40px 0 0;
			display: flex;
			width: calc(100% - 0px);
			justify-content: flex-start;
			align-items: center;
			flex-wrap: wrap;
			.login-btn1 {
				margin: 0;
				width: calc(50% - 0px);
				order: 1;
			}
			.login-btn2 {
				margin: 20px 0 0;
				display: flex;
				width: 100%;
				justify-content: flex-start;
				align-items: center;
				flex-wrap: wrap;
				order: 3;
			}
			.login-btn3 {
				margin: 0;
				width: calc(50% - 0px);
				text-align: right;
				order: 2;
			}
			.loginInBt {
				border: 0px solid rgba(0, 0, 0, 1);
				cursor: pointer;
				padding: 0 10px;
				margin: 0 0 10px;
				color: #fff;
				font-weight: 600;
				letter-spacing: 2px;
				font-size: 24px;
				border-radius: 50px;
				background: #05cb64;
				width: 190px;
				min-width: 68px;
				height: 60px;
			}
			.loginInBt:hover {
				opacity: 1;
			}
			.register {
				border: 1px solid #ccc;
				cursor: pointer;
				border-radius: 4px;
				padding: 0 20px;
				margin: 0 10px;
				color: #fff;
				background: none;
				width: auto;
				font-size: 16px;
				height: 34px;
			}
			.register:hover {
				color: #05ce65;
				border-color: #05ce65;
				opacity: 1;
			}
			.forget {
				border: 0;
				cursor: pointer;
				border-radius: 0;
				padding: 0;
				margin: 0 10px 10px 0;
				color: #fff;
				background: none;
				width: auto;
				font-size: 15px;
				text-align: center;
				height: 60px;
			}
			.forget:hover {
				color: #05ce65;
				opacity: 1;
			}
		}
	}
}

</style>
