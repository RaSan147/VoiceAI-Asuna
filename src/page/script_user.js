class USER{
	constructor() {
		this.user_name = null;
		this.user_id = null;

		this.preference = {};
	}

	get_local_data(redirect=true) {
		// get userdata from localstorage
		let user_name = localStorage.getItem('uname');
		let uid = localStorage.getItem('uid');
		if (user_name===null||uid===null){
			if(redirect) this.redirect_2_login();
			return false;
		}



		
		this.user_name = user_name;
		this.user_id = uid;
	}

	set_local_data() {
		// set userdata to localstorage
		localStorage.setItem('uname', this.user_name);
		localStorage.setItem('uid', this.user_id);
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
						log("verified")
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

		
		// const form = document.createElement("form");
		// form.method = "POST";
		// form.action = "/chat?send_msg";
		// form.style.display = "none";
		// form.setAttribute("enctype", "multipart/form-data");

		// const form_ = new FormData(form);
		// form_.append("chat", "chat");
		// form_.append("username", user.user_name);
		// form_.append("uid", user.user_id);
		// form_.append("message", msg);

		// const request = new XMLHttpRequest()
		// request.open("POST", form.action, true)
		// request.onreadystatechange = () => {
		// 	if (request.readyState === XMLHttpRequest.DONE) {
		// 		if (request.status === 204 || request.status === 200){
		// 			var response = JSON.parse(request.responseText);
		// 			if (response.status){
		// 				that.success_msg(msg_ele)
		// 				return that.add_chat(that.make_message(response.message, "bot"), "bot");
		// 			}
		// 		}
		// 		that.not_sent(msg_ele, msg)
		// 	}
		// }

		// request.send(form_)


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


