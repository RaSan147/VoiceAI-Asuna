class USER{
	constructor() {
		this.user_name = null;
		this.user_id = null;
		this.bot_skin = "01";
		this.preference = {};
	}

	get_local_data(redirect=true) {
		// get userdata from localstorage
		let user_name = localStorage.getItem('uname');
		let uid = localStorage.getItem('uid');
		let skin = localStorage.getItem('skin');
		if (user_name===null||uid===null){
			if(redirect) this.redirect_2_login();
			return false;
		}



		
		this.user_name = user_name;
		this.user_id = uid;
		if(skin) this.bot_skin = skin;
	}

	set_local_data() {
		// set userdata to localstorage
		localStorage.setItem('uname', this.user_name);
		localStorage.setItem('uid', this.user_id);
		localStorage.setItem('skin', this.bot_skin);
	}

	redirect_2_login() {
		// redirect to login page
		window.location.href = '/login';
	}

	verify_login(redirect=false, in_home=false) {
		const user = this;
		if (user.user_name===null||user.user_id===null) return

	
		const form = document.createElement("form");
		form.method = "POST";
		form.action = "/do_verify";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const formData = new FormData(form)
		formData.append("verify", "verify")
		formData.append("username", user.user_name)
		formData.append("uid", user.user_id)
		const request = new XMLHttpRequest()
		request.open("POST", "do_verify", true)
		request.onreadystatechange = () => {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 204 || request.status === 200){
					var response = JSON.parse(request.responseText);
					if (response.status){
						console.log("verified")
						if(!in_home) window.location.href = "/";
					}
					else{
						user.logout(redirect);
						if(redirect) user.redirect_2_login();
					}
				}
			}
		}

		request.send(formData)

	}

	get_skin_link() {
		
		const form = document.createElement("form");
		form.method = "POST";
		form.action = "/bot_manager";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const formData = new FormData(form)
		formData.append("get_skin_link", "get_skin_link")
		formData.append("username", user.user_name)
		formData.append("uid", user.user_id)
		const request = new XMLHttpRequest()
		request.open("POST", form.action, true)
		request.onreadystatechange = () => {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 204 || request.status === 200){
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

		request.send(formData)
	}

	logout(redirect=true) {
		// logout
		user.user_name = null;
		user.user_id = null;
		user.set_local_data();
		if(redirect) user.redirect_2_login();
	}

}
	

var user = new USER();


