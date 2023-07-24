const log = console.log,
	byId = document.getElementById.bind(document),
	byClass = document.getElementsByClassName.bind(document),
	byTag = document.getElementsByTagName.bind(document),
	byName = document.getElementsByName.bind(document),
	createElement = document.createElement.bind(document);


String.prototype.toHtmlEntities = function() {
	return this.replace(/./ugm, s => s.match(/[a-z0-9\s]+/i) ? s : "&#" + s.codePointAt(0) + ";");
};









function null_func() {
	return true;
}

function line_break() {
	var br = createElement("br");
	return br;
}

function toggle_scroll() {
	document.body.classList.toggle('overflowHidden');
}

function go_link(typee, locate) {
	// function to generate link for different types of actions
	return locate + "?" + typee;
}
// getting all the links in the directory

class Config {
	constructor() {
		this.total_popup = 0;
		this.popup_msg_open = false;
		this.allow_Debugging = true
		this.Debugging = false;
		this.is_touch_device = 'ontouchstart' in document.documentElement;


		this.previous_type = null;
		this.themes = ["Tron"];



		this.is_webkit = navigator.userAgent.indexOf('AppleWebKit') != -1;
		this.is_edge = navigator.userAgent.indexOf('Edg') != -1;

	}
}
var config = new Config();


class Tools {
	// various tools for the page
	refresh() {
		// refreshes the page
		window.location.reload();
	}
	sleep(ms) {
		// sleeps for a given time in milliseconds
		return new Promise(resolve => setTimeout(resolve, ms));
	}
	onlyInt(str) {
		if (this.is_defined(str.replace)) {
			return parseInt(str.replace(/\D+/g, ""));
		}
		return 0;
	}
	c_time() {
		// returns current time in milliseconds
		return new Date().getTime();
	}
	datetime() {
		// returns current date and time
		return new Date(Date.now());
	}
	time_offset() {
		// returns the time offset in milliseconds
		// check https://stackoverflow.com/questions/60207534/new-date-gettimezoneoffset-returns-the-wrong-time-zone
	
	// for the reason of negative sign
		return new Date().getTimezoneOffset() * 60 * 1000 * -1;
	}
	del_child(elm) {
		if (typeof(elm) == "string") {
			elm = byId(elm);
		}
		while (elm.firstChild) {
			elm.removeChild(elm.lastChild);
		}
	}
	toggle_bool(bool) {
		return bool !== true;
	}
	exists(name) {
		return (typeof window[name] !== 'undefined');
	}
	hasClass(element, className, partial = false) {
		if (partial) {
			className = ' ' + className;
		} else {
			className = ' ' + className + ' ';
		}
		return (' ' + element.className + ' ').indexOf(className) > -1;
	}
	addClass(element, className) {
		if (!this.hasClass(element, className)) {
			element.classList.add(className);
		}
	}
	enable_debug() {
		if (!config.allow_Debugging) {
			alert("Debugging is not allowed");
			return;
		}
		if (config.Debugging) {
			return
		}
		config.Debugging = true;
		var script = createElement('script');
		script.src = "//cdn.jsdelivr.net/npm/eruda";
		document.head.appendChild(script);
		script.onload = function() {
			eruda.init()
		};
	}
	is_in(item, array) {
		return array.indexOf(item) > -1;
	}
	is_defined(obj) {
		return typeof(obj) !== "undefined"
	}
	toggle_scroll(allow = 2, by = "someone") {
		if (allow == 0) {
			document.body.classList.add('overflowHidden');
		} else if (allow == 1) {
			document.body.classList.remove('overflowHidden');
		} else {
			document.body.classList.toggle('overflowHidden');
		}
	}
	download(dataurl, filename = null, new_tab=false) {
		const link = createElement("a");
		link.href = dataurl;
		link.download = filename;
		if(new_tab){
			link.target = "_blank";
		}
		link.click();
	}
	
	fake_push(){
		history.pushState({}, document.title, ".")
	}

