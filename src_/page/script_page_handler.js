class PAGES{
	constructor(){
		this.current_page = "home";
		this.chat_page_handler = chat
		this.chat_page = chat.page
		this.anime_page_handler = anime
		this.anime_page = anime.page
	}

	async to_chat(){
		this.current_page = "chat"
		await this.anime_page_handler.hide_page()
		this.chat_page_handler.show_page()
		this.chat_page_handler.chat_input.focus()
	}

	async to_anime(){
		
		this.current_page = "anime"
		await this.chat_page_handler.hide_page()
		// location.reload(); // following code makes the charecter to invisible. so simply just reloading
		this.anime_page_handler.show_page()
	}
}

var pages = new PAGES()