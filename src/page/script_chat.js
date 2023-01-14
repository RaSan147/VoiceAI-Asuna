// chat handler

function request(url){
	fetch(url).then(r => {
		if(!r.ok)
			return false
		return r.text
	}).catch(e => {
		// server is down
		log(e)
	})

}
class ChatHandler{

	constructor(){
		this.current_msg  = 0; // current chat id
		this.cache_id = 0; // message not sent
		this.chats = byId("chats");
		this.page = byId("chat-page");
		this.chat_input = byId("chat_input");
		this.chat_input.onkeydown = e => {
			if(e.key == "Enter"){
				if(e.shiftKey){
					// this.chat_input.value += "\n";
					return;
				}
				e.preventDefault();
				this.send_message();
			}
		}
		
	}

	// add chat to chat list
	add_chat(chat, type="user"){
		const m_id = this.cache_id+1
		this.cache_id+=1;

		let message = createElement("div");
		message.id = "chat-c" + m_id
		message.classList.add("message");

		if(type == "bot"){
			let img = createElement("img");
			img.src = bot.avatar;
			img.classList.add("profile_pic");
			message.appendChild(img);
		}
		message.appendChild(chat);
		this.chats.appendChild(message);
		// this.chats.appendChild(line_break());
		if(this.chats.scrollHeight > 100)
			window.scrollTo({
			top: this.chats.scrollHeight,
			left: 0,
			behavior: 'smooth'
		});
		this.chat_input.focus();
		
		return message
	}

	// make message element
	make_message(msg, type, render="innerText"){
		let message = createElement("div");
		message.classList.add("message-text");
		message.classList.add(type);
		message[render] = msg;
		return message;
	}
	// remove chat from chat list
	remove_chat(id){
		this.chats.removeChild(byId("chat-" + id));
	}

	not_sent(msg_ele, msg){
		const that = this;
		const err_msg = createElement("div")
		err_msg.classList.add("error_foot")
		err_msg.innerText = "Failed. Tap to retry"
		err_msg.onclick = (e) => {
			that.chats.removeChild(msg_ele)
			this.chats.removeChild(err_msg)
			that.send_message(msg)
		}
		this.chats.appendChild(err_msg)

	}

	send_message(text=null){
		var msg;
		if(text==null) msg = this.chat_input.value;
		else msg = text;
		msg = msg.trim();
		this.chat_input.value = "";
		this.chat_input.focus();
		if (msg.length == 0) return;
		
		const msg_ele = this.add_chat(this.make_message(msg, "user"));
		// send message to server
		// use fetch post
		this.push_msg(msg_ele, msg)

	}

	success_msg(msg_ele){
		const tick = createElement("span")
		tick.className = "fa fa-regular fa-check sent-tick"
		tick.innerText = "✔"
		tick.style.color = "green"
		tick.style.fontSize = "5px"
		msg_ele.appendChild(tick)
		theme_controller.del_fa_alt(msg_ele)
	}

	replied_msg(json){
		const that = this;
		const msg = json.message;
		var render = "innerText";
		if (json.render == "innerHTML") render = "innerHTML";
		const msg_ele = that.add_chat(this.make_message(msg, "bot", render), "bot");
		if (json.script) {
			log("script: " + json.script)
			const script = createElement("script");
			script.innerText = json.script;
			msg_ele.appendChild(script);
		}

		return msg_ele
	}

	async push_msg(msg_ele, msg){
		const that = this;
		// actually send message 

		if(msg == "clear") return tools.del_child(this.chats)
		if(msg == "logout"){
			that.add_chat(that.replied_msg("Ok bye!!!"), "bot");
			await tools.sleep(1000)
			return user.logout()
		}

		

		const form = document.createElement("form");
		form.method = "POST";
		form.action = "/chat?send_msg";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const form_ = new FormData(form);
		form_.append("chat", "chat");
		form_.append("username", user.user_name);
		form_.append("uid", user.user_id);
		form_.append("message", msg);

		const request = new XMLHttpRequest()
		request.open("POST", form.action, true)
		request.onreadystatechange = () => {
			if (request.readyState === XMLHttpRequest.DONE) {
				if (request.status === 204 || request.status === 200){
					var response = JSON.parse(request.responseText);
					if (response.status){
						that.success_msg(msg_ele)
						return that.replied_msg(response)
					}
				}
				that.not_sent(msg_ele, msg)
			}
		}
	
		request.send(form_)

		

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
		// 		throw new Error()
		// 	}
		// }).catch(e => {
		// 	this.not_sent(msg_ele, msg)
		// })

	}

	verify_index(index){
		// match with current index on browser,
		// if lower, will get previous <100 msg
		
		



	}

	async get_msg_index(){
		var index = await request("/chat?get_msg_index&uid="+user.user_id, "GET");
		if(index == null) {
			bot.set_status(false);
			return
		}
		
		bot.set_status(true);
		index = JSON.parse(index);
		if(index.status == "ok"){
			chat.verify_index(index)
		}
	}

	get_msg(id){
		// get message to server
		// use xmlhttprequest post

		var msg = request("/get_msg?id="+id)
		if (msg==null) return false
		msg = JSON.parse(msg)
		this.add_chat(this.make_message(msg.text, msg.from));


	}

	async hide_page(){
		this.page.classList.add('hidden');
		top_bar.hide()
		await tools.sleep(500);
		this.page.classList.add('inactive');
		// loading_popup()
	}

	show_page(){
		this.page.classList.remove('hidden');
		this.page.classList.remove('inactive');

		top_bar.show()
	}




}

var chat = new ChatHandler();
// chat.active_page()

// setInterval(chat.get_msg_index.bind(chat), 1500);

