import argparse
import time
from libs.utorrentapi import UTorrentAPI

parser = argparse.ArgumentParser()
parser.add_argument("--server", "-s", help="[required] uTorrent Web UI URL")
parser.add_argument("--username", "-u", help="[required] Web login username, default: admin", default='admin')
parser.add_argument("--password", "-p", help="[required] Web login password")
parser.add_argument("--days", "-d", help="Allow number of seed days before delete torrent, default: 7", default='7')
parser.add_argument("--test", "-t", help="Test mode, default: False", default='0')
args = parser.parse_args()

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
    apiclient = UTorrentAPI(server_url, username, password)
    today_time = time.time()

    if apiclient is not None:
        torrents = apiclient.get_list()
        for torrent in torrents['torrents']:
            if torrent[24]:
                gap = int((today_time - torrent[24]) / 3600 / 24)
                if gap > seed_days:
                    apiclient.remove(torrent[0])


if __name__ == "__main__":
    test_mode = args.test in ('1', 'True', 'true', 'yes')
    if not args.server or not args.username or not args.password:
        print("Missing arguments, run -h for help")
        exit()
    if test_mode:
        test(args.server, args.username, args.password, int(args.days))
    else:
        remove_completed_torrent(args.server, args.username, args.password, int(args.days))