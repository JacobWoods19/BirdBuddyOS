import sys
from network import InternetChecker
from colored import fg, bg, attr
from motiondetect import MotionDetector
from pushover import PushoverHandler

def colored_print(text, color, background='black', attributes=[]):
    color_text = fg(color) + bg(background)
    for attribute in attributes:
        color_text += attr(attribute)
    color_text += text + attr('reset')
    print(color_text)

def prompt_yes_no(message):

    while True:
        user_input = input(f"{message} (y/n): ").strip().lower()
        if user_input in {'y', 'n'}:
            return user_input == 'y'
        colored_print("Invalid input, please enter 'y' or 'n'.", 'red')

def prompt_integer(message, range=None):

    while True:
        try:
            value = int(input(f"{message}: "))
            if range and (value < range[0] or value > range[1]):
                raise ValueError(f"Please enter a value between {range[0]} and {range[1]}")
            return value
        except ValueError as e:
            colored_print(str(e), 'red')

def setup_pushover():
    """ Handles Pushover setup. """
    if prompt_yes_no("Enable Pushover notifications?"):
        user_key = input("Enter user key: ")
        api_key = input("Enter API key: ")
        time_enabled = prompt_yes_no("Enable time in notifications?")
        return PushoverHandler(api_key, user_key, time_enabled=time_enabled)
    return None

def print_banner():
    banner = r"""
                                                       _...--.
                                       _____......----'     .'
                                 _..-''                   .'
                               .'                       ./
                       _.--._.'                       .' |
                    .-'                           .-.'  /
                  .'   _.-.                     .  \   '
                .'  .'   .'    _    .-.        / `./  :
              .'  .'   .'  .--' `.  |  \  |`. |     .'
           _.'  .'   .' `.'       `-'   \ / |.'   .'
        _.'  .-'   .'     `-.            `      .'
      .'   .'    .'          `-.._ _ _ _ .-.    :
     /    /o _.-'               .--'   .'   \   |
   .'-.__..-'                  /..    .`    / .'
 .'   . '                       /.'/.'     /  |
`---'                                   _.'   '
                                      /.'    .'
                                       /.'/.'
                                       
                    
_________ .__  .__                     __________.__           .___
\_   ___ \|  | |__|_____ ______ ___.__.\______   \__|______  __| _/
/    \  \/|  | |  \____ \\____ <   |  | |    |  _/  \_  __ \/ __ | 
\     \___|  |_|  |  |_> >  |_> >___  | |    |   \  ||  | \/ /_/ | 
 \______  /____/__|   __/|   __// ____| |______  /__||__|  \____ | 
        \/        |__|   |__|   \/             \/               \/ 
                   
                                       
                                       
                                       """
    print(banner)

def main():
    print_banner()
    print("Turn Your Pi into a Smart Bird Feeder - Version 1.0\n")
    internet_checker = InternetChecker()
    internet_checker.check_internet()
    debug = prompt_yes_no("Enable debug mode? Debug mode will display what the camera sees")
    cool_down_time = prompt_integer("Enter cool down time (seconds)")
    sensitivity = prompt_integer("Enter sensitivity (0-1000, 500 recommended)", (0, 1000))
    pushover = setup_pushover()
    
    detector = MotionDetector(debug=debug, cool_down_time=cool_down_time, pushover=pushover, sensitivity=sensitivity)
    if not detector.validate_camera_connected():
        sys.exit("No camera connected, exiting.")
    
    detector.run()

if __name__ == "__main__":
    main()
