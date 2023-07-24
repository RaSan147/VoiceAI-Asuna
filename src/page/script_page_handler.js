class PAGES{
	constructor(){
		this.current_page = "home";
		this.chat_page_handler = chat
		this.chat_page = chat.page
		this.anime_page_handler = anime
		this.anime_page = anime.page
	}
	
	async _to_chat(){
		this.current_page = "chat"
		await this.anime_page_handler.hide_page()
		this.chat_page_handler.show_page()
		this.chat_page_handler.chat_input.focus()
	}
	
	to_chat(){
		tools.fake_push()
		this._to_chat()
	}
	
	async _to_anime(){
		await this.chat_page_handler.hide_page()
		// location.reload(); // following code makes the character to invisible. so simply just reloading
		this.anime_page_handler.show_page()
		
	}

	to_anime(){
		if (this.current_page == "home") return;
		// history.pushState({page: "anime"}, "Anime AI", "#anime")
		history.back(); // this._to_anime()
	}
}

var pages = new PAGES()