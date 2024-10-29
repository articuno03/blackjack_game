# Blackjack Game

This is a simple blackjack game created for online multiplayer

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Play the game:** Two players load in and 2 cards are randomly given to each player. One face up, one face down.
4. **Option** Can choose to hit or stay. If over 21, you lose.
5. **Opponent Option** Takes their turn to hit or stay.
6. **Cards Revealed** The winner is decided
7. **Additional Options** Split

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to Python documentation]
* [Link to sockets tutorial]

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
*Assumptions

**Role and Responsibilities**
*Roles

**Communication Plan**
*Channels

**Additional Notes**
*Notes

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
