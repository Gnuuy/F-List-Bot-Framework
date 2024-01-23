#Singleton for sharing data between modules.
class BotSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BotSingleton, cls).__new__(cls, *args, **kwargs)
            # Add shared data as needed
            cls.currentTime = 1
            cls.room = ""
            cls.boothsOcccupants = []
            cls.moderators = ["Moo", "Keyah", "Kemonomimi GM", "Captain Eberswalde", "Mayhem Maid", 
              "Fetch me their souls", "Cassandra Star", "Fellation", "Prolific", 
              "Leuna Madra", "Clari", "Brenda", "Petulant", "Kemonomimi Hub", 
              "Sarathiel", "Nine Lives", "Red Shadowscale", "Ellis Ailven", 
              "Red Eyed Bunny", "ElpheIt Valentine"]
        return cls._instance