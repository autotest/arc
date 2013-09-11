#!/usr/bin/python

import os
import sys
import importlib

def get_module(name):
    '''
    Loads the given module and if found, returns it
    '''
    module_name = 'arc.cli.args.%s' % name
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        return None

def get_arguments(module):
    return getattr(module, 'ARGUMENTS', None)

def get_action_arguments(module):
    return getattr(module, 'ACTION_ARGUMENTS', None)

def args_to_rest(module, header, args):
    result = []
    char = '~'

    result.append(header)
    result.append(len(header) * char)

    for entry in args:
        short_long_opts = entry[0]
        if len(short_long_opts) > 1:
            result.append("%s, %s" % entry[0])
        else:
            result.append("%s" % entry[0])
        result.append("   %s" % entry[1].get("help", ""))
        result.append("")
    result.append("")
    return result

def module_options_to_rest(module):
    result = []

    actions = get_action_arguments(module)
    arguments = get_arguments(module)

    if (actions is None) and (arguments is None):
        return ''

    if actions is not None:
        result += args_to_rest(module, 'ACTION ARGUMENTS', actions)

    if arguments is not None:
        result += args_to_rest(module, 'OPTIONAL ARGUMENTS', arguments)

    return '\n'.join(result)

def module_name_to_rest_build_file(name):
    # FIXME: lookup this __file__ location
    OUTPUT_DIR = 'build'
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    output_file_name = 'cli_args_%s.txt' % name
    output_file_path = os.path.join('build',
                                    output_file_name)

    module = get_module(name)
    if module is not None:
        output = open(output_file_path, 'w')
        output.write(module_options_to_rest(module))
        output.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <module_name>" % sys.argv[0])
        sys.exit(-1)

    module = get_module(sys.argv[1])
    if module is None:
        print("Module %s not found" % sys.argv[1])
        sys.exit(-1)

    module_name_to_rest_build_file(sys.argv[1])
