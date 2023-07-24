class ANIME{
	constructor(){
		this.page = byId("anime-page");
	}

	async show_page(){
		this.page.classList.remove("inactive");
		this.page.classList.remove("hidden");
		document.body.classList.add("overflowHidden")
		try{bot.app.start();}
		catch(e){log("avatar not loaded")}

	}

	async hide_page(){
		this.page.classList.add("hidden");
		await tools.sleep(500);
		this.page.classList.add('inactive');
		document.body.classList.remove("overflowHidden")
		try{bot.app.stop();}
		catch(e){log("avatar not loaded")}
	}
	
	async set_bg(link){
		this.page.style.backgroundImage = "url('"+link+"')";
		log("bg: "+link)
	}
	
	async get_bg(){
		var that = this
		
		const form = document.createElement("form");
		form.method = "POST";
		form.action = "?bot_manager";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const form_ = new FormData(form);
		form_.append("post-type", "room_bg");
		form_.append("username", user.user_name);
		form_.append("uid", user.user_id);
		const request = new XMLHttpRequest()
		request.open("POST", form.action, false)
		request.onreadystatechange = () => {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 204 || request.status === 200){
					// use tools.safeJSONParse
					var response = JSON.parse(request.responseText);
					if (response.status){
						let msg_ele = response.message
						that.set_bg(msg_ele)
					}
				}
			}
		}

		
		request.send(form_)

	}
	
}

var anime = new ANIME()

//anime.set_bg("https://i.pximg.net/img-original/img/2022/09/04/00/03/11/100976186_p0.jpg")
anime.get_bg()
anime.show_page()
