# telewrap

`telewrap` is a utility that lets you run bash cmdline
and send a message to you or to your friends when the shell finishes
to run

## How To Install

* First use telegram's `BotFather` to create your bot and receive its `token`
* run `telewrapper.py configure [token]`  to configure telewrapper to send you a message
  send `/subscribe [username]` with a username that will identify your uid
* run `sudo telewrapper.py install -u [users]` where `users` is a list of users
  you want to send them a message
* now just add `telewrap` before any cmdline you'd like to execute `telewrap sleep 5`
