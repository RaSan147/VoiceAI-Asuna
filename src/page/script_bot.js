class Bot_{
	constructor(){
		//this.avatar = "https://i.ibb.co/mJkDYVm/image-2023-01-13-121437265.png";
		this.avatar = "https://i.ibb.co/7VqWWVH/image.webp"
		this.active = false;
		this.status_bull = byId("app_status");
		this.AI_NAME = "Asuna";
		this.model4 = null;
		this.canvas = byId("canvas");
		this.canvas.style.height = "auto";	
		this.app = null;
		this.cubism4Model = 
		`/live2d.bak/asuna/asuna_${user.bot_skin}/asuna_${user.bot_skin}.model.json`
		// "https://cdn.jsdelivr.net/gh/Eikanya/Live2d-model/Live2D/Senko_Normals/senko.model3.json"
		// "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json";
		
	  
		
		top_bar.set_title(this.AI_NAME);
		top_bar.set_profile_pic(this.avatar);
	}

	get_user_pref_skin(skin){
		user.bot_skin = skin;
		user.set_local_data();
		popup_msg.createPopup("Skin changed. Please refresh", "<a class='pagination' onclick='tools.refresh()'>Refresh</a>");
		popup_msg.show();
	}

	set_status(status){
		this.active = status;
		if (status){
			this.status_bull.style.color = "#00ff00";
		}else{
			this.status_bull.style.color = "#ff0000";
		}
	}

	async anim_loader() {
		this.app = new PIXI.Application({
			view: document.getElementById("canvas"),
			autoStart: true,
			resizeTo: document.body,
			backgroundAlpha:0,
			backgroundColor: 0x000000,
		});
	
		this.model4 = await PIXI.live2d.Live2DModel.from(this.cubism4Model);
	
		this.app.stage.addChild(this.model4);
	
		this.set_size();
	}


	
	set_size(){
		theme_controller.getViewportSize();
		// log(vw,vh)
		var scale = 0.25;
		if(vh>999){
			scale = 0.35;
		}
		if(vh>1279){
			scale = 0.45;
		}
		this.model4.scale.set(scale);
		this.model4.x = this.get_x(scale);
		this.model4.y = 170;

		if (vh<500){
			this.model4.y = 30;
		}
		
	}

	get_x(scale){
		var min_w, max_w, min_x, max_x, per, times, x, scaled;
		min_w = 300;
		max_w = 1280; 
		if(scale==0.25){
			min_x = -150;
			max_x = 300;
		}else if(scale==0.35){
			min_x = -270;
			max_x = 300;
		}else if(scale==0.45){
			min_x = -400;
			max_x = 100;
		}
		per = (vw-min_w)/(max_w-min_w);
		times = (max_x-min_x)
		x = per*times+min_x;
		return x;
	}




}

var bot = new Bot_();



window.addEventListener("resize", function () {
	bot.set_size();
})