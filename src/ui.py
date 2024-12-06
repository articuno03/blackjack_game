
def header(): 
    return """\
===================================================================
===================================================================
                       Welcome to Blackjack       
===================================================================
===================================================================
(start) to start the game
(chat) to chat with other players
(list) to list all connected players
(quit) to go back
===================================================================
"""


def topScoreboard():
    message = """\
===================================================================
===================================================================
                           Scoreboard
        Enter command (chat, start, list, hit, stand, quit):
-------------------------------------------------------------------
"""
    return message
def userScoreboard(hand):
    message = '''                                                           
    Your hand:''' 
    message += f"{', '.join(hand)}"  
                                                                     
                                                                                                   

    return message

def opponentScoreboard():
    message = '''\
    

--------------------------------------------------------------------

  '''
      
                                              

    return message

def bottomScoreboard():
    message = '''\

===================================================================
'''
    return message