<template>
	<div>
		<div class="register-container">
			<el-form v-if="pageFlag=='register'" ref="ruleForm" class="rgs-form animate__animated animate__" :model="ruleForm" :rules="rules">
				<div class="rgs-form2">
					<div class="title">基于深度学习的音乐推荐系统</div>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('zhanghao')?'required':''">账号：</div>
						<el-input  v-model="ruleForm.zhanghao"  autocomplete="off" placeholder="账号"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('mima')?'required':''">密码：</div>
						<el-input  v-model="ruleForm.mima"  autocomplete="off" placeholder="密码"  type="password"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('mima')?'required':''">确认密码：</div>
						<el-input  v-model="ruleForm.mima2" autocomplete="off" placeholder="确认密码" type="password" />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('nicheng')?'required':''">昵称：</div>
						<el-input  v-model="ruleForm.nicheng"  autocomplete="off" placeholder="昵称"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('xingbie')?'required':''">性别：</div>
						<el-select v-model="ruleForm.xingbie" placeholder="请选择性别" >
							<el-option
								v-for="(item,index) in yonghuxingbieOptions"
								v-bind:key="index"
								:label="item"
								:value="item">
							</el-option>
						</el-select>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('shoujihaoma')?'required':''">手机号码：</div>
						<el-input  v-model="ruleForm.shoujihaoma"  autocomplete="off" placeholder="手机号码"  type="text"  />
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('shengri')?'required':''">生日：</div>
						<el-date-picker
							format="yyyy 年 MM 月 dd 日"
							value-format="yyyy-MM-dd"
							v-model="ruleForm.shengri"
							type="date"
							placeholder="生日"
						></el-date-picker>
					</el-form-item>
					<el-form-item class="list-item" v-if="tableName=='yonghu'">
						<div class="lable" :class="changeRules('touxiang')?'required':''">头像：</div>
						<file-upload
							tip="点击上传头像"
							action="file/upload"
							:limit="3"
							:multiple="true"
							:fileUrls="ruleForm.touxiang?ruleForm.touxiang:''"
							@change="yonghutouxiangUploadChange"
						></file-upload>
					</el-form-item>
					<div class="register-btn">
						<div class="register-btn1">
							<button type="button" class="r-btn" @click="login()">注册</button>
						</div>
						<div class="register-btn2">
							<div class="r-login" @click="close()">已有账号，直接登录</div>
						</div>
					</div>
				</div>
			</el-form>
		</div>
	</div>
</template>

<script>
	import 'animate.css'
export default {
	data() {
		return {
			ruleForm: {
			},
			forgetForm: {},
            pageFlag : '',
			tableName:"",
			rules: {},
            yonghuxingbieOptions: [],
		};
	},
	mounted(){
		this.pageFlag = this.$route.query.pageFlag
		if(this.$route.query.pageFlag=='register'){
			
			let table = this.$storage.get("loginTable");
			this.tableName = table;
			if(this.tableName=='yonghu'){
				this.ruleForm = {
					zhanghao: '',
					mima: '',
					nicheng: '',
					xingbie: '',
					shoujihaoma: '',
					shengri: '',
					touxiang: '',
					status: '',
				}
			}
			if ('yonghu' == this.tableName) {
				this.rules.zhanghao = [{ required: true, message: '请输入账号', trigger: 'blur' }]
			}
			if ('yonghu' == this.tableName) {
				this.rules.mima = [{ required: true, message: '请输入密码', trigger: 'blur' }]
			}
			if ('yonghu' == this.tableName) {
				this.rules.nicheng = [{ required: true, message: '请输入昵称', trigger: 'blur' }]
			}
			this.yonghuxingbieOptions = "男,女".split(',')
		}
	},
	created() {
	},
	destroyed() {
		  	},
	methods: {
		changeRules(name){
			if(this.rules[name]){
				return true
			}
			return false
		},
		// 获取uuid
		getUUID () {
			return new Date().getTime();
		},
		close(){
			this.$router.push({ path: "/login" });
		},
        yonghutouxiangUploadChange(fileUrls) {
            this.ruleForm.touxiang = fileUrls;
        },

        // 多级联动参数


		// 注册
		login() {
			var url=this.tableName+"/register";
			if((!this.ruleForm.zhanghao) && `yonghu` == this.tableName){
				this.$message.error(`账号不能为空`);
				return
			}
			if((!this.ruleForm.mima) && `yonghu` == this.tableName){
				this.$message.error(`密码不能为空`);
				return
			}
			if((this.ruleForm.mima!=this.ruleForm.mima2) && `yonghu` == this.tableName){
				this.$message.error(`两次密码输入不一致`);
				return
			}
			if((!this.ruleForm.nicheng) && `yonghu` == this.tableName){
				this.$message.error(`昵称不能为空`);
				return
			}
			if(`yonghu` == this.tableName && this.ruleForm.shoujihaoma &&(!this.$validate.isMobile(this.ruleForm.shoujihaoma))){
				this.$message.error(`手机号码应输入手机格式`);
				return
			}
            if(this.ruleForm.touxiang!=null) {
                this.ruleForm.touxiang = this.ruleForm.touxiang.replace(new RegExp(this.$base.url,"g"),"");
            }
			this.$http({
				url: url,
				method: "post",
				data:this.ruleForm
			}).then(({ data }) => {
				if (data && data.code === 0) {
					this.$message({
						message: "注册成功",
						type: "success",
						duration: 1500,
						onClose: () => {
							this.$router.replace({ path: "/login" });
						}
					});
				} else {
					this.$message.error(data.msg);
				}
			});
		}
	}
};
</script>

