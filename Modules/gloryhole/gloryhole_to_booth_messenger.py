from BotState import Bot

HasHelpInfo = False

def handler(msg_pipe):
    msg = msg_pipe.get()

    if msg.code == "MSG" and msg.json["message"].startswith("/me"):
        character = msg.json["character"]
        forwarded_message = msg.json["message"]

        # Find the booth the character is a participant of
        for booth in Bot.booths:
            if character in booth.participants:
                # Create a map of participants to anonymous identifiers
                participant_ids = {participant: f"[color=green][Participant {index+1}][/color]" for index, participant in enumerate(booth.participants)}

                # Get the anonymous identifier for the sender
                sender_id = participant_ids.get(character, "Unknown Participant")

                # Update the message to use the anonymous identifier
                anonymized_message = forwarded_message.replace("/me", f"/me {sender_id}")

                # Forward the message to all occupants of the booth
                for occupant in booth.occupants:
                    if occupant != character:  # Don't echo the message back to the sender
                        Bot.send_out(Bot.Message(code="PRI", json={"message": anonymized_message, "recipient": occupant}))
                break

def predicate(msg):
    return msg.code == "MSG" and msg.json["message"].startswith("/me")