const base = {
    get() {
        return {
            url : "http://localhost:8080/django7182nd2n/",
            name: "django7182nd2n",
            // 退出到首页链接
            indexUrl: 'http://localhost:8080/front/dist/index.html'
        };
    },
    getProjectName(){
        return {
            projectName: "基于深度学习的音乐推荐系统"
        } 
    }
}
export default base
