import argparse
import time
import sys
import os
import traceback
import logging
from logging.handlers import RotatingFileHandler
from libs.utorrentapi import UTorrentAPI

parser = argparse.ArgumentParser()
parser.add_argument("--server", "-s", help="[required] uTorrent Web UI URL")
parser.add_argument("--username", "-u", help="[required] Web login username, default: admin", default='admin')
parser.add_argument("--password", "-p", help="[required] Web login password")
parser.add_argument("--days", "-d", help="Allow number of seed days before delete torrent, default: 7", default='7')
parser.add_argument("--test", "-t", help="Test mode, default: False", default='0')
args = parser.parse_args()

base_dir = os.path.dirname(os.path.realpath(__file__))

if getattr(sys, 'frozen', False):
    from sys import exit

    base_dir = os.path.dirname(sys.executable)


def log_setup(level: int = logging.DEBUG, log_time_zone_local: bool = True, log_file_name: str = None):
    if not log_file_name:
        log_file_name = os.path.basename(__file__).split('.py')[0] + '.log'
    if not log_file_name.endswith('.log'):
        log_file_name += ".log"
    handler = RotatingFileHandler(os.path.join(base_dir, log_file_name),
                                  maxBytes=307200, backupCount=3, encoding='utf-8')  # 300KB
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    if not log_time_zone_local:
        formatter.converter = time.gmtime  # if you want UTC time
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)


def test(server_url: str, username: str, password: str, seed_days: int = 0):
    """
    This is test
    """
    apiclient = UTorrentAPI(server_url, username, password)
    today_time = time.time()

    if apiclient is not None:
        torrents = apiclient.get_list()
        index = 0
        for torrent in torrents['torrents']:
            gap = 0
            if torrent[24]:
                gap = int((today_time - torrent[24]) / 3600 / 24)
            if seed_days:
                if gap > seed_days:
                    name = f"test -- remove: [{index}] {torrent[2]} - ID: {torrent[0]} -- status: {torrent[21]} -- cld: {torrent[24]} (gap: {gap} days)"
                    print(name)
            else:
                name = f"[{index}] {torrent[2]} - ID: {torrent[0]} -- status: {torrent[21]} -- cld: {torrent[24]} (gap: {gap} days)"
                print(name)
            index += 1


def remove_completed_torrent(server_url: str, username: str, password: str, seed_days: int = 7):
    """
    Access Web UI to check key order
    """
    api_client = UTorrentAPI(server_url, username, password)
    today_time = time.time()

    if api_client is not None:
        torrents = api_client.get_list()
        for torrent in torrents['torrents']:
            if torrent[24]:
                gap = int((today_time - torrent[24]) / 3600 / 24)
                if gap > seed_days:
                    api_client.remove(torrent[0])


if __name__ == "__main__":
    start_time = time.time()
    test_mode = args.test in ('1', 'True', 'true', 'yes')
    log_setup(logging.INFO)
    logging.info(f"start, test_mode: {'yes' if test_mode else 'no'}")
    if not args.server or not args.username or not args.password:
        print("Missing arguments, run -h for help")
        logging.info('missing arguments, exit!')
        exit()
    if test_mode:
        test(args.server, args.username, args.password, int(args.days))
    else:
        logging.info(f"target url: {args.server}, username: {args.username}, max seed days: {args.days}")
        try:
            remove_completed_torrent(args.server, args.username, args.password, int(args.days))
        except Exception:
            logging.error(f"execute remove_completed_torrent error, traceback:\n{traceback.format_exc()}")
    logging.info(f"end, duration: {(time.time() - start_time):.2f} seconds")
