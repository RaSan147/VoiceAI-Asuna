self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('fox-store').then((cache) => cache.addAll([
	"https://i.ibb.co/jGGGYw4/image.webp", //  japan feild */
	"https://i.ibb.co/KqYGB5t/image.webp", //#  shower */
	"https://i.ibb.co/WVyzpvz/image.webp", //#  spring room */
	"https://i.ibb.co/8dbTJbM/image.webp", //#  sitting room */
	"https://i.ibb.co/9tbsVCB/image.webp", //#  bed room */
])),
  );
});

self.addEventListener('fetch', (e) => {
  console.log(e.request.url);
  e.respondWith(
    caches.match(e.request).then((response) =>  response || fetch(e.request)),
  );
});
