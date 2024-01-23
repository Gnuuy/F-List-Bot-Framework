from BotState import Bot
import json
import os

HasHelpInfo = True
command_name = "!feedback"
command_description = "Send feedback to the bot developer."


def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.json["message"].startswith("!feedback"):
        # Extract the feedback text
        feedback_message = msg.json["message"][9:].strip()
        # The user who gave the feedback
        character = msg.json["character"]
        feedback_data = {"character": character, "feedback": feedback_message}

        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Path to the JSON file where feedback will be stored
        feedback_file = os.path.join(dir_path, "feedback.json")

        # Load existing feedbacks and append the new one
        if os.path.exists(feedback_file):
            with open(feedback_file, "r") as file:
                try:
                    feedbacks = json.load(file)
                except json.JSONDecodeError:
                    feedbacks = []
        else:
            feedbacks = []

        feedbacks.append(feedback_data)

        with open(feedback_file, "w") as file:
            json.dump(feedbacks, file, indent=4)

        # Send a thank-you response to the same channel from which the feedback was received
        response_message = "Thank you for your feedback! We greatly appreciate it."
        if msg.code == "PRI":
            Bot.send_out(Bot.Message(code="PRI", json={"message": response_message, "recipient": character}))

        elif msg.code == "MSG":
            Bot.send_out(Bot.Message(code="MSG", json={"message": response_message, "channel": msg.json["channel"]}))


def predicate(msg):
    return (msg.code == "MSG" or msg.code == "PRI") and msg.json["message"].startswith("!feedback")