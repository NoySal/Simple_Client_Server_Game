# QuickMaths Game Server and Client

## Overview

**QuickMaths** is a multiplayer trivia game designed to test players' speed and accuracy in answering simple math-related questions. The project consists of two main components:

1. **Server**: Hosts the game, broadcasts offers to clients, manages connections, and facilitates the game between two players.
2. **Client**: Listens for server offers, connects to the server, participates in the game, and displays the results.

The game is designed for two players, where the first player to answer the question correctly wins the round. The project demonstrates fundamental concepts of socket programming, multithreading, and network communication in Python.

## Project Structure

- **`server.py`**: Contains the `Server` class that handles all server-side operations.
- **`client.py`**: Contains the `Client` class that handles all client-side operations.

### Server (`server.py`)

The server is responsible for:

- Broadcasting UDP offers to potential clients.
- Listening for TCP connections from clients.
- Managing the game logic, including:
  - Randomly selecting a trivia question.
  - Waiting for both players to connect.
  - Determining the winner based on the fastest correct answer.
  - Broadcasting the results to the players.
- Recycling the game state after each round to prepare for a new game.

### Client (`client.py`)

The client is responsible for:

- Listening for UDP broadcasts from the server.
- Parsing the server's offer and connecting via TCP.
- Participating in the game by:
  - Sending the team name to the server.
  - Receiving the trivia question.
  - Sending the answer as quickly as possible.
  - Receiving and displaying the game results.
- Reconnecting to the server for subsequent games.

## Requirements

- Python 3.x
- Standard Python libraries: `socket`, `struct`, `threading`, `time`

## Getting Started

### Running the Server

1. Open a terminal window.
2. Navigate to the directory containing `server.py`.
3. Run the server:

   ```bash
   python server.py
   
  The server will start listening for clients and broadcasting offers.
### Running the Client

1. Open a separate terminal window.
2. Navigate to the directory containing `client.py`.
3. Run the client:

   ```bash
   python client.py
   
The client will listen for server offers and connect when one is received.

## Game Flow

1. The server starts and waits for two clients to connect.
2. Clients connect to the server after receiving a broadcast offer.
3. The server sends a trivia question to both clients simultaneously.
4. The first client to send the correct answer is declared the winner.
5. The server broadcasts the game results to both clients.
6. The game restarts, and the server waits for new clients.

## Future Enhancements

- **Enhanced Question Bank**: Expand the trivia questions to cover more topics.
- **Game Statistics**: Implement a feature to track and display game statistics (e.g., win/loss records).
- **User Interface**: Develop a GUI for better user experience.
- **Cross-Network Play**: Improve the server and client code to support play across different networks, not just within the same local network.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the game, fix bugs, or add new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- This project was developed as part of a hackathon for the "Introduction to Networking" course.
