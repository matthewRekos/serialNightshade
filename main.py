import argparse
import utils
from attacker import Attacker




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = utils.add_attack_arguments(parser)
    args = parser.parse_args()
    attack_type = args.attack_type
    if args.attack_output:
        attack_output = args.attack_output
    else:
        attack_output = "{}_attack.json"

    # open trace
    # initalize attacker
    # if args.

    attacker = Attacker(
        attack_type=attack_type,
        time=args.time,
        data=args.data,
        identifier=args.identifier,
        output_format=args.output_format,
        attack_chance=args.attack_chance
    )
    trace = attacker.read_trace(args.input)
    #add attacks to the trace
    attacker.add_attacks_to_trace(trace)
    #Get modified trace
    trace_w_attacks = attacker.get_attack_trace()
    executed_attacks = attacker.get_executed_attacks()
    #Write trace w/ attacks and a key of all attacks executed in the set format
    attacker.output_data(args.output, trace_w_attacks)
    attacker.output_data(args.attack_output, executed_attacks)