	full_path(rel_path){
		let fake_a = createElement("a")
		fake_a.href = rel_path;
		return fake_a.href;
	}


	async copy_2(ev, textToCopy) {
		// navigator clipboard api needs a secure context (https)
		if (navigator.clipboard && window.isSecureContext) {
			// navigator clipboard api method'
			await navigator.clipboard.writeText(textToCopy);
			return 1
		} else {
			// text area method
			let textArea = createElement("textarea");
			textArea.value = textToCopy;
			// make the textarea out of viewport
			textArea.style.position = "fixed";
			textArea.style.left = "-999999px";
			textArea.style.top = "-999999px";
			document.body.appendChild(textArea);
			textArea.focus();
			textArea.select();

			let ok=0;
				// here the magic happens
				if(document.execCommand('copy')) ok = 1

			textArea.remove();
			return ok

		}
	}
	
	// pass expected list of properties and optional maxLen
	// returns obj or null
	safeJSONParse(str, propArray, maxLen) {
	    var parsedObj, safeObj = {};
	    try {
	        if (maxLen && str.length > maxLen) {
	            return null;
	        } else {
	            parsedObj = JSON.parse(str);
	            if (typeof parsedObj !== "object" || Array.isArray(parsedObj)) {
	                safeObj = parseObj;
	            } else {
	                // copy only expected properties to the safeObj
	                propArray.forEach(function(prop) {
	                    if (parsedObj.hasOwnProperty(prop)) {
	                        safeObj[prop] = parseObj[prop];
	                    }
	                });
	            }
	            return safeObj;
	        }
	    } catch(e) {
	        return null;
	    }
	}

	fetch_json(url){
		return fetch(url).then(r => r.json()).catch(e => {console.log(e); return null;})
	}
	
	is_standalone(){
		const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
		if (document.referrer.startsWith('android-app://')) {
			return true; // twa-pwa
		} else if (navigator.standalone || isStandalone) {
			return true;
		}
		return false;
	}
	
	is_touch_device(){
		return 'ontouchstart' in document.documentElement;
	}
	
	async is_installed(){
		var listOfInstalledApps = []
		if("getInstalledRelatedApps" in navigator){
			listOfInstalledApps  = await navigator.getInstalledRelatedApps();
		}
		console.log(listOfInstalledApps)
		for (const app of listOfInstalledApps) {
		// These fields are specified by the Web App Manifest spec.
		console.log('platform:', app.platform);
		console.log('url:', app.url);
		console.log('id:', app.id);
		
		// This field is provided by the UA.
		console.log('version:', app.version);
		}
		
		return listOfInstalledApps
	}

	get AMPM_time() {
		var date = new Date();
		var hours = date.getHours();
		var minutes = date.getMinutes();
		var ampm = hours >= 12 ? 'pm' : 'am';
		hours = hours % 12;
		hours = hours ? hours : 12; // the hour '0' should be '12'
		minutes = minutes < 10 ? '0'+minutes : minutes;
		var strTime = hours + ':' + minutes + ' ' + ampm;
		return strTime;
	}
	
	setCookie(cname, cvalue, exdays=365) {
	  const d = new Date();
	  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
	  let expires = "expires="+d.toUTCString();
	  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
	}
	
	getCookie(cname) {
		let name = cname + "=";
		let decodedCookie = decodeURIComponent(document.cookie);
		let ca = decodedCookie.split(';');
		for(let i = 0; i <ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
		}
		return "";
	}
	
	clear_cookie() {
		document.cookie.split(";").forEach(
			function(c) { 
				document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
			}
		);
	}
}
var tools = new Tools();

tools.is_installed()

'#########################################'
if(localStorage.getItem('uname')=="Ray"){
tools.enable_debug() // TODO:[DONE] Disable this in production 
}
'#########################################'

class Popup_Msg {
	constructor() {
		this.made_popup = false;
		this.init()
		this.create()
		this.opened = 0;
	}

	clean() {
		tools.del_child(this.header);
		tools.del_child(this.content);
	}

