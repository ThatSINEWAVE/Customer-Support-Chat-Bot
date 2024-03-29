# Customer Support Chatbot Application

This repository hosts a customer support chatbot application that leverages the ChatterBot library for conversational AI and the Twilio API to engage with clients via messaging.

The application is built on Flask, a lightweight WSGI web application framework in Python, making it easy to extend and integrate with web services.

## Features

- AI-driven Conversations: Utilizes ChatterBot for intelligent, context-aware conversations with users.
- Twilio Integration: Employs the Twilio API to facilitate real-time messaging with clients, enhancing customer support.
- Flask Framework: Built with Flask, enabling easy web integration and scalability.

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

## Structure

- `app_v5.py`: The main application file containing Flask setup, route definitions, ChatterBot initialization, and Twilio API integration.
- `datasets/`: A directory containing various categories for training the chatbot, including:
- `feedback/`
- `general_information/`
- `order_delivery/`
- `placing_orders/`
- `returns/`

Each folder contains a corpus.yml file tailored for its specific category, aiding in the chatbot's learning process.

## Setup and Installation

- Clone the Repository: Start by cloning this repository to your local machine.

```
git clone <repository-url>
```

- Install Dependencies: Install the required Python packages using pip.

```
pip install flask chatterbot twilio
```

- Train the Chatbot: Use the provided datasets to train the chatbot for better accuracy and context understanding.

```
python -m chatterbot --train datasets/
```

- Run the Application: Start the Flask application.

```
flask run
```

## Usage

Once the application is running, it can interact with clients through the configured Twilio messaging service. The chatbot utilizes the trained datasets to respond to customer inquiries, feedback, and support requests effectively.

For detailed API usage and additional configurations, refer to the ChatterBot and Twilio documentation.

## Disclaimer

The training data (corpus) for this chatbot is primarily in Romanian, tailored for an online store context. 
The datasets are structured to enable the bot to handle a wide range of customer inquiries autonomously. 
In scenarios where the chatbot cannot provide sufficient assistance, it is designed to direct customers to real customer support agents for further help.


## Contribution

Contributions to enhance the chatbot's functionality, extend the datasets, or improve the application's efficiency are welcome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
