import argparse
from wb import WildebeestApi
from wb import api
import os

def main():

    if 'WB_SERVER_URL' not in os.environ.keys():
        print("wild is required WB_SERVER_URL information to access Wildebeest Server.")
        print("please export it to os environment.")
        print("")
        return

    if 'WB_API_KEY' not in os.environ.keys():
        print("Only you can access public datasets without WB_API_KEY.");
        print("if you want to access your private datasets what registered in Wildebeest,");
        print("export your API Key to os environment.")
        print("")

    parser = argparse.ArgumentParser(
        description='Wildebeest Data Catalogue CommandLine Interface by N3NCLOUD',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='Wildebeest API ' + WildebeestApi.__version__)

    subparsers = parser.add_subparsers(title='commands',
                                       help=Help.wildebeest,
                                       dest='command')

    subparsers.required = False
    subparsers.choices = Help.wildebeest_choices
    # parse_organizations(subparsers)
    # parse_datasets(subparsers)
    # parse_resource(subparsers)
    define_command(subparsers)

    args = parser.parse_args()
    command_args = {}
    command_args.update(vars(args))

    if 'func' not in command_args.keys():
        print(" Wildbeest CommandLine Interface " + WildebeestApi.__version__)
        print("")
        print("   Homepage: http://www.n3ncloud.co.kr")
        print("   Github: https://github.com/n3nc/wild-cli")
        print("   Documents: http://d3.n3ncloud.co.kr/wildebeest/1.0")
        print("")
        print("   N3NCLOUD Co., Ltd.")
        print("")
        print(" Usage: wild -h ")
        print("")
        return

    del command_args['func']
    del command_args['command']
    error = False
    try:
        out = args.func(**command_args)
    except ValueError as e:
        print(e)
        out = None
        error = True
    except KeyboardInterrupt:
        print('User cancelled operation')
        out = None
    if out is not None:
        print(out, end='')

    # This is so that scripts that pick up on error codes can tell when there was a failure
    if error:
        exit(1)


def define_command(subparsers):
    commands = {
        'organizations': {
            'help': 'Commands related to Wildebeest organizations',
            'aliases': ['o'],
            'sub': {
                'list': {
                    'help': 'List available organizations',
                    'aliases': ['l'],
                    'func': api.organizations_list_cli
                },
                'show': {
                    'help': 'Show a detail of a specific organization',
                    'aliases': ['s'],
                    'func': api.organizations_show_cli,
                    'options': {
                        '?': {
                            'dest': 'organization_id',
                            'default': '',
                            'help': 'Organization Id'
                        }
                    }
                },
                'datasets': {
                    'help': 'Dataset list of a specific organization',
                    'aliases': ['d'],
                    'func': api.organizations_datasets_cli,
                    'options': {
                        '?': {
                            'dest': 'organization_id',
                            'default': '',
                            'help': 'Organization Id'
                        },
                        '-p': {
                            'dest': 'page',
                            'default': 1,
                            'required': False,
                            'help': 'Page number for results paging. Page size is 20 by default'
                        }
                    }
                }
            }
        },
        'datasets': {
            'help': 'Commands related to Wildebeest datasets',
            'aliases': ['d'],
            'sub': {
                'list': {
                    'help': 'List available datasets',
                    'aliases': ['l'],
                    'func': api.datasets_list_cli,
                    'options': {
                        '-p': {
                            'dest': 'page',
                            'default': 1,
                            'required': False,
                            'help': 'Page number for results paging. Page size is 20 by default'
                        }
                    }
                },
                'show': {
                    'help': 'Show a detail of a specific dataset',
                    'aliases': ['sh'],
                    'func': api.datasets_show_cli,
                    'options': {
                        '?': {
                            'dest': 'dataset_id',
                            'default': '',
                            'help': 'Organization Id'
                        }
                    }
                },
                'search': {
                    'help': 'Search datasets by query',
                    'aliases': ['s'],
                    'func': api.datasets_search_cli,
                    'options': {
                        '?': {
                            'dest': 'query',
                            'default': '',
                            'help': 'Organization Id'
                        },
                        '-p': {
                            'dest': 'page',
                            'default': 1,
                            'required': False,
                            'help': 'Page number for results paging. Page size is 20 by default'
                        }
                    }
                },
                'resources': {
                    'help': 'Resource List of a dataset',
                    'aliases': ['r'],
                    'func': api.datasets_resources_cli,
                    'options': {
                        '?': {
                            'dest': 'dataset',
                            'default': None,
                            'help': 'Organization Id'
                        }
                    }
                },
                'download': {
                    'help': 'Download all resource of a dataset',
                    'aliases': ['d'],
                    'func': api.datasets_download_cli,
                    'options': {
                        '?': {
                            'dest': 'dataset_id',
                            'default': '',
                            'help': 'Dataset Id'
                        }
                    }
                }
            }
        },
        'resource': {
            'help': 'Commands related to Wildebeest resources',
            'aliases': ['r'],
            'sub': {
                'show': {
                    'help': 'Show a detail of a specific dataset',
                    'aliases': ['s'],
                    'func': api.resource_show_cli,
                    'options': {
                        '?': {
                            'dest': 'resource_id',
                            'default': '',
                            'help': 'Resource Id'
                        }
                    }
                },
                'download': {
                    'help': 'Search datasets by query',
                    'aliases': ['d'],
                    'func': api.resource_download_cli,
                    'options': {
                        '?': {
                            'dest': 'resource_id',
                            'default': '',
                            'help': 'Resource Id'
                        }
                    }
                }
            }
        }
    }
    parse_commands(subparsers, commands)


def parse_commands(subparsers, commands):
    for cmd, desc in commands.items():
        mainset = subparsers.add_parser(
            cmd,
            formatter_class=argparse.RawTextHelpFormatter,
            help=desc['help'],
            aliases=desc.get('aliases', []))

        if 'sub' in desc.keys():
            subset = mainset.add_subparsers(title='commands', dest='command')
            subset.required = True
            keywords = []
            keywords.extend(desc['sub'].keys())
            for sub_name, sub_desc in desc['sub'].items():
                aliases = sub_desc.get('aliases', [])
                keywords.extend(aliases)
                sub_cmd = subset.add_parser(
                    sub_name,
                    aliases=aliases,
                    formatter_class=argparse.RawTextHelpFormatter,
                    help=sub_desc.get('help', ''))
                sub_cmd.set_defaults(func=sub_desc['func'])
                if 'options' in sub_desc.keys():
                    sub_options = sub_cmd._action_groups.pop()
                    for opt_name, opt_desc in sub_desc['options'].items():
                        if opt_name == '?':
                            sub_options.add_argument(
                                dest=opt_desc['dest'],
                                nargs='?',
                                default=opt_desc.get('default'),
                                help=opt_desc.get('help', ''))
                        else:
                            sub_options.add_argument(
                                opt_name,
                                '--'+opt_desc['dest'],
                                dest=opt_desc['dest'],
                                default=opt_desc.get('default'),
                                required=opt_desc.get('required', False),
                                help=opt_desc.get('help', ''))

            subset.choices = keywords
