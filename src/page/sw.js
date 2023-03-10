__sw_version__ = "09-mar_2023"

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('ai-girl').then((cache) => cache.addAll([
	"https://i.ibb.co/jGGGYw4/image.webp", //  japan feild */
	"https://i.ibb.co/KqYGB5t/image.webp", //#  shower */
	"https://i.ibb.co/WVyzpvz/image.webp", //#  spring room */
	"https://i.ibb.co/8dbTJbM/image.webp", //#  sitting room */
	"https://i.ibb.co/9tbsVCB/image.webp", //#  bed room */
	"https://cdn.jsdelivr.net/gh/hung1001/font-awesome-pro-v6@44659d9/css/all.min.css" // font awesome cdn
])),
  );
});

self.addEventListener('fetch', (e) => {
  console.log(e.request.url);
  e.respondWith(
    //caches.match(e.request).then((response) => fetch(e.request) || response),
    fetch(e.request)
  );
});
