# UPDATES

Lots of progress made. Heres a list of whats new...

 - the initial commands are working as planned
   1. "start" begins a queue for beginning the game
   2. "chat" properly sends the player into chat mode
   3. "exit_chat" allows player to go back out of chat
   4. "list" properly lists connected players
   5. "quit" allows players to leave game

- Game Logic:
- When all players are ready the server properly deals out cards
- each player is shown 1 of the other players cards and the first player to take a turn is indicated
- once the first player is finished indicated by a stand or bust, the next player is prompted
- once all players finish their turns, the game ends and a winner is declared

- exit_chat
- I added a new option called exit_chat that is only prompted in chat mode. This works better than using quit because quit is used to exit the connection

- Known Bugs:
  1. Existing Username
    - Checking for existing usernames. Sometimes the players.json file will not properly delete players who disconnect and store their username so you cant take that username
    - in later joins. This will need to be fixed as if you type an existing username it essentially crashes
  2. Resetting the game
    - The game does not properly reset after a winner is declared. This needs to be implemented
  3. Other
    - There are some other bugs I cant think of at the moment but please add to the list when you come across any


Going forward...
- Nearing the finish line, just need to do some cleanup and error handling. We need to test for various edge cases
- There will be a lot of error handling that needs to be done.

# IMPORTANT NOTE
- Be super careful about what gets merged I had some close calls
