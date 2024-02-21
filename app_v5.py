from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from twilio.rest import Client
import os
import subprocess


# Your send_telegram_message and custom_print functions
def send_telegram_message(log_message):
    try:
        command = [
            'curl',
            '-X', 'POST',
            'https://api.telegram.org/BOT_ID/sendMessage',
            '-d', f'chat_id=CHAT_ID&text={log_message}'
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        with open('error_log.txt', 'a') as f:
            f.write(str(e) + '\n')


def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = " ".join(map(str, args))
    send_telegram_message(message)


original_print = print
print = custom_print

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials
account_sid = 'SID'
auth_token = 'TOKEN'
client = Client(account_sid, auth_token)

# Initialize and train multiple chatbot models
tasks = ["placing_orders", "general_information", "order_delivery", "returns", "feedback"]
bots = {}
for task in tasks:
    print(f"Initializing and training bot for: {task}")
    bot = ChatBot(task, storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  database_uri=f'sqlite:///{task}.sqlite3?check_same_thread=False')
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(os.path.join("D:\\Code\\WhatsApp BOT\\Multi-Model Bot\\datasets", task, "corpus.yml"))
    bots[task] = bot

user_states = {}


def get_bot_response(incoming_msg, user_state):
    print(f"Getting bot response for state: {user_state} with message: {incoming_msg}")
    if user_state not in bots:
        return "Scuze, nu pot sa va ajut cu aceasta optiune, aveti alta intrebare?"

    response = bots[user_state].get_response(incoming_msg).text
    if response.strip():
        return response + "\nPentru a va intoarce la meniul principal tastati 9"
    else:
        return ("Scuze, nu pot sa va ajut cu aceasta problema, aveti alta intrebare? "
                "\nPentru a va intoarce la meniul principal tastati 9")


@app.route('/webhook', methods=['POST'])
def webhook():
    from_number = request.values.get('From')
    incoming_msg = request.values.get('Body', '').strip()

    print(f"Received message: {incoming_msg} from number: {from_number}")

    if from_number not in user_states:
        print(f"Initializing state for number: {from_number}")
        user_states[from_number] = None

    if incoming_msg == "9":
        user_states[from_number] = None
        response_msg = """Buna ziua, cu ce va putem ajuta astazi?
1. Plasarea unei comenzi
2. Informatii generale
3. Livrarea comenzilor
4. Returnari
5. Feedback
( Tastati numarul optiunii dorite )"""
        print(f"User selected to return to main menu.")
    elif user_states[from_number] is None:
        if incoming_msg in ["1", "2", "3", "4", "5"]:
            user_states[from_number] = tasks[int(incoming_msg) - 1]
            response_msg = ("Buna ziua, cu ce va pot ajuta in legatura cu " + user_states[from_number].replace("_", " ")
                            + "? \nPentru a va intoarce la meniul principal tastati 9")
            print(f"User selected option: {incoming_msg}, setting state to: {user_states[from_number]}")
        else:
            response_msg = """Buna ziua, cu ce va putem ajuta astazi?
1. Plasarea unei comenzi
2. Informatii generale
3. Livrarea comenzilor
4. Returnari
5. Feedback
( Tastati numarul optiunii dorite )"""
            print(f"Sending initial greeting message to user.")
    else:
        response_msg = get_bot_response(incoming_msg, user_states[from_number])

    response = MessagingResponse()
    response.message(response_msg)
    print(f"Sending response: {response_msg}")
    return str(response)


if __name__ == '__main__':
    print("Starting the Flask application...")
    app.run(debug=True)
