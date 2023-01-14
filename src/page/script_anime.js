class ANIME{
	constructor(){
		this.page = byId("anime-page");
	}

	show_page(){
		this.page.classList.remove("inactive");
		this.page.classList.remove("hidden");
		document.body.classList.add("overflowHidden")
		bot.app.start();

	}

	async hide_page(){
		this.page.classList.add("hidden");
		await tools.sleep(500);
		this.page.classList.add('inactive');
		document.body.classList.remove("overflowHidden")
		bot.app.stop();
	}
}

var anime = new ANIME()

anime.show_page()