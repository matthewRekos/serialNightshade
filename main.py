import argparse
import utils
from attacker import Attacker


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = utils.add_attack_arguments(parser)
    args = parser.parse_args()
    attack_type = args.attack_type
    attack_kwargs = vars(args)
    if args.attack_output:
        attack_output = args.attack_output
    else:
        attack_output = "{}_added_attacks.{}".format(args.input.split(".")[0], args.format)

    if args.output:
        output = args.output
    else:
        output = "{}_with_attacks.{}".format(args.input.split(".")[0], args.format)

    attacker = Attacker(
        attack_type=attack_type,
        time=args.time,
        data=args.data,
        identifier=args.identifier,
        format=args.format,
        attack_chance=args.attack_chance
    )
    trace = attacker.read_trace(args.input)
    #add attacks to the trace
    attacker.add_attacks_to_trace(trace, **attack_kwargs)
    #Get modified trace
    trace_w_attacks = attacker.get_attack_trace()
    executed_attacks = attacker.get_executed_attacks()
    #Write trace w/ attacks and a key of all attacks executed in the set format
    attacker.output_data(output, trace_w_attacks)
    attacker.output_data(attack_output, executed_attacks)