	init() {
		this.onclose = null_func;
		this.scroll_disabled = false;

		this.popup_container = byId("popup-container");
		if (this.popup_container == null) {
			log("Popup container not found")
			log("Creating new popup container")
			this.popup_container = createElement("div");
			this.popup_container.id = "popup-container";
			document.body.appendChild(this.popup_container);
			const style = createElement("style");
			style.innerHTML = `
.modal_bg {
display: inherit;
position: fixed;
z-index: 1;
padding-top: inherit;
left: 0;
top: 0;
width: 100vw;
height: 100vh;
overflow: auto;
}


.popup {
position: fixed;
z-index: 22;
left: 50%;
top: 50%;
width: 100%;
height: 100%;
overflow: hidden;
transition: all .5s ease-in-out;
transform: translate(-50%, -50%) scale(1)
}

.popup-box {
display: block;
/*display: inline;*/
/*text-align: center;*/
position: fixed;
top: 50%;
left: 50%;
color: #BBB;
transition: all 400ms ease-in-out;
background: #222;
width: 95%;
max-width: 500px;
z-index: 23;
padding: 20px;
box-sizing: border-box;
max-height: min(600px, 80%);
height: max-content;
min-height: 300px;
overflow: auto;
border-radius: 6px;
text-align: center;
overflow-wrap: anywhere;
}

.popup-close-btn {
cursor: pointer;
position: absolute;
right: 20px;
top: 20px;
width: 30px;
height: 30px;
background: #222;
color: #fff;
font-size: 25px;
font-weight: 600;
line-height: 30px;
text-align: center;
border-radius: 50%
}

.popup:not(.active) {
transform: translate(-50%, -50%) scale(0);
opacity: 0;
}


.popup.active .popup-box {
transform: translate(-50%, -50%) scale(1);
opacity: 1;
}

`			
			document.body.appendChild(style);
		}
	}

	create() {
		var that = this;
		let popup_id, popup_obj, popup_bg, close_btn, popup_box;

		popup_id = config.total_popup;
		config.total_popup += 1;



		popup_obj = createElement("div")
		popup_obj.id = "popup-" + popup_id;
		popup_obj.classList.add("popup")

		popup_bg = createElement("div")
		popup_bg.classList.add("modal_bg")
		popup_bg.id = "popup-bg-" + popup_id;
		popup_bg.style.backgroundColor = "#000000EE";
		popup_bg.onclick = function() {
			that.close()
		}

		popup_obj.appendChild(popup_bg);

		this.popup_obj = popup_obj
		this.popup_bg = popup_bg


		popup_box = createElement("div");
		popup_box.classList.add("popup-box")

		close_btn = createElement("div");
		close_btn.className = "popup-btn disable_selection popup-close-btn"
		close_btn.onclick = function() {
			that.close()
		}
		close_btn.innerHTML = "&times;";
		popup_box.appendChild(close_btn)

		this.header = createElement("h1")
		this.header.id = "popup-header-" + popup_id;
		popup_box.appendChild(this.header)

		this.hr = createElement("popup-hr-" + popup_id);
		this.hr.style.width = "95%"
		popup_box.appendChild(this.hr)

		this.content = createElement("div")
		this.content.id = "popup-content-" + popup_id;
		popup_box.appendChild(this.content)
		this.popup_obj.appendChild(popup_box)

		byId("popup-container").appendChild(this.popup_obj)
	}
	close() {
		this.onclose()
		this.dismiss()
		config.popup_msg_open = false;
		this.init()
	}
	hide() {
		this.popup_obj.classList.remove("active");
		tools.toggle_scroll(1)
		this.opened = 0
	}
	dismiss() {

		history.back() //this.hide()
		tools.del_child(this.header);
		tools.del_child(this.content);
		this.made_popup = false;
		
	}

