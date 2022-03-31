# Attack Insertion Tool

This tool is designed to add attacks randomly into a serial data bus dataset. It then outputs a copy of that dataset with the attacks, and a truth file with any attacks added so you can test your IDS.

## Installation
Simply run the setup file to package this tool as 'nightshade'
```bash
python3 setup.py install
```


## Usage
```bash
usage: nightshade [-h] [--attack-chance ATTACK_CHANCE] [--output OUTPUT]
                  [--format FORMAT] --input INPUT
                  [--attack-output ATTACK_OUTPUT] --attack-type ATTACK_TYPE
                  [--time TIME] [--data DATA] [--identifier IDENTIFIER]
                  [--flooding-min-length FLOODING_MIN_LENGTH]
                  [--spoofing-interval-lowerbound SPOOFING_INTERVAL_LOWERBOUND]
                  [--spoofing-interval-upperbound SPOOFING_INTERVAL_UPPERBOUND]
                  [--manipulation-field MANIPULATION_FIELD]
```
For an example of adding a spoofing attack to $(TRACE/PATH) with time since epoch stored as a key labeled 'time'
```bash
nightshade --input $(TRACE/PATH) --attack-type spoofing -t time
```



## Attack Types:
### Spoofing
- We define spoofing as an attacker pretending to be someone else (Lying about their source address)
- On an attack trigger it copies the message, increases the time, and inserts it later into the trace 
- Requirements : --time argument must provide key for time since epoch field
- Extra Features : --spoofing-interval-<lowerbound/upperbound> provide lower and upper bounds for how far into the trace the spoofed attack is. Larger intervals are typically better for testing the resiliency of systems.
### Corruption
- We define corruption as a malicious data field sent by a device
- On an attack the triggering message has its data field replaced with a random data field 
- Requirements : --data argument must provide key for data field
### Manipulation
- We define manipulation as a bit being changed in a message, where the message is still valid on the bus
- Notably some protocols (CAN) drop messages when bits are flipped, so check protocol behavior before using this attack type
### Flooding
- Flooding is the repetition of messages on the bus, usually such that no other messages can be sent
- On an attack trigger the message is copied a random number of times and all messages in the trace have their timestamp increased to reflect the large number of new messages
- Requirements : --time argument must provide key for time since epoch field
- Extra Features : --flooding-min-length should be set to the minimum amount of time in microseconds between messages (including the time to transmit the message)
### Cancelling
- Cancelling is the removal of a message from the bus
- On an attack trigger the message is deleted from the trace
### Silencing
- Silencing is extended dead bus time
- On an attack trigger the timestamps of all future messages are increased by a random period of attack time to simulate silence on the bus
- Requirements : --time argument must provide key for time since epoch field

# Extensions
## Attack Extensions
To extend this tool with a new attack simply add a function inside the attacker class ensuring to:
- add it to `add_attack_lookup` in the Attacker class `__init__`
- ensure `self.message_queue` and `self.executed_attacks` include any attack triggers

## Formatting Extensions
Currently this tool supports csv and json formats for input and output. To extend simply
- add the format and corresponding read/write functions to `formatting_key` in the Attacker class `__init__`

## Future Attack Improvements
- Adding compatibility with a popular signal processing tool would allow more realistic manipulation attack detection, and support for voltage based intrusion detection systems
- `smart-mode` to add attacks based on observed patterns in the dataset, rather than randomly. 
  - finding messages with aperiodic timing intervals
  - independent data variables
  - intelligent flooding patterns
