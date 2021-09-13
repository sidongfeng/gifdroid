import argparse
import glob
import os
import json

from location import keyframe_location
from mapping import gui_mapping
from trace import find_execution_trace

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='GIFdroid: Automated Replay of Visual Bug Reports for Android Apps')
    parser.add_argument('--video', dest='video',
                        help='bug recording',
                        default=None, type=str)
    parser.add_argument('--utg', dest='utg',
                        help='GUI transition graph in json format',
                        default=None, type=str)
    parser.add_argument('--artifact', dest='artifact',
                        help='GUI screenshots in UTG',
                        default=None, type=str)
    parser.add_argument('--out', dest='out',
                        help='output of the execution trace',
                        default='execution.json', type=str)
    args = parser.parse_args()
    return args

def read_graph_with_action(utg):
    f = open(utg, 'r')
    parsed_json = json.loads(f.read())
    f.close()
    vertices = 0
    graph = []
    for event in parsed_json['events']:
        s = int(event['sourceScreenId'])
        d = int(event['destinationScreenId'])
        if 'target' in event.keys():
            action_type = event['target']['type']
            action_id = event['target']['targetDetails']
        else:
            action_type = 'LAUNCH'
            action_id = 'app'
        graph.append([s, d, action_type, action_id])
    
    return graph

def store_trace(utg, traces, out):
    graph = read_graph_with_action(utg)
    output_json = {'video': args.video, 
                    'utg': args.utg,
                    'artifact': args.artifact,
                    'replay_traces':[]}

    for trace in traces:
        trace_seq = {'trace': []}
        for i in range(len(trace)-1):
            # detect action
            for g in graph:
                if g[0] == trace[i] and g[1] == trace[i+1]:
                    action = g
                    break
            
            seq = {
                "sourceScreenId": trace[i],
                "destinationScreenId": trace[i+1],
                "action": {
                    "type": action[2],
                    "targetDetails": action[3] 
                }
            }
            trace_seq['trace'].append(seq)
        
        output_json['replay_traces'].append(trace_seq)

    with open(out, 'w') as fp:
        json.dump(output_json, fp, indent=4)

def main(video, screenshots, utg):
    keyframe_sequence, keyframe_index = keyframe_location(video)
    print('-'*30)
    print('Keyframe Index:')
    print(keyframe_index)
    print('-'*30)
    index_sequence = gui_mapping(screenshots, keyframe_sequence)
    print('Index Sequence')
    print(index_sequence)
    print('-'*30)
    traces = find_execution_trace(utg, index_sequence)
    print('Execution Trace')
    print(traces)
    print('-'*30)
    store_trace(utg, traces, args.out)
    print('Execution Trace stored in {}'.format(args.out))
    return index_sequence, traces

if __name__ == "__main__":
    args = parse_args()

    print('Called with args:')
    print(args)

    if args.video is None or args.utg is None or args.artifact is None:
        print("Please insert correct input. For help information, -h")
        exit()

    main(args.video, args.artifact, args.utg)
