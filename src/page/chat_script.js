// chat handler

class ChatHandler{

	constructor(){
		this.current_chat  = 0; // current chat id
		this.current_reply = 0; // current reply id
		this.chats = byId("chats");
		this.chat_input = byId("chat_input");
		this.chat_input.onkeydown = e => {
			if(e.key == "Enter"){
				this.send_message();
			}
		}
		
	}

	// add chat to chat list
	add_chat(chat){
		let message = createElement("div");
		message.classList.add("message");
		message.appendChild(chat);
		this.chats.appendChild(message);
		this.chats.appendChild(line_break())
		if(this.chats.scrollHeight > 100)
		window.scrollTo(0, this.chats.scrollHeight)
		this.chat_input.focus();
	}

	// make message element
	make_message(msg, type){
		let message = createElement("div");
		message.classList.add("message-text");
		message.classList.add(type);
		message.innerHTML = msg;
		return message;
	}
	// remove chat from chat list
	remove_chat(id){
		this.chats.removeChild(byId("chat-" + id));
	}

	send_message(){
		let msg = this.chat_input.value;
		this.chat_input.value = "";
		this.chat_input.focus();
		if (msg.length == 0) return;

		// send message to server
		// use fetch post
		
		this.add_chat(this.make_message(msg, "user"));

		// fetch("/chat?send_msg", {
		// 	method: "POST",
		// 	headers: {
		// 		"Content-Type": "application/json"
		// 	},

		// 	body: JSON.stringify({
		// 		message: msg
		// 	})
		// }).then(r => r.json()).then(data => {
		// 	if(data.status == "ok"){
		// 		// message sent
		// 		this.add_chat(this.make_message(msg, "user"));
		// 	} else {
		// 		// error
		// 		popup_msg.createPopup("Failed to send message", data.err_msg);
		// 		popup_msg.open_popup();
		// 	}
		// }).catch(e => {
		// 	popup_msg.createPopup("Failed to send message");
		// 	popup_msg.open_popup();
		// })

	}

	get_reply(_){
		// send message to server
		// use fetch post
		fetch("/chat?get_reply="+(this.current_reply+1)
			).then(r => r.json()).then(data => {
			if(data.status == "ok"){
				// message sent
				this.add_chat(this.make_message(data.reply, "bot"));
			}
		}).catch(e => {
			bot.set_status(false);
			return false; 
		})
		// disable fetch err log
		.catch(e => {
			
	}


}

let chat = new ChatHandler();

setInterval(chat.get_reply.bind(chat), 500);