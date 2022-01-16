# telewrap

`telewrap` is a utility that lets you run bash cmdline
and send a message to you or to your friends when the shell finishes
to run

## How To Install

```
git clone https://github.com/Maimonator/telewrapper.git
cd telewrapper
pip3 install -r requirements.txt
python3 telewrapper.py configure <TOKEN>
python3 telewrapper.py install -u <USER>
```

* First use telegram's `@BotFather` to create your bot and receive its `token`
* run `telewrapper.py configure [token]`  to configure telewrapper to send you a message
	* On telegram, go to the chat with your new bot and send `/subscribe [username]` with a username that will identify your uid
* run `sudo telewrapper.py install -u [users]` where `users` is a list of users
  you want to send them a message
* now just add `telewrap` before any cmdline you'd like to execute `telewrap sleep 5`
