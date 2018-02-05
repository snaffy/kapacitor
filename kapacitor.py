import argparse
import glob
import shutil

import time

from configurator.configurator import *


from projectconfiguration import ProjectConf
from taskmngmt.kapacitormanager import KapacitorTemplateCreator, KapacitorTaskCreator, KapacitorTaskManager

start = time.time()

def remove_old_config(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def generate_alerts_conf(path):
    alert_conf_files_path = glob.glob(os.path.join(path, "*.yaml"))
    for file in alert_conf_files_path:
        if file.endswith("email_channel.yaml"):
            continue
        else:
            AlertConf(file).generate_alerts_conf()

if __name__ == '__main__':
    parent_parser = argparse.ArgumentParser(add_help=True)

    group1 = parent_parser.add_argument_group('Group1', 'Commands generating configuration based on .yaml files')
    group1.add_argument('--gc', help='Path to the directory containing the microwatcher configuration files for a specific ec2 instance', type=str)
    group1.add_argument('--gmc', help='Generates a microwatcher configuration files for all ec2 instances. '
                                      'The argument is the path to the main directory with all ec2 instance, e.g. /usr/local/ki/rva/kapacitor/ ', type=str)

    group2 = parent_parser.add_argument_group('Group2', 'Commands that add alerts based on the generated configuration from Group1')
    group2.set_defaults(c=ProjectConf.get_default_template_dir_path())
    group2.add_argument('--ctsk', help='Adds new tasks (alerts) to the kapacitor. '
                                       'The argument is the path to the ec2 instance directory containing the generated configuration', type=str)

    group3 = parent_parser.add_argument_group('Group3', 'Commands for temporarily disabling alerts')
    group3.add_argument('--mtsk', help='ID / name of the alert to be disabled, acceptable regular expressions e.g. --mtsk staging-staging-gts.utilimarc.com-*')
    group3.add_argument('-t', help='The time by which microwatcher should be disabled, default - 60 minutes', type=int)
    group3.add_argument('-u', help='Time unit, default - minutes', choices=['minutes', 'hours', 'days', 'weeks'], type=str)
    group3.set_defaults(t=60, u='minutes')

    group4 = parent_parser.add_argument_group('Group4', 'Commands that add templates to kapacitor')
    group4.add_argument('--ctmp', help='Adds new template to the kapacitor. '
                                       'The default template location is /usr/local/ki/monitoring/kapacitor/templates',
                        action='store_true')
    group4.add_argument('-c', help='[Optional parameter] Path to directory with templates', type=str)

    # args = parent_parser.parse_args(['--gc=C:\\Projects\\monitoring_root\\monitoring_root\\monitoring_client\\rva\\kapacitor\\vehicle-event-router-staging-yaml-concept'])
    #args = parent_parser.parse_args(['--gmc=C:\\Projects\\monitoring_root\\monitoring_client\\rva\\kapacitor\\test'])
    #args = parent_parser.parse_args(['--mtsk=test-task', '-t=1'])
    args = parent_parser.parse_args(['--ctsk=C:\\Projects\\monitoring_root\\monitoring_root\\monitoring_client\\rva\\kapacitor\\vehicle-event-router-staging-yaml-concept'])
    #args = parent_parser.parse_args(['--ctsk=C:\\Projects\\monitoring_root\\monitoring_client\\rva\kapacitor\\vehicle-event-router-staging-yaml-concept-flat-structure'])
    # args = parent_parser.parse_args(['--ctsk=asfasf'])
    # args = parent_parser.parse_args()
    parent_parser.print_help()
    if args.gc:
        print(args.gc)
        if os.path.exists(args.gc):
            remove_old_config(os.path.join(args.gc, 'output'))
            generate_alerts_conf(args.gc)
    if args.gmc:
        print(args.gmc)
        if os.path.exists(args.gmc):
            alert_conf_dir_path = args.gmc
            for entry in os.listdir(alert_conf_dir_path):
                if entry == 'email_channel.yaml':
                    continue
                single_instance = os.path.join(alert_conf_dir_path, entry)
                remove_old_config(os.path.join(single_instance, 'output'))
                generate_alerts_conf(single_instance)
    if args.ctmp:
        KapacitorTemplateCreator(args.c).create()
    if args.ctsk:
        if os.path.exists(args.ctsk):
            KapacitorTaskCreator(args.ctsk).create()
    if args.mtsk:
        ktm = KapacitorTaskManager(args.mtsk, args.t, args.u)
        ktm.disable()
        ktm.enable()

end = time.time()
print("Execution time: ")
print(end - start)