<style lang="scss" scoped>
.register-container {
	position: relative;
	background: url(http://codegen.caihongy.cn/20241122/3afd27dffe9d48fe81e8299759ba0da6.jpg) no-repeat right top / cover !important;
	background: url(http://codegen.caihongy.cn/20241122/3afd27dffe9d48fe81e8299759ba0da6.jpg) no-repeat right top / cover !important;
	display: flex;
	width: 100%;
	min-height: 100vh;
	justify-content: flex-start;
	align-items: center;
	.rgs-form {
		.rgs-form2 {
		width: 100%;
		}
		border-radius: 12px;
		padding: 40px;
		margin: 20px 0 20px 10%;
		z-index: 1000;
		flex-direction: column;
		background: #0d0d0d;
		display: flex;
		width: 750px;
		align-items: center;
		position: relative;
		flex-wrap: wrap;
		height: auto;
		.title {
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
			padding: 0 0 0 0px;
			margin: 0 0 20px;
			width: 100%;
			position: relative;
			height: auto;
			/deep/ .el-form-item__content {
				display: block;
			}
			.lable {
				color: #999;
				display: inline-block;
				width: 100%;
				font-size: 16px;
				line-height: 40px;
				text-align: left;
			}
			.el-input {
				width: 100%;
			}
			.el-input /deep/ .el-input__inner {
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
			.el-input /deep/ .el-input__inner:focus {
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
			.el-input-number {
				width: 100%;
			}
			.el-input-number /deep/ .el-input__inner {
				text-align: center;
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
			.el-input-number /deep/ .el-input__inner:focus {
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
			.el-input-number /deep/ .el-input-number__decrease {
				display: none;
			}
			.el-input-number /deep/ .el-input-number__increase {
				display: none;
			}
			.el-select {
				width: 100%;
			}
			.el-select /deep/ .el-input__inner {
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
			.el-select /deep/ .el-input__inner:focus {
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
			.el-date-editor {
				width: 100%;
			}
			.el-date-editor /deep/ .el-input__inner {
				border-radius: 0px;
				padding: 0 0 0 30px;
				color: #fff;
				background: none;
				width: 100%;
				font-size: 16px;
				border-color: #999;
				border-width: 0 0 1px;
				border-style: solid;
				height: 44px;
			}
			.el-date-editor /deep/ .el-input__inner:focus {
				border-radius: 0px;
				padding: 0 0 0 30px;
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
			.el-date-editor.el-input {
				width: 100%;
			}
			/deep/ .el-upload--picture-card {
				background: transparent;
				border: 0;
				border-radius: 0;
				width: auto;
				height: auto;
				line-height: initial;
				vertical-align: middle;
			}
			/deep/ .upload .upload-img {
				border: 1px solid #999;
				cursor: pointer;
				border-radius: 0px;
				color: #999;
				background: none;
				width: 120px;
				font-size: 24px;
				line-height: 48px;
				text-align: center;
				height: 48px;
			}
			/deep/ .el-upload-list .el-upload-list__item {
				border: 1px solid #999;
				cursor: pointer;
				border-radius: 0px;
				color: #999;
				background: none;
				width: 120px;
				font-size: 24px;
				line-height: 48px;
				text-align: center;
				height: 48px;
			}
			/deep/ .el-upload .el-icon-plus {
				border: 1px solid #999;
				cursor: pointer;
				border-radius: 0px;
				color: #999;
				background: none;
				width: 120px;
				font-size: 24px;
				line-height: 48px;
				text-align: center;
				height: 48px;
			}
			/deep/ .el-upload__tip {
				color: #fff;
				font-size: 15px;
			}
			/deep/ .el-input__inner::placeholder {
				color: #fff;
				font-size: 16px;
			}
			.required {
				position: relative;
			}
			.required::after{
				color: red;
				position: inherit !important;
				content: "*";
				order: -1;
			}
			.editor {
				border: 1px solid #eee;
				background: #fff;
				width: 100%;
				min-height: 250px;
				height: auto;
			}
			.editor>.avatar-uploader {
				line-height: 0;
				height: 0;
			}
		}
		.list-item.email {
			input {
				border-radius: 0px;
				padding: 0 0px;
				color: #999;
				background: none;
				flex: 1;
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
			input::placeholder {
				color: #fff;
				font-size: 16px;
			}
			button {
				border: 0px solid #efeff7;
				cursor: pointer;
				border-radius: 0 0px 0px 0;
				padding: 0;
				margin: 0px 0 0 10px;
				color: #fff;
				background: #05ce65;
				width: 150px;
				font-size: 15px;
				height: 44px;
			}
			button:hover {
				opacity: 1;
			}
		}
		.register-btn {
			margin: 0;
			display: flex;
			width: calc(100% + 0px);
			justify-content: space-between;
		}
		.register-btn1 {
			margin: 0;
			width: calc(50% - 0px);
		}
		.register-btn2 {
			width: calc(50% - 0px);
		}
		.r-btn {
			border: 0px solid rgba(0, 0, 0, 1);
			cursor: pointer;
			padding: 0 10px;
			margin: 0 0 10px;
			color: #fff;
			font-weight: 600;
			letter-spacing: 2px;
			font-size: 24px;
			border-radius: 30px;
			background: #05cb64;
			width: 190px;
			min-width: 68px;
			height: 60px;
		}
		.r-btn:hover {
			opacity: 1;
		}
		.r-login {
			cursor: pointer;
			padding: 0;
			color: #ccc;
			display: inline-block;
			width: 100%;
			font-size: 15px;
			line-height: 60px;
			text-align: right;
		}
		.r-login:hover {
		}
	}
}
	
	::-webkit-scrollbar {
	  display: none;
	}
</style>
