class Bot{
	constructor(){
		this.avatar = "https://i.imgur.com/8YQ1Z7A.png";
		this.active = false;
		this.status_bull = byId("app_status");
		this.AI_NAME = "Alice";
		
		top_bar.set_title(this.AI_NAME);
	}

	set_status(status){
		this.active = status;
		if (status){
			this.status_bull.style.color = "#00ff00";
		}else{
			this.status_bull.style.color = "#ff0000";
		}
	}

}

let bot = new Bot();
