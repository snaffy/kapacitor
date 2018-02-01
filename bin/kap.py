import argparse
import glob
import os
import sys

from bin.configurator.configurator import AlertConf

sys.path.append("D:\Development\Python\kapacitor\test")
sys.path.append("D:\Development\Python\kapacitor\configurator")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kapacitor foo')
    parser.add_argument('-ga', help='Instance path')
    args = parser.parse_args()
    if args.ga:
        if os.path.exists(args.ga):
            # for file in glob.glob(os.path.join(args.ga, "*.yaml")):
                AlertConf("C:\\Projects\\monitoring_root\\monitoring_root\\monitoring_client\\rva\\kapacitor\\vehicle-event-router-staging-yaml-concept\\dbi_value.yaml").generate_alerts_conf()