import argparse
import glob

import time

from configurator.configurator import *

start = time.time()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kapacitor foo')
    parser.add_argument('-gsa', help='Instance path')
    parser.add_argument('-gma', help='Instance path')
    args = parser.parse_args()

    if args.gsa:
        if os.path.exists(args.gsa):
            alert_conf_files_path = glob.glob(os.path.join(args.gsa, "*.yaml"))
            for file in alert_conf_files_path:
                if file.endswith("email_channel.yaml"):
                    continue
                else:
                    AlertConf(file).generate_alerts_conf()
    if args.gma:
        if os.path.exists(args.gma):
            alert_conf_dir_path = args.gma
            for entry in os.scandir(alert_conf_dir_path):
                if entry.is_dir():
                    for file in entry.path:
                        alert_conf_files_path = glob.glob(os.path.join(entry.path, "*.yaml"))
                        for f2 in alert_conf_files_path:
                            if f2.endswith("email_channel.yaml"):
                                continue
                            else:
                                AlertConf(f2).generate_alerts_conf()

end = time.time()
print(end - start)