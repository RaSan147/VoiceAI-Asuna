
if (window.history && "pushState" in history) {
	// because JSHint told me to
	// handle forward/back buttons
	window.onpopstate = async function (evt) {
		"use strict";
		evt.preventDefault();
		// guard against popstate event on chrome init
		//log(evt.state)
		if(pages.current_page=="chat"){
			pages.current_page= "home"
			
			history.replaceState({page:"home"}, "Home", ".")

			pages._to_anime()
			return
		}
		//location.reload();
	};

}

