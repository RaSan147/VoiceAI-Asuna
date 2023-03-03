var app_installed = false
var notify_install = false

if (0 && 'serviceWorker' in navigator) {
  navigator.serviceWorker
    .register('/sw.js')
    .then(() => { console.log('Service Worker Registered'); });
}

var install_btn = byId("to-install")
var open_pwa_btn = byId("to-open-pwa")

open_pwa_btn.onclick = (e) => {
	window.open('.', '_blank');
}

if(!tools.is_standalone() && tools.is_touch_device()){
	notify_install = true
}

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  app_installed = false; 

	
	if(!notify_install){
		return
	}
  e.preventDefault();
  // Stash the event so it can be triggered later.
  deferredPrompt = e;
  // Update UI to notify the user they can add to home screen
  install_btn.style.display = 'block';

  install_btn.onclick = () => {
    // hide our user interface that shows our A2HS button

    install_btn.style.display = 'none';
    // Show the prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the A2HS prompt');
        app_installed = true;
        install_btn.style.display = "none"
        toaster.toast("Installing...")
      } else {
        console.log('User dismissed the A2HS prompt');
        app_installed = false;
      }
    });
  }
})


window.addEventListener('appinstalled', () => {
  // Clear the deferredPrompt so it can be garbage collected
  deferredPrompt = null;
  open_pwa_btn.style.display = "block"
});

async function getInstalledApps() {
  const installedApps = await navigator.getInstalledRelatedApps();

  if(notify_install && installedApps){
  	open_pwa_btn.style.display = "block"
  }
  
  return installedApps
}

if ('getInstalledRelatedApps' in navigator) {
  getInstalledApps();
} else {
  log("pwa check up not supported")
}



const GOOGLE_VENDOR_NAME = 'Google Inc.';

function isOpera(){
  return Boolean(window.opr);
}

function isChromium() {
  return Boolean(window.chrome);
}



const _userAgent = window.navigator.userAgent;
const _vendor = window.navigator.vendor;
var _browserName = null;
function getBrowserName() {
	let userAgent = _userAgent
	let vendor = _vendor
	if (_browserName){
		return _browserName
	}
  switch (true) {
    case /Edge|Edg|EdgiOS/.test(userAgent):
      return 'Edge';
    case /OPR|Opera/.test(userAgent):
      return 'Opera';
    case /CriOS/.test(userAgent):
    case /Chrome/.test(userAgent) && vendor === GOOGLE_VENDOR_NAME && isChromium():
      return 'Chrome';
    case /Vivaldi/.test(userAgent):
      return 'Vivaldi';
    case /YaBrowser/.test(userAgent):
      return 'Yandex';
    case /Firefox|FxiOS/.test(userAgent):
      return 'Firefox';
    case /Safari/.test(userAgent):
      return 'Safari';
    case /MSIE|Trident/.test(userAgent):
      return 'Internet Explorer';
    default:
      return 'Unknown';
  }
}

_browserName = getBrowserName()

function isChrome() {
  const name = getBrowserName();
  return name === 'Chrome';
}

function to_install_if_not_chrome(){
	install_btn.style.display="block"
	install_btn.onclick= () => {
		popup_msg.show()
	}
	var body = createElement("div")
	var msg = createElement("p")
	
	msg.innerHTML = `To install, please click <b>&#8962; Add to Home Screen</b>
	<br>
	<h2>Already installed?</h2>
	Kindly open it from <b>Home screen</b>
	<br>
	<h2>Why?</h2>
	This app works & looks better on fullscreen, without any outlines and other things. And if you are seeing this, you're probably not using chrome, no problem... Just follow above steps to manually install (Chrome does that in better ways)
	`
	
	
	popup_msg.createPopup("Install as PWA for the best Experience", msg
		)
}

if(notify_install && !isChrome()){
	to_install_if_not_chrome()
}

