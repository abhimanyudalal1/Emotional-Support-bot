# Emotional Support Bot

This project is a web-based emotional support chatbot. It features a friendly user interface for interacting with an AI-powered bot designed to provide a supportive and empathetic conversational experience.

## Project Structure

The project is organized into two main parts:

-   `client/`: A React application that provides the user interface for the chatbot.
-   `server/`: A Flask (Python) backend that handles the chat logic and integrates with the OpenAI API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Node.js and npm (for the React client)
-   Python 3.x and pip (for the Flask server)
-   An OpenAI API key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Emotional-Support-bot.git
    cd Emotional-Support-bot
    ```

2.  **Set up the backend:**

    -   Navigate to the `server` directory:
        ```bash
        cd server
        ```
    -   Create a virtual environment:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```
    -   Create a `.env` file in the `server` directory and add your OpenAI API key:
        ```
        OPENAI_API_KEY='your-openai-api-key'
        ```

3.  **Set up the frontend:**

    -   Navigate to the `client` directory:
        ```bash
        cd ../client
        ```
    -   Install the required npm packages:
        ```bash
        npm install
        ```

### Running the Application

1.  **Start the backend server:**

    -   Make sure you are in the `server` directory with the virtual environment activated.
    -   Run the Flask application:
        ```bash
        gunicorn app:app
        ```
    -   The server will start on `http://127.0.0.1:8000`.

2.  **Start the frontend client:**

    -   Make sure you are in the `client` directory.
    -   Run the React application:
        ```bash
        npm start
        ```
    -   The client will start on `http://localhost:3000` and will open automatically in your browser.

## Built With

-   [React](https://reactjs.org/) - The web framework used for the client.
-   [Flask](https://flask.palletsprojects.com/) - The web framework used for the server.
-   [OpenAI API](https://openai.com/docs) - Used for the chatbot's intelligence.