from network import InternetChecker
from colored import fg, bg, attr
from motiondetect import MotionDetector
def colored_print(text, color, background='black', attributes=[]):
    color_text = fg(color) + bg(background)
    for attribute in attributes:
        color_text += attr(attribute)
    color_text += text + attr('reset')
    print(color_text)

def main():
    print(r"""\

      _...._
    /       \
   /  o _ o
   (    \/  )
  )          (
(    -  -  -  )
(             )
 (            )
  [          ]
---/l\    /l\--------
  ----------------
     (  )
    ( __ _)
                """)
    print(r""" 
  ____    _____   _____    _____    ____    _    _   _____    _____   __     __
 |  _ \  |_   _| |  __ \  |  __ \  |  _ \  | |  | | |  __ \  |  __ \  \ \   / /
 | |_) |   | |   | |__) | | |  | | | |_) | | |  | | | |  | | | |  | |  \ \_/ / 
 |  _ <    | |   |  _  /  | |  | | |  _ <  | |  | | | |  | | | |  | |   \   /  
 | |_) |  _| |_  | | \ \  | |__| | | |_) | | |__| | | |__| | | |__| |    | |   
 |____/  |_____| |_|  \_\ |_____/  |____/   \____/  |_____/  |_____/     |_|   
                                                                                         
          """)
    internet_checker = InternetChecker()
    internet_checker.check_internet()
    detector = MotionDetector(debug=True)
    detector.run()
if __name__ == "__main__":
    main()
    