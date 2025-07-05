import os

"""Prints a styled launch message with an ASCII logo and application details."""

def print_launch_message():
    ascii_logo = r"""
                  ██████████████                  
              ██████████████████████              
           ████████████████████████████           
        ██████████████████████████████████        
      ██████████████████████████████████████      
     ████████████████████████████████████████     
    ████████   ████████████████████   ████████    
  ██████████      ███        ███      ██████████  
  ██████████                          ██████████  
 ███████████                          ███████████ 
██████████                              ██████████
█████████████                        █████████████
██████████  ██████████████████████████  ██████████
██████████   ██ ████                    ██████████
██████████   ████████                   ██████████
███████████  ███ ████                  ███████████
████████████████ █████               ██ ██████████
 ███████████  █████████████████████   ███████████ 
 █████████████                      █████████████ 
  ██████████████████           █████████████████  
   █████████████████   ████   █████████████████   
    ██████████████              ██████████████    
     ██████████   ███        ███   ██████████     
       ██████████ █████    █████ ██████████       
         ███████████████  ███████████████         
           ████████            ████████           
              █████            █████              

 ██████╗ ███████╗████████╗██╗  ██╗██╗   ██╗██████╗ 
██╔════╝ ██╔════╝╚══██╔══╝██║  ██║██║   ██║██╔══██╗
██║  ███╗█████╗     ██║   ███████║██║   ██║██████╔╝
██║   ██║██╔══╝     ██║   ██╔══██║██║   ██║██╔══██╗
╚██████╔╝███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝
 ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
    """

    message = f"""
[MAIN] Launching main App...
-----------
{ascii_logo}
Gethub - A Ride Booking App
Developed by Group 4 - Regularn't

This application is submitted as a final requirement for:
CMPE 103 - Object-Oriented Programming  
Polytechnic University of the Philippines - Sta. Mesa, Manila

Members:
Mark Abucejo      - Lead Developer
Zybert Sibolboro  - Full Stack Developer
Renier Dela Cruz  - Backend Developer
Lorens Mercado    - Backend Developer
Kathlyn Estorco   - UI/UX Designer
Maeryl Venida     - UI/UX Designer
Luke Lopez        - QA/Test Engineer

GitHub Repository: 
https://github.com/nug3tsss/ride-booking-system/

"""

    # ANSI green color for the whole block (only works in terminals)
    green = "\033[92m"
    reset = "\033[0m"

    # Clear console
    os.system("cls" if os.name == "nt" else "clear")

    # Print styled message
    print(green + message + reset)
