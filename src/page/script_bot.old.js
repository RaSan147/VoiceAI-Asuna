class Bot_{
	constructor(){
		this.avatar = "https://i.ibb.co/mJkDYVm/image-2023-01-13-121437265.png";
		this.active = false;
		this.status_bull = byId("app_status");
		this.AI_NAME = "Asuna";
		this.model4 = null;
		this.canvas = byId("canvas");
		this.app = null;
		this.cubism4Model =
		"/live2d.bak/asuna/asuna_01/asuna_01.model.json"
		// "https://cdn.jsdelivr.net/gh/Eikanya/Live2d-model/Live2D/Senko_Normals/senko.model3.json"
		// "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json";
		
	  
		
		top_bar.set_title(this.AI_NAME);
		top_bar.set_profile_pic(this.avatar);
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
		this.canvas.style.height = "auto";
		theme_controller.getViewportSize();
		// log(vw,vh)
		var scale;
		var vh1, vh2;
		var s1, s2;

		vh1 = 700; // 0.20
		vh2 = 1080; // 0.35

		s1 = 0.2;
		s2 = 0.35;
		
		// vh1 = 0; // 0
		// vh2 = 1080; // 0.35

		// s1 = 0;
		// s2 = 0.35;



		scale = (vh-vh1)/(vh2-vh1)*(s2-s1) + s1;

		this.model4.scale.set(scale);
		this.model4.x = this.get_x(scale);
		this.model4.y = 170;
		
	}


	get_x(scale){
		var min_w, max_w, per, times, x, scaled;
		var min_x, max_x;
		var x1, x2;

		min_w = 1280; // x = 150
		max_w = 1920;  // x = 600

		x1 = 150
		x2 = 600

		var times = (vw-min_w)/(max_w-min_w)
		var x_change = (x2-(x1));
		x = times*x_change+(x1);
		
		// per = (vw-min_w)/(max_w-min_w);
		// times = (max_x-min_x)
		// x = per*times+min_x;
		return x;
	}

	

	get_y(scale){
		var min_w, max_w, min_x, max_x, per, times, x, scaled;
		min_h = 300; // y = 170
		max_h = 1080;  // x = 250

		var times = (vw-min_w)/(max_w-min_w)
		var x_change = (250-(-150));
		x = times*x_change+(-150);
		
		// per = (vw-min_w)/(max_w-min_w);
		// times = (max_x-min_x)
		// x = per*times+min_x;
		return x;
	}

}

var bot = new Bot_();



window.addEventListener("resize", function () {
	bot.set_size();
})