from pathlib import Path
import os
### TEXTS ###

CONFIGURE_TITLE = """
 _____    _                               
|_   _|  | |                              
  | | ___| | _____      ___ __ __ _ _ __  
  | |/ _ \ |/ _ \ \ /\ / / '__/ _` | '_ \ 
  | |  __/ |  __/\ V  V /| | | (_| | |_) |
  \_/\___|_|\___| \_/\_/ |_|  \__,_| .__/ 
                                   | |    
                                   |_|    



"""
CONFIGURE_TOKEN = """
To get started, you need to create a new Telegram bot. Follow these steps:
1. Open the Telegram app and search for BotFather
2. Follow the instructions to create a new bot
3. Copy the token provided by BotFather and paste it below

For more detailed instructions, visit: https://core.telegram.org/bots/features#creating-a-new-bot
"""

CONFIGURE_SUBSCRIPTION = """
Great, now you just need to subscribe some users to your bot. Follow these steps:
1. Go to your bot in the Telegram app and send the message '/start' to start a conversation
2. (Optional) Repeat step 1 for every user you want to subscribe, for updates from telewrap
3. Send the message '/end' to your bot to complete the configuration process
"""

CONFIGURE_END = """
That's it! Your Telewrap configuration is complete.
If you find it useful, please consider starring the Telewrap repository on GitHub.

Thank you for using Telewrap!
"""

CONFIGURE_TOKEN_ERROR = """
Invalid token received: '{token}'. Make sure you have created a Telegram bot and copied the token correctly.
"""

### ENV ###
CONFIG_PATH = (Path(os.environ.get("TELEWRAP_CONFIG_DIR","~/.config")) / ".telewrap.config").expanduser().absolute()
