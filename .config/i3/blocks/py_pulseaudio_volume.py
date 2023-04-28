#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv
import subprocess
from os import environ

# To make this work:
# In /etc/pulse/default.pa:
#       change "load-module module-stream-restore"
#       to     "load-module module-stream-restore restore_device=false"


def get_sink_input_indices():
    raw_sink_inputs = str(subprocess.check_output(['pacmd',
                                                   'list-sink-inputs']),'utf-8').split('\n')
    clean_lines = [line.strip() for line in raw_sink_inputs]
    inputs = [line[7:] for line in clean_lines if line.startswith('index: ')]

    return inputs

def move_sink_input_to_sink(sink_input,new_sink):
    subprocess.call(['pacmd',
                     'move-sink-input',
                      str(sink_input),
                      str(new_sink)])

def get_raw_list_sinks():
    raw_list_sinks = str(subprocess.check_output(['pacmd',
                                              'list-sinks']), 'utf-8').split('\n')
    clean_lines = [line.strip() for line in raw_list_sinks]
    return clean_lines

def get_defualt_sink(raw_list_sinks):
    for line in raw_list_sinks:
        if 'index' in line and '*' in line:
            return int(line[-1])

def get_all_sinks(raw_list_sinks):
    retval = sorted([int(line[-1]) for line in raw_list_sinks if 'index' in line])
    return retval

def get_next_sink(default_sink, all_sinks):
    if default_sink in all_sinks:
        default_sink_index = all_sinks.index(default_sink)
    else:
        return all_sinks[0]
    if default_sink_index + 1 == len(all_sinks):
        return all_sinks[0]
    else:
        return all_sinks[default_sink_index + 1]

def set_new_sink(next_sink):
    output = str(subprocess.check_output(['pacmd',
                                          'set-default-sink',
                                          str(next_sink)]),'utf-8')
    if output == '':
        return True
    else:
        return False


def get_volume(raw_list_sinks):
    start_looking = False
    for line in raw_list_sinks:
        if 'index' in line and '*' in line:
            start_looking = True
        if start_looking and 'volume:' in line:
            return int([target.strip() for target in \
                    line.split('/') if '%' in target][0][:-1])

def get_mute(raw_list_sinks):
    pass


def get_display_sink(raw_list_sinks):
    default_sink = get_defualt_sink(raw_list_sinks)
    all_sinks = get_all_sinks(raw_list_sinks)
    num_of_sinks = len(all_sinks)
    nice_sink_list = list(range(num_of_sinks))
    display_sink = nice_sink_list[all_sinks.index(default_sink)]
    return display_sink

# def ensure_correct_sink(default_sink):
#     sink_input_indices = get_sink_input_indices()
#     for sink_input_index in sink_input_indices:
#         move_sink_input_to_sink(sink_input_index, default_sink)


def switch_sinks():
    raw_list_sinks = get_raw_list_sinks()
    default_sink = get_defualt_sink(raw_list_sinks)
    all_sinks = get_all_sinks(raw_list_sinks)
    new_sink = get_next_sink(default_sink,all_sinks)
    while True:
        success = set_new_sink(new_sink)
        if success:
            break
        else:
            invalid_sink_index = all_sinks.index(new_sink)
            all_sinks.pop(invalid_sink_index)
            new_sink =  get_next_sink(default_sink,all_sinks)
    sink_input_indices = get_sink_input_indices()
    for sink_input_index in sink_input_indices:
        move_sink_input_to_sink(sink_input_index, new_sink)


if __name__ == "__main__":
    try:
        (button) = int(environ.get('BLOCK_BUTTON'))
    except:
        button = None

    if button == 1:
        switch_sinks()
    elif button == 2:
        command = ['amixer',
                   '-q',
                   '-D',
                   'pulse',
                   'sset',
                   'Master',
                   'toggle']
        subprocess.call(command)
        volume = True
    elif button == 3:
        switch_sinks()
    elif button == 4:
        command = ['amixer',
                   '-q',
                   '-D',
                   'pulse',
                   'sset',
                   'Master',
                   '5%+']
        subprocess.call(command)
    elif button == 5:
        command = ['amixer',
                   '-q',
                   '-D',
                   'pulse',
                   'sset',
                   'Master',
                   '5%-']
        subprocess.call(command)


    raw_list_sinks = get_raw_list_sinks()
    volume = get_volume(raw_list_sinks)


    display_sink = get_display_sink(raw_list_sinks)


    #ensure_correct_sink(default_sink)
    if volume == 0:
        icon = ''
    elif volume < 50:
        icon = ''
    else:
        icon = ''
    print ('%s %3s%s %s' % (icon,
                            volume,
                            '%',
                            display_sink))
















