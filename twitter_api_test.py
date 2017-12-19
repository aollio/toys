#!/usr/bin/env python3

import twitter

CONSUMER_KEY = 'RYXVBQBS4nFHheMUobgCr9cQ5'
CONSUMER_SECRET = 'f9VvJeLFgCKJVz04z38X9LO2cY3znbq5RZ3gj4WyDavY36Bn8q'
ACCESS_TOKEN_KEY = '798551903533572096-dTgAPEshfHWiIvTlWNwuKZI6Z6oFMLx'
ACCESS_TOKEN_SECRET = 'gvZ3Ay5IrGsWBkyd4pxFzHAWO6pWZMd2mEU7XYCnxILzz'
PROXIES = {'https': 'socks5://127.0.0.1:1086'}

# tweets = api.GetUserTimeline()

TIMELINE_PER_REQ_COUNT = 200
TIMELINE_WINDOW_LIMIT = 900

_api = None


def get_api():
    global _api
    if not _api:
        _api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET,
                           ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET,
                           proxies=PROXIES)

    return _api


def get_all_tweets(screen_name=None, user_id=None):
    api = get_api()
    if not user_id and not screen_name:
        raise ValueError("Get all tweets must have id or screen_name")
    user = api.GetUser(screen_name=screen_name, user_id=user_id, include_entities=True)
    statuses_count = user.statuses_count
    print('All statuses count:', user.statuses_count)
    statuses = [user.status]
    req_count = statuses_count // TIMELINE_PER_REQ_COUNT + 1
    # Now ignoring twitter limiting. Per 15 minutes can get max 180K statuses.
    print('Request count:', req_count)
    for _ in range(req_count):
        statuses.extend(
            api.GetUserTimeline(screen_name=user.screen_name, count=TIMELINE_PER_REQ_COUNT, max_id=statuses[-1].id - 1))
        print('%sth' % (_ + 1), 'Response.', 'All Size:', len(statuses))
    return statuses


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(default=None, dest='screen_name', help='User screen name. e.g. @one')
    args = parser.parse_args()

    statues = get_all_tweets(args.screen_name)
    json_statues = [status.AsJsonString() for status in statues]
    all_json_str = '[' + ','.join(json_statues) + ']'
    with open(args.screen_name + '.json', 'w+') as file:
        file.write(all_json_str)
