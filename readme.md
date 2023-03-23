PROJECT Asuna (NOT AI yet)
-------------
<p align="center"><img src="https://user-images.githubusercontent.com/34002411/214065966-6fcbd90f-0948-42dd-b846-5e6130a78421.jpg" alt="ASUNA SAO"/></p>

Welcome to project Asuna.

## Live Demo: https://aigirl.repl.co
*(voice unavailable)*


# Description:
* **This is not a ChatGPT or full blown all knowing AI**
* This is an English only, pattern based chat bot (for now)
* Currently using regular expressions to catch and reply specific patterns of messaged and collecting inputs and unknown inputs to train in future
* Once, With sufficient data and resources, we will perform AI training
* If you have any idea or want to provide IO datas, please file an Issue or Pull Request
* Documentation will be created soon for ease of group development.
* Currently this is an one man project and my 1st language is not English, Using 1000 years of knowledge from animes and movies to enreach the chat input response.
* So please don't expect much but I hope I'll be able to provide great performance with it.

* **Please have patience** Maintaining completely new (self made) server, UI and back end is not easy task (for me). Then again adding IO based patterns, sequencing them takes time.


* My/Our main goal is to create a Multi platform accessable voice assistant.

* our additional plan is to create their animated avatar and make it available online (via Browsers)


# Current status:
- [x] Create server and web UI
- [x] Add anime live2D
- [x] Connect chat 
- [x] Server and UI improvements
- [x] Add intent and context
- [ ] Understand and reply according to context
- [ ] Add more Commands
- [ ] Add voice recognition
- [ ] Add voice output
- [ ] Add anime live2D animations
- [ ] Improve sidebars
- [ ] Allow bot send pictures
- [ ] Allow bot send audio
- [ ] Allow bot send video




# How To Run:
* **First** install the [REQUIREMENTS](/REQUIREMENTS.md), click it to see details
* To Launch the server run the [RUN_ME.py](/RUN_ME.py) file
  ```
  python RUN_ME.py
  ```
* Demo video coming soon...


# Requirement:
* Python 3.7 or higher
* Works on Android Pydroid 3 😄 too (most develoment is done using this)


# Common IO: (similar inputs may/will work too)
* Basic `hiiii`, `hello`
* `What's your/my name` / `how're u`
* `Whats the time` / `tell time`
* <ins>**Static Q/A**</ins>, like `whats newtons 3rd law` / `whos the president of canada` / `whats root(69+420)`
* `Whats the latest news` / `news highlights`
* `Tell me about yourself` / `... your hobby/favorite game/anime`
* `Love ya`
* `Repeat after me` -> will reply whatever you say next. Say `stop/stop repeating` to stop
* `change dress` to change costumes and `change room` to switch background 
* **Many more (forgot mostly) and many more coming soon**


# CONTRIBUTION GUIDELINE:
* Make changes on whatever you feel like
* Place some good comments (so that an intermediate python programmer can understand)
* Make a PR and try to explain what you have changed and if theres any issue.
* Keep in mind if you are interested :
  * pyrobox.py is the server main file (like django or flask)
  * App_server.py is the file that handles client-host request responses.
  * Chat_raw2.py is the tool that actually handles what msg will do what and reply what (can be used as standalone in CLI mode for development mode, will use test account)
* Don't worry about marge-issue, I'll update the code
* Most importantly AS A MOBILE CODER, I USUALLY DON'T FOLLOW ANY CODE STYLE GUIDELINE (or pep8), SO PLEASE DON'T WORRY ABOUT THAT TOO MUCH. (I'll try to follow it in future)

# Thanks to:
0. Reki Kawahara and abec (for creating Asuna)
1. Sony group (for Wake me up Asuna App idea and illustrations)
2. Pixi.js and live2D for character animation
3. Replit for continuously hosting Demo link for free
4. (Coming soon) Anyone who's willing to share chat data and ideas

# Additional members:
0. https://github.com/coolst3r (technical and knowledge-base support)
