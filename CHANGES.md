# UPDATES

Lots of progress made. Heres a list of whats new...

 - the initial commands are working as planned
   1. "start" begins a queue for beginning the game
   2. "chat" properly sends the player into chat mode
   3. "exit_chat" allows player to go back out of chat
   4. "list" properly lists connected players
   5. "quit" allows players to leave game

- Game Logic:
- So far the code properly deals out cards randomly to connected players
- Need to add hit and stand features to work properly
- The rest of the calculations for game outcome are included but not tested at the moment, this will be easier once player turns are correctly implemented

- exit_chat
- I added a new option called exit_chat that is only prompted in chat mode. This works better than using quit because quit is used to exit the connection

- Known Bugs:
  1. Existing Username
- Checking for existing usernames. Sometimes the players.json file will not properly delete players who disconnect and store their username so you cant take that username
- in later joins. This will need to be fixed as if you type an existing username it essentially crashes
  2. Stand and Hit Not Implemented
  - The code stops after the cards are dealt so this will need to be added
  3. Other
    - There are some other bugs I cant think of at the moment but please add to the list when you come across any


Going forward...
- Nearing the finish line, just need to finish the game logic and clean some stuff up for the final product.

# IMPORTANT NOTE
- Be super careful about what gets merged I had some close calls
