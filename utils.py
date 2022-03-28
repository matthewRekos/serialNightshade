import argparse
import json
from json import JSONDecodeError
import csv

import ast

def add_attack_arguments(arg_parser):
    arg_parser.add_argument(
        "--attack-chance","-ac",
        help="Attack will occur once per every X messages, where X is this arg",
        default=100,
        type=int,
    )
    arg_parser.add_argument(
        "--output", "-o",
        help="Path for output of trace with attacks inserted",
        type=str,
        default="trace_with_attacks.json"
    )
    arg_parser.add_argument(
        "--format", "-f",
        help="Format for input and output data [supports: csv,json]",
        default="json",
        type=str,
    )
    arg_parser.add_argument(
        "--input", "-i",
        help="Path for trace to add attacks to",
        type=str,
        required=True,
    )
    arg_parser.add_argument(
        "--attack-output", "-ao",
        help="Path for output of what attacks were added to a trace",
        type=str,
    )
    arg_parser.add_argument(
        "--attack-type", "-at",
        help="chosen attacks to add to dataset. supported: [spoofing, corruption, manipulation, canceling]",
        type=str,
        required=True,
    )
    arg_parser.add_argument(
        "--time", "-t",
        help="key for the field containing time since epoch",
        type=str,
        default="time"
    )
    arg_parser.add_argument(
        "--data", "-d",
        help="key for the field containing message data supports : hex-string, list of bytes, int",
        type=str,
        default="data"
    )
    arg_parser.add_argument(
        "--identifier", "-id",
        help="key for the field containing message the unique ID for the message",
        type=str,
        default="id"
    )
    arg_parser.add_argument(
        "--flooding-min-length", "-fml",
        help="[flooding] informs the minimum time (microseconds) between messages such that flooding data is realistic",
        type=int,
        default=500
    )
    arg_parser.add_argument(
        "--spoofing-interval-lowerbound", "-silb",
        help="[spoofing] informs the lowerbound of when spoofed messages appear",
        type=int,
        default=500
    )
    arg_parser.add_argument(
        "--spoofing-interval-upperbound", "-siub",
        help="[spoofing] informs the upperbound of when spoofed messages appear",
        type=int,
        default=50000
    )
    arg_parser.add_argument(
        "--manipulation-field", "-mf",
        help="[manipulation] informs what field to flip a bit in, defaults to 'id'",
        type=str,
        default="id"
    )
    return arg_parser

def open_trace(trace_path):
    try:
        with open(trace_path, "r") as f:
            trace_data = json.load(f)
    except FileNotFoundError:
        pass
    except JSONDecodeError:
        trace_data = []
        for item in f.readlines():
            trace_data.append(ast.literal_eval(item))

    return trace_data

def read_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    return reader

def write_csv(path, data):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)


def read_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def write_json(path, data):
    with open(path, "w") as fw:
        json.dump(data, fw)


