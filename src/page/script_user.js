class USER{
	constructor() {
		this.user_name = null;
		this.user_id = null;
		this.bot_skin = "01";
		this.preference = {};

		this.get_local_data(false);
	}

	get_local_data(redirect=true) {
		// get userdata from localstorage
		let user_name = localStorage.getItem('uname')||tools.getCookie ("uname");
		let uid = localStorage.getItem('uid')||tools.getCookie ("uid");
		if (user_name===null||uid===null){
			if(redirect){
				this.logout(redirect);
			}
			return false;
	}

		this.user_name = user_name;
		this.user_id = uid;
		
	}

	set_local_data() {
		// set userdata to localstorage
		localStorage.setItem('uname', this.user_name);
		localStorage.setItem('uid', this.user_id);
		//localStorage.setItem('skin', this.bot_skin);
	}

	redirect_2_login() {
		// redirect to login page
		if(window.location.href != '/login'){
			window.location.href = '/login';
		}
	}

	verify_login(redirect=false, in_home=false) {
		if(!in_home){
		window.location.href = "/";}
		return true
		
		
		const user = this;
		if (user.user_name===null||user.user_id===null) return

		
		const form = document.createElement("form");
		form.method = "POST";
		form.action = "?do_verify";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const form_ = new FormData(form)
		form_.append("post-type", "verify")
		form_.append("username", user.user_name)
		form_.append("uid", user.user_id)
		const request = new XMLHttpRequest()
		request.open("POST", form.action, true)
		request.onreadystatechange = () => {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 204 || request.status === 200){
					// use tools.safeJSONParse
					var response = JSON.parse(request.responseText);
					if (response.status){
						if(!in_home) window.location.href = "/";
					}
					else{
						user.logout(redirect);
						//if(redirect) user.redirect_2_login();
					}
				}
			}
		}

		request.send(form_)
	}

	get_skin_link() {
		
		const form = document.createElement("form");
		form.method = "POST";
		form.action = "?bot_manager";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const form_ = new FormData(form)
		form_.append("post-type", "get_skin_link")
		form_.append("username", user.user_name)
		form_.append("uid", user.user_id)
		const request = new XMLHttpRequest()
		request.open("POST", form.action, false)
		request.onreadystatechange = () => {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 204 || request.status === 200){
					// use tools.safeJSONParse
					var response = JSON.parse(request.responseText);
					if (response.status){
						console.log("Loading Avatar")
						bot.cubism4Model = response.message;
						bot.anim_loader();
					}
					else{
						log("Failed to get character link")
					}
				}
			}
		}

		request.send(form_)

	}

	logout(redirect=true) {
		// logout
		tools.clear_cookie();
		localStorage.clear();
		if(redirect) this.redirect_2_login();
	}

}
	

var user = new USER();


