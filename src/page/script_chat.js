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
		let that = this;
		this.minimized = false; //minimized mode, when both chat and see
		this.current_msg  = 0; // current chat id
		this.cache_id = 0; // message not sent
		this.chats = byId("chats");
		this.page = byId("chat-page");
		this.chat_input = byId("chat_input");
		this.maximize_btn = byId("maximize-page") 
		this.chat_input.onkeydown = e => {
			if(e.key == "Enter"){
				if(e.shiftKey){
					that.chat_input.value += "\n";
					return;
				}
				e.preventDefault();
				that.send_message();
			}
		}
		this.chat_input.onfocus = e => { that.go_to_bottom()
		}
		if('visualViewport' in window) {
			window.visualViewport.onresize = e =>{
				that.go_to_bottom()
			}
		}

		this.default_reply = {
			"message": "Sorry, I didn't get that. Try again.",
			"render": "innerText",
			"script": ""
		}
		
	}
	
	async go_to_bottom(){
		//alert(this.chats.scrollHeight)
		await tools.sleep(30)

		if(this.chats.scrollHeight > 100){
			this.page.scrollTo({
			top: this.chats.scrollHeight,
			left: 0,
			behavior: 'smooth'
			});
		}
	}

	add_typing(){
		let typing = createElement("div");
		typing.classList.add("typing");
		typing.innerText = "typing...";
		return this.add_chat(typing, "bot");
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
		
		this.chat_input.focus();
		this.go_to_bottom()
		
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
		byId("help-notice").style.display = "none"; // hide help notice on first message


		var msg;
		if(text==null) msg = this.chat_input.value;
		else msg = text;
		msg = msg.trim();
		if(msg.length>512){
			toaster.toast("Message too long")
			return
		}
		this.chat_input.value = "";
		this.chat_input.focus();
		if (msg.length == 0) return;
		
		const msg_ele = this.add_chat(this.make_message(msg, "user"));
		// send message to server
		// use fetch post
		this.push_msg(msg_ele, msg)

	}

	success_msg(msg_ele){
		let tick = createElement("span")
		tick.className = "fa fa-regular fa-check sent-tick"
		tick.innerText = "✔"
		tick.style.color = "green"
		tick.style.fontSize = "5px"

		this.chats.appendChild(tick)
		theme_controller.del_fa_alt(tick)
	}

	async replied_msg(json){
		let that = this;
		const msg = json.message;
		var render = "innerText";
		if (json.render == "innerHTML") render = "innerHTML";
		const msg_ele = that.add_chat(this.make_message(msg, "bot", render), "bot");
		if (json.script) {
			log("script: " + json.script)
			const script = createElement("script");
			script.innerText = json.script;
			// script.setAttribute("async", true);
			document.body.appendChild(script);
		}
		var voice=null, motion="idle", expression=null, volume=1;
		if (json.voice) {
				voice = json.voice;
				// alert(voice)
		}
		if (json.motion) {
			motion = json.motion
		}
		if (json.expression) {
			expression = json.expression
		}
		if (json.volume) {
			volume = json.volume
		}
		
		if (json.delay) {
			// set a timer of 5 min
			await tools.sleep(json.delay * 1000)
		}


		if (voice) {
			bot.speak(voice, volume, expression)
		}

		return msg_ele
	}

	async push_msg(msg_ele, msg){
		const that = this;
		// actually send message 
		

		if(msg == "clear") return tools.del_child(this.chats)
		// if(tools.is_in(msg.toLowerCase(), ["logout", "log out", "sign off", "signoff", "sign out", "signout", "logoout"])){
		// 	let reply = this.default_reply;
		// 	reply.message = "Ok bye!!!";
		// 	that.replied_msg(reply);
		// 	await tools.sleep(1000)
		// 	return user.logout()
		// }


		var typing = null;

		const form = document.createElement("form");
		form.method = "POST";
		form.action = "/chat?send_msg";
		form.style.display = "none";
		form.setAttribute("enctype", "multipart/form-data");

		const form_ = new FormData(form);
		form_.append("post-type", "send-txt");
		form_.append("username", user.user_name);
		form_.append("uid", user.user_id);
		form_.append("message", msg);
		form_.append("time", tools.c_time());
		form_.append("tzOffset", tools.time_offset());
		form_.append("voice", appConfig.enable_voice && pages.current_page=="home");

		const request = new XMLHttpRequest()
		request.open("POST", form.action, true)
		request.onreadystatechange = () => {
			
			if (request.readyState === XMLHttpRequest.DONE) {
				
				if (request.status === 204 || request.status === 200){
					// use tools.safeJSONParse
					var response = JSON.parse(request.responseText);
					if (typing) that.chats.removeChild(typing);
					if (response.status){
						that.success_msg(msg_ele)
						return that.replied_msg(response)
					}
				}
				// that.not_sent(msg_ele, msg)
			}
		}
		request.onprogress = (e) => {
			log("ready state: " + request.readyState + " status: " + request.status)
			if (typing==null){
			if (request.status === 100) {
				typing = that.add_typing();
				return;
			}}
		}
		request.onerror = (e) => {
			
			that.not_sent(msg_ele, msg)
		}

		
	function handleEvent(e) {
		log(`${e.type}: ${e.loaded} bytes transferred ${request.status}\n`);
	}

	function addListeners(xhr) {
		xhr.addEventListener('loadstart', handleEvent);
		xhr.addEventListener('load', handleEvent);
		xhr.addEventListener('loadend', handleEvent);
		xhr.addEventListener('progress', handleEvent);
		xhr.addEventListener('error', handleEvent);
		xhr.addEventListener('abort', handleEvent);
	}

	addListeners(request);



	
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
		// use tools.safeJSONParse
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
		// use tools.safeJSONParse
		msg = JSON.parse(msg)
		this.add_chat(this.make_message(msg.text, msg.from));


	}

	async hide_page(){
		this.page.classList.add('hidden');
		top_bar.hide()
		await tools.sleep(500);
		this.page.classList.add('inactive');
		
		//alert("shit")
		// loading_popup()
	}

	show_page(){
		this.page.classList.remove('hidden');
		
		this.page.classList.remove('inactive');
		top_bar.show()
	}
	
	show_max_btn(display=true){
		if(display){
			this.maximize_btn.classList.remove("invisible")
		} else {
			this.maximize_btn.classList.add("invisible")
			
		}
		
	}
	
	
	async minimize(){
		var that = this;
		this.minimized = true;
		
		pages.to_anime()
		
		// to_anime() takes 500ms to take action. So wait for 550ms
		await tools.sleep(550)
		this.show_page();
		this.page.classList.add("minimized")
		this.go_to_bottom()
		top_bar.hide();
		this.show_max_btn()
		
		this.maximize_btn.onclick = () => {
			that.maximize()
		}
		byId("to-chat").classList.add("invisible")
	}
	
	async maximize() {
		this.hide_page()
		this.show_max_btn(false)
		
		// fix animation bug
		await tools.sleep(500);
		
		this.page.classList.remove("minimized")
		byId("to-chat").classList.remove("invisible")
		this.minimized = false;
		
	}
	




}

var chat = new ChatHandler();
// chat.active_page()

// setInterval(chat.get_msg_index.bind(chat), 1500);

