import platform
import os

banner1 = """
████████╗██╗███████╗     ██╗██╗ █████╗ ███╗   ██╗██╗  ██╗██╗   ██╗██████╗  █████╗ ███╗   ██╗
╚══██╔══╝██║██╔════╝     ██║██║██╔══██╗████╗  ██║██║ ██╔╝██║   ██║██╔══██╗██╔══██╗████╗  ██║
   ██║   ██║█████╗       ██║██║███████║██╔██╗ ██║█████╔╝ ██║   ██║██║  ██║███████║██╔██╗ ██║
   ██║   ██║██╔══╝  ██   ██║██║██╔══██║██║╚██╗██║██╔═██╗ ██║   ██║██║  ██║██╔══██║██║╚██╗██║
   ██║   ██║███████╗╚█████╔╝██║██║  ██║██║ ╚████║██║  ██╗╚██████╔╝██████╔╝██║  ██║██║ ╚████║
   ╚═╝   ╚═╝╚══════╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
                                                                                            
"""

banner2 = """
                                 .---.                                                                                    
                                 |   |                                                 _______                            
         .--.      __.....__     '---'.--.             _..._        .                  \  ___ `'.                _..._    
         |__|  .-''         '.   .---.|__|           .'     '.    .'|                   ' |--.\  \             .'     '.  
     .|  .--. /     .-''"'-.  `. |   |.--.          .   .-.   . .'  |                   | |    \  '           .   .-.   . 
   .' |_ |  |/     /________\   \|   ||  |    __    |  '   '  |<    |                   | |     |  '    __    |  '   '  | 
 .'     ||  ||                  ||   ||  | .:--.'.  |  |   |  | |   | ____      _    _  | |     |  | .:--.'.  |  |   |  | 
'--.  .-'|  |\    .-------------'|   ||  |/ |   \ | |  |   |  | |   | \ .'     | '  / | | |     ' .'/ |   \ | |  |   |  | 
   |  |  |  | \    '-.____...---.|   ||  |`" __ | | |  |   |  | |   |/  .     .' | .' | | |___.' /' `" __ | | |  |   |  | 
   |  |  |__|  `.             .' |   ||__| .'.''| | |  |   |  | |    /\  \    /  | /  |/_______.'/   .'.''| | |  |   |  | 
   |  '.'        `''-...... -'__.'   '    / /   | |_|  |   |  | |   |  \  \  |   `'.  |\_______|/   / /   | |_|  |   |  | 
   |   /                     |      '     \ \._,\ '/|  |   |  | '    \  \  \ '   .'|  '/            \ \._,\ '/|  |   |  | 
   `'-'                      |____.'       `--'  `" '--'   '--''------'  '---'`-'  `--'              `--'  `" '--'   '--' 
"""

banner3 = """
 _____ _        ___ _             _   __     ______            
|_   _(_)      |_  (_)           | | / /     |  _  \           
  | |  _  ___    | |_  __ _ _ __ | |/ / _   _| | | |__ _ _ __  
  | | | |/ _ \   | | |/ _` | '_ \|    \| | | | | | / _` | '_ \ 
  | | | |  __/\__/ | | (_| | | | | |\  | |_| | |/ | (_| | | | |
  \_/ |_|\___\____/|_|\__,_|_| |_\_| \_/\__,_|___/ \__,_|_| |_|
                                                               
                                                               
"""

banner4 = R"""
 ______            _____                       __  __          ____                       
/\__  _\__        /\___ \  __                 /\ \/\ \        /\  _`\                     
\/_/\ \/\_\     __\/__/\ \/\_\     __      ___\ \ \/'/'  __  _\ \ \/\ \    __      ___    
   \ \ \/\ \  /'__`\ _\ \ \/\ \  /'__`\  /' _ `\ \ , <  /\ \/\ \ \ \ \ \ /'__`\  /' _ `\  
    \ \ \ \ \/\  __//\ \_\ \ \ \/\ \L\.\_/\ \/\ \ \ \\`\\ \ \_\ \ \ \_\ /\ \L\.\_/\ \/\ \ 
     \ \_\ \_\ \____\ \____/\ \_\ \__/.\_\ \_\ \_\ \_\ \_\ \____/\ \____\ \__/.\_\ \_\ \_\
      \/_/\/_/\/____/\/___/  \/_/\/__/\/_/\/_/\/_/\/_/\/_/\/___/  \/___/ \/__/\/_/\/_/\/_/
                                                                                          
                                                                                          
"""

banner5 = """
   ▄▄▄▄▀ ▄█ ▄███▄    ▄▄▄▄▄ ▄█ ██      ▄   █  █▀  ▄   ██▄   ██      ▄   
▀▀▀ █    ██ █▀   ▀ ▄▀  █   ██ █ █      █  █▄█     █  █  █  █ █      █  
    █    ██ ██▄▄       █   ██ █▄▄█ ██   █ █▀▄  █   █ █   █ █▄▄█ ██   █ 
   █     ▐█ █▄   ▄▀ ▄ █    ▐█ █  █ █ █  █ █  █ █   █ █  █  █  █ █ █  █ 
  ▀       ▐ ▀███▀    ▀      ▐    █ █  █ █   █  █▄ ▄█ ███▀     █ █  █ █ 
                                █  █   ██  ▀    ▀▀▀          █  █   ██ 
                               ▀                            ▀          
"""

if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")

if not os.path.exists("./img"):
    os.mkdir("./imgs")

if not os.path.exists("./logs"):
    os.mkdir("./logs")

print(banner3)
