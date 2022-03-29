from random import randint
import sys
import utils


class Attacker:
    def __init__(
        self, time, data, identifier, attack_type, format, attack_chance
    ):
        pass

        add_attack_lookup = {
            "spoofing": self.add_spoofing_attack,
            "corruption": self.add_corruption_attack,
            "flooding": self.add_flooding_attack,
            "silence": self.add_silence_attack,
            "manipulate": self.add_manipulation_attack,
        }
        self.add_attack = add_attack_lookup[attack_type]
        self.attack_type = attack_type
        formatting_key = {"json": (utils.write_json, utils.read_json), "csv": (utils.write_csv, utils.read_csv)}
        self.output_data, self.read_trace = formatting_key[format]

        self.time_var = time
        self.data_var = data
        self.id_var = identifier
        self.total_attack_time = 0
        self.attack_chance = attack_chance
        self.executed_attacks = []
        self.message_queue = []
        self.format = format
        # self.time_interval_low = time_interval_low
        # self.time_interval_high = time_interval_high

    def __str__(self):
        return "{} Attacker - Executing one attack per every {} messages\nOutput Format : {}".format(
            self.attack_type, self.attack_chance, self.format
        )

    def add_attacks_to_trace(self, trace, **kwargs):
        for message in trace:
            message[self.time_var] += self.total_attack_time
            # Determine if random attack trigger:
            if randint(1, self.attack_chance) == 1:
                self.add_attack(message, **kwargs)
            else:
                message["attack"] = False
                self.message_queue.append(message)

    def add_spoofing_attack(self, message, **kwargs):
        atk_msg = dict(message)
        try:
            current_time = message[self.time_var]
            new_time = current_time + randint(
                kwargs["spoofing_interval_lowerbound"], kwargs["spoofing_interval_upperbound"]
            )
            atk_msg[self.time_var] = new_time
            atk_msg["attack"] = True
        except KeyError:
            print("Time field not found, supply --time argument")
            sys.exit()
        self.message_queue.append(message)
        self.message_queue.append(atk_msg)
        self.executed_attacks.append(dict(atk_msg))

    def randomize_message_data(self, data):
        if isinstance(data, list):
            pass
            number_entries = len(data)
            for x in range(0, number_entries):
                data[x] = randint(0, self.data_max)
        elif isinstance(data, int):
            data = randint(0, (self.data_max * self.data_len))
        elif isinstance(data, str):
            data = hex(randint(0, (self.data_max * self.data_len)))
        return data

    def add_corruption_attack(self, message, **kwargs):
        atk_msg = dict(message)
        try:
            atk_msg[self.data_var] = self.randomize_message_data(message[self.data_var])
        except KeyError:
            print("Data field not found, supply --data argument")
            sys.exit()
        atk_msg["attack"] = True
        self.message_queue.append(atk_msg)
        self.executed_attacks.append(atk_msg)

    def add_flooding_attack(self, message, **kwargs):
        random_number_of_attacks = randint(100,1000)
        for x in range(0, random_number_of_attacks):
            atk_msg = dict(message)
            random_len = randint(kwargs["flooding_min_length"], kwargs["flooding_min_length"] + 100)
            new_time = prev_time + random_len
            self.total_attack_time += random_len
            atk_msg["ticks"] = new_time
            atk_msg["attack"] = True
            self.message_queue.append(atk_msg)
            self.executed_attacks.append(dict(atk_msg))
            prev_time = new_time



    def add_cancel_attack(self, message, **kwargs):
        #Add to list of attacks without adding back into the message queue
        #Alerting on this would likely be from an anomaly noticed on the next occurence of the message
        #This makes grading less trivial, since the lack of message is the attack. It is recommended not to use message["attack"] to grade cancel attacks
        self.executed_attacks.append(message)



    def add_silence_attack(self, message, **kwargs):
        #add half a second to 10 seconds of dead bus time
        self.total_attack_time += randint(500000, 10000000)
        #append the attack triggering message, as its the last message before a long period of silence
        message["attack"] = True
        self.executed_attacks.append(message)
        self.message_queue.append(message)

    def add_manipulation_attack(self, message, **kwargs):
        target = kwargs["manipulation_field"]
        try:
            atk_message = dict(message)
            atk_message["attack"] = True
            atk_message[target] ^= 1 << randint(0, atk_message[target].bit_length()-1)
            self.message_queue.append(atk_message)
            self.executed_attacks.append(atk_message)
        except KeyError:
            print("supply manipulation field arg to flip a bit in a particular field")
            sys.exit()

    def get_attack_trace(self):
        return self.message_queue

    def get_executed_attacks(self):
        return self.executed_attacks

    def get_meta_information(self):
        return {"attack_type": self.attack_type}