	async open_popup(allow_scroll = false) {
		if (!this.made_popup) {
			return
		}
		
		this.opened = 1
		this.popup_obj.classList.add("active");
		config.popup_msg_open = this;
		
		if (!allow_scroll) {
			tools.toggle_scroll(0);
			this.scroll_disabled = true;
		}
		
		tools.fake_push()
	}

	async show(allow_scroll = false) {
		this.open_popup(allow_scroll)
	}

	async createPopup(header = "", content = "", hr = true, onclose = null_func) {
		this.init()
		this.clean()
		this.onclose = onclose;
		this.made_popup = true;
		if (typeof header === 'string' || header instanceof String) {
			this.header.innerHTML = header;
		} else if (header instanceof Element) {
			this.header.appendChild(header)
		}
		if (typeof content === 'string' || content instanceof String) {
			this.content.innerHTML = content;
		} else if (content instanceof Element) {
			this.content.appendChild(content)
		}
		if (hr) {
			this.hr.style.display = "block";
		} else {
			this.hr.style.display = "none";
		}

	}
}
var popup_msg = new Popup_Msg();

class Toaster {
	constructor() {
		this.container = createElement("div")
		this.container.classList.add("toast-box")
		document.body.appendChild(this.container)

		this.default_bg = "#005165ed";

		this.queue = [];
	}


	async toast(msg, time, bgcolor='') {
		// toaster is not safe as popup by design
		// time is in ms, 0 means no auto close
		var sleep = 3000;

		while (this.queue.length > 2) {
			await tools.sleep(100)
		}
		this.queue.push(1)

		let toaste = createElement("div")
		toaste.classList.add("toast-body")
		
		this.container.appendChild(toaste)

		await tools.sleep(50) // wait for dom to update
		
		// SET BG COLOR
		toaste.style.backgroundColor = bgcolor || this.default_bg;

		toaste.innerText = msg;
		toaste.classList.add("visible")
		if(tools.is_defined(time)) sleep = time;
		await tools.sleep(sleep)
		toaste.classList.remove("visible")
		await tools.sleep(500)
		toaste.remove()

		this.queue.pop()

	}
}

var toaster = new Toaster()



function r_u_sure({y=null_func, n=null, head="Head", body="Body", y_msg="Yes",n_msg ="No"}={}) {
	popup_msg.close()
	var box = createElement("div")
	var msggg = createElement("p")
	msggg.innerHTML = body; //"This can't be undone!!!"
	box.appendChild(msggg)
	var y_btn = createElement("div");
	y_btn.innerText = y_msg;//"Continue"
	y_btn.className = "pagination center";
	y_btn.onclick = y;/*function() {
		that.menu_click('del-p', file);
	};*/
	var n_btn = createElement("div");
	n_btn.innerText = n_msg;//"Cancel"
	n_btn.className = "pagination center";
	n_btn.onclick = () => {return (n==null) ? popup_msg.close() : n()};
	box.appendChild(y_btn);
	box.appendChild(line_break());
	box.appendChild(n_btn);
	popup_msg.createPopup(head, box) ; //"Are you sure?"
	popup_msg.open_popup();
}

function loading_popup() {
	popup_msg.close()
	var box = createElement("div")
	box.innerHTML = `
<svg width="200" height="200" viewBox="0 0 100 100">
  <polyline class="line-cornered stroke-still" points="0,0 100,0 100,100" stroke-width="10" fill="none"></polyline>
  <polyline class="line-cornered stroke-still" points="0,0 0,100 100,100" stroke-width="10" fill="none"></polyline>
  <polyline class="line-cornered stroke-animation" points="0,0 100,0 100,100" stroke-width="10" fill="none"></polyline>
  <polyline class="line-cornered stroke-animation" points="0,0 0,100 100,100" stroke-width="10" fill="none"></polyline>
</svg>

<div class="wrapper">
<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>
<div class="shadow"></div>
<div class="shadow"></div>
<div class="shadow"></div>
</div>



<link rel="stylesheet" href="./style_loading.css">
`
	popup_msg.createPopup("Loading...", box) ; //"Are you sure?"
	popup_msg.open_popup();
}




