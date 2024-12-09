# Blackjack Game

This is a simple blackjack game created for online multiplayer

**How to run**
1. **Verify IP Address:** First you must ensure that the IP Address in both server.py and client.py are setup to communicate properly.
2. **Ensure an open Port:** Ensure you are using an open port number that is not currently being used.
3. **Start the server:** Run the `server.py` script.
4. **Connect clients:** Run the `client.py` script on two different machines or terminals.
5. **Enter a valid Username:** Begin by entering a username that has not been taken.
6. **Welcome Screen:** If the following steps have been done, you should see a welcome screen that will outline various commands.

**How to play:**
1. **Start the game:** In order to start the game, all players must ready up with the specified "start" command.
2. **Place your bet:** Each player is given $100 to bet with. In order to place a bet, use the "bet" command and hit enter. Following this enter the specified amount you would like to bet.
3. **Initial Cards:** Each player will be given two cards. The game board will show each players cards as well as **one** dealer card.
4. **Turn Order:** During your turn, you may choose to hit or stand depending on your card hand.
5. **Hit:** If you choose to hit, you will be given another card to add to your total hand value.
6. **Stand:** If you choose to stand, your turn is over and your current hand of cards is final and can't be added to.
7. **Bust!:** If the total of your cards exceeds 21, you will bust and essentially lose that hand.
8. **21:** The goal of the game is to get as close to a hand total of 21 as possible without exceeding. You are playing against the dealer.
9. **Face Cards & Aces:** A face card (J,Q,K) is worth 10 points, an Ace is worth either 1 point or 11 points based on your total.
10. **Have Fun:** Enjoy the game and try to win fake money!

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to Python documentation]
* https://docs.python.org/3/library/socket.html
* https://www.geeksforgeeks.org/socket-programming-python/

# Statement of Work

**Project**
* BlackJack

**Team**
* Garret Tilton and Will Fagerstrom

**Objective**
*We will be creating a simple online blackjack game. There will be a betting system and graphics for cards.

**Scope**
* Inclusions: A fake money system in the form of chips, a graphical representation of cards and a table, the blackjack game itself, a set of rules on the side for new players.
* Exclusions: Animations, no more than 2 players

**Deliverables**
* Various python scripts for controlling sockets, game mechanics, and a graphical interface. A document outlining the project. A rulebook.

**Timeline**
* Milestones:
* Task Breakdown:

**Technical Requirements**
*Hardware
*Software

**Assumptions**
*Assumptions: We created the project with a simple layout of commands to help guide new users in navigating the game.

**Role and Responsibilities**
*Roles: During the development of the game, Garret and Will bounced back and forth in writing the code and used pull requests to check each others new additions before making any changes to main. This ensured main was never broken.

**Communication Plan**
*Channels: Garret and Will texted throughout the semester to plan meeting times. We met every Tuesday and Thursday at noon to work for several hours.

**Additional Notes**
*Notes

**Roadmap**
*Future Releases: Continuing in development of the game, we would like to implement some additional features common to the game of blackjack...
1. **Split and Double:** These options allow the player to split their hand or double their bet based on certain conditions such as 2 of the same card or an Ace and 7.
2. **Money Tracking:** We did not implement a way for players to see their current money totals. This would be a useful thing to implement.
3. **Dynamic IP and Port:** This is something we were missing in our final release and we would like to implement.
4. **Web UI:** We would like to provide a popup UI, allowing for more creativity in graphics and features.
5. **Encryption** We would like to make the user have a encrypted password so when they exit the server their stuff is still protected and saved and they can log back on to their specific user.
**Retrospective**
1. **What Went Well:**
   - Overall, I think what went well is that we planned on keeping the game simple to reduce the amount of possible bugs and errors in the code. This was a smart choice and saved us some headaches in the long run.
   - We delegated time very well throughout the semester and established set times every week to meet and discuss the project.
   - Communication was vital in the team aspect of the project and our vision of the game was shared and agreed upon.
   - In the end the project worked well, they game was able to be played correctly with multiple player including the dealear.  The game worked according to the rules and each player was allowed to bet with an ingame curreny that can be saved with them for the next games they want to play.
2. **Improvements:**
   - Towards the end of the semester, we were a little behind in the development of the game. This caused us to rush some of the later features and miss a few bugs.
   - We did very little in the area of testing the code. This would have helped us greatly and allowed us to avoid some big challenges we faced.

# Sprint 1: Implement TCP Client/Server
* Properly established a connection between client and server with the max number of clients set to 10.
* Included error handling for improper Host and Port as well as unsuccessful connections

# Sprint 2: Design and Implement Message Protocol
* Messages can be sent between clients and received by the server.
* Format of the messages consist of Join, Chat, Start, and Quit
* Server side parses messages based on input and will send messages based on type
* Properly sends error messages when incorrect messaging is sent over the server
* TODO: Implement a list of connected clients

# Sprint 3: Multiplayer Functionality, Synchronize State Across Clients
* TODO: Assign unique ID's for each client
* TODO: Create class: OutputFormat
* TODO: Create class: CardManager
* TODO: Create class: GameLogic
* TODO: Begin game and send game board with message "Start"
* TODO: Shuffle array list of cards and send to clients

# Sprint 4: Gameplay, Game State, UI
* TODO: Allow for player input and iterate through player turns
* TODO: Implement "House" player as server
* TODO: Implement win conditions
 
# Sprint 5: Implement Error Handling and Testing
* TODO: Proplerly Handle Errors and Test Mechanics

# Sprint 6: Additional Bonus Features
* TODO: Implement Money System
* TODO: Implement Split and Double Functionality
* TODO: Implement BlackJack Win Status

# Sprint X: Web Server/Client UI and Encryption
* Our team did not complete the extra credit implementations for the physical UI and Encryptions as a majority of the focus was towards getting the game to function correctly.
