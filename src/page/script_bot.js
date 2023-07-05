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
		this.cubism4Model = `/live2d.bak/asuna/asuna_${user.bot_skin}/asuna_${user.bot_skin}.model.json`
		// "https://cdn.jsdelivr.net/gh/Eikanya/Live2d-model/Live2D/Senko_Normals/senko.model3.json"
		// "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json";

		this.motions = {
			"idle": ["idle",undefined],
			"happy": ["", 0],
			"happy_s": ["", 1],
			"happy_l": ["", 2],
			"sad": ["", 3],
			"sad_s": ["", 4],
			"sad_l": ["", 5],
			"sneeze": ["", 6],
			"surprised": ["", 7],
			"surprise": ["", 7],
			"surprised_s": ["", 8],
			"surprise_s": ["", 8],
			"surprised_l": ["", 9],
			"surprise_ld": ["", 9],
			"angry": ["", 10],
			"angry_s": ["", 11],
			"angry_l": ["", 12]
		}
		
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
		
		var ratio = vh/vw
		this.model4["ratio"] = ratio
		
		if (ratio<1.2){
			this.model4.y = 50;
			if(vh>800){
				this.model4.y = 170;
			}
			if(vh<500){
			this.model4.y = -100;
			}
		}

		if (ratio>1.2){
			this.model4.y = 30;
			if(vh>800){
				this.model4.y = 150;
			}
		if(vh>1500){
			this.model4.y = 500;
		}
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


	

	get_y(scale){
		var min_w, max_w, min_x, max_x, per, times, x, scaled;
		min_w = 300; // y = 170
		max_w = 1080;  // x = 250

		times = (vw-min_w)/(max_w-min_w)
		var x_change = (250-(-150));
		x = times*x_change+(-150);
		
		// per = (vw-min_w)/(max_w-min_w);
		// times = (max_x-min_x)
		// x = per*times+min_x;
		return x;
	}

	speak_mtn(mtn, audio=null, volume=1, expression=null){
		let [type, mtn_id] = this.motions[mtn]
		// var category_name||type = "Idle" // name of the morion category
		// var animation_index||mtn_id = 0 // index of animation under that motion category
		var priority_number = 3 // if you want to keep the current animation going or move to new animation by force
		// var audio_link = "https://cdn.jsdelivr.net/gh/RaSan147/pixi-live2d-display@v1.0.3/playground/test.mp3" //[Optional arg, can be null or empty] [relative or full url path] [mp3 or wav file]
		// var volume = 1; //[Optional arg, can be null or empty] [0.0 - 1.0]
		// var expression = 4; //[Optional arg, can be null or empty] [index|name of expression]

		this.model4.motion(type, mtn_id, priority_number, audio, volume, expression)
	}
	
	speak(audio_file, volume=1, expression=null){
		this.model4.speak(audio_file, volume, expression)
	}

}

var bot = new Bot_();



window.addEventListener("resize", function () {
	bot.set_size();
})