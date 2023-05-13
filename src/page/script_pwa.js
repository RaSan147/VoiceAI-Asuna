

if (window.history && "pushState" in history) {
	// because JSHint told me to
	// handle forward/back buttons
	window.onpopstate = async function (evt) {
		"use strict";
		evt.preventDefault();
		// guard against popstate event on chrome init
		//log(evt.state)
		if(popup_msg.opened){
			popup_msg.hide()
			//fake_push()
			return false
		}
		if(sidebar_control.is_open("R")){
			sidebar_control._closeNavR()
			//fake_push()
			return false
		}
		
		if(pages.current_page=="chat"){
			pages.current_page = "home"
			//fake_push()
			pages._to_anime()
			return false
		}
		
		//location.reload(true);
	};

}


