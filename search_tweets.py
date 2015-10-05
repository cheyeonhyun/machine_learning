CONSUMER_KEY = 'SynWbLE5Y4qZHDl2GBJgOI4cm'
CONSUMER_SECRET = '3u8uIQASboRuZnI6o3mTyBLCOdU0rZXvW43eUV0nJhir1LDBKg'
ACCESS_TOKEN = '338429673-ctldxuhtVfVwemCJe1EDhesaiSwuXfqDDTrAkANA'
ACCESS_TOKEN_SECRET = 'IYQo6JK4VOpRXf3jZFzAL28foLYxzJPdx4Il22vT5O8qr'

# CONSUMER_KEY = '5Xm1jEjEu7T6iXRhPdcK0Sepk'
# CONSUMER_SECRET = 'mX97DVM76mc1seLlLhMcT5xOsP16ZwWLN8eQWmlsIHuD8R2JPF'
# ACCESS_TOKEN = '1450178244-WtliEAUYj0WXWSINdfAdxO8yPfKvMfwwUozvWu9'
# ACCESS_TOKEN_SECRET = 'eA8UWN4q7hTfY0IOw3T0rKSNeSXyoJPAXz5YErgNRyCJD'

# CONSUMER_KEY = 'CkYQYeiZ9P9bD1Xg3GK4gUxwp'
# CONSUMER_SECRET= 'eZyJRZARy2fyR6IXpv3iQMtzIavggGFhpfIjxKlrExnenlESV4'
# ACCESS_TOKEN = '3386581257-B34i8rEtMsq5n5rbezRb6hJCmhRaoXw583LntbT'
# ACCESS_TOKEN_SECRET = 'b3IoToOafgHWQr82oBTorRIPTatil1R16TQwTTzyaLthS'

# CONSUMER_KEY = 'fO1vW01I5oYWelBj8XXknLmkZ'
# CONSUMER_SECRET = 'DJ36cnWpMHJJWCTHJUG1yhjWBFbeeU9QrsfWzi7TlGFaJrf7Ke'
# ACCESS_TOKEN = '3386676586-Bs6sEWGoWQf1dS6mb3bv35SQhUFXVQGdZw0ob95'
# ACCESS_TOKEN_SECRET = 'UOdKOyzd51ZP4nOYfibyYdPrBMKJ0x2smAX9mbZjAkrJe'

public_commands = {}


def public(f):
    public_commands[f.__name__] = f
    return f


def clean(obj):
    import json
    return json.loads(json.dumps(obj))


class UnicodeCsvWriter(object):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        import csv
        self.f = open(self.filename, self.mode)
        self.csvwriter = csv.writer(self.f, delimiter='\t')
        return self

    def writerow(self, row):
        self.csvwriter.writerow([unicode(cell).encode('utf-8') for cell in row])

    def __exit__(self, type, value, tb):
        try:
            self.f.close()
        finally:
            # rewrite in utf-16 because of Excel
            with open(self.filename, 'rb') as f:
                content = f.read().decode('utf-8')
            with open(self.filename, 'wb') as f:
                f.write(content.encode('utf-16'))


from birdy.twitter import StreamClient
client = StreamClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


KEYS = 'screen_name id name location followers_count favourites_count description'.split(' ')



from birdy.twitter import UserClient
client = UserClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


@public
def search_tweets_by_queries():
    import csv
    from time import sleep
    from birdy.twitter import TwitterRateLimitError
    '''
    Search by Queries
    '''
    # from birdy.twitter import JSONObject
    # import json
    KEYS2 = 'screen_name user_name text date'.split(' ')
    print 'Fetching results'
    group_count = 0
    max_id_list = []
    with open('twitter_search_doximity_mention.csv', 'wb') as f:
        csvwriter = csv.writer(f, delimiter='\t')
        csvwriter.writerow(KEYS2)
        print KEYS2
        while group_count <14:
            if group_count == 0:
                page_data = client.api.search.tweets.get(q='@doximity', count = 100).data
                    # data += page_data
                # max_id_list.append(page_data['search_metadata']['max'])
                print "STATUSES"
                count = 1
                check = []
                for dat in page_data['statuses']:
                    user_info_list = []
                    the_text = clean(dat['text'])
                    print the_text
                    check.append(clean(dat['id']))
                    user_name = clean(dat['user']['name'])
                    date = clean(dat['created_at'])
                    print date
                    print user_name
                    screen_name = clean(dat['user']['screen_name'])
                    print screen_name
                    user_info_list.append(screen_name)
                    user_info_list.append(user_name)
                    user_info_list.append(the_text)
                    user_info_list.append(date)
                    csvwriter.writerow([unicode(user_info_list[key]).encode('utf-8') for key in range(0,4)])
                    print count, "FIRST"
                    count += 1
                max_id_list.append(min(check)-1)
                group_count += 1
                sleep(10)
            else:
                try:
                    page_data = client.api.search.tweets.get(q='@doximity', count = 100, max_id = max_id_list[-1]).data
                        # data += page_data
                    print "SEARCH METADATA:"
                    print clean(page_data['search_metadata'])
                    print "STATUSES"
                    count = 1
                    for dat in page_data['statuses']:
                        user_info_list = []
                        the_text = clean(dat['text'])
                        date = clean(dat['created_at'])
                        print the_text
                        check.append(clean(dat['id']))
                        user_name = clean(dat['user']['name'])
                        print user_name
                        screen_name = clean(dat['user']['screen_name'])
                        print screen_name
                        user_info_list.append(screen_name)
                        user_info_list.append(user_name)
                        user_info_list.append(the_text)
                        user_info_list.append(date)
                        csvwriter.writerow([unicode(user_info_list[key]).encode('utf-8') for key in range(0,4)])
                        print count, group_count
                        count += 1
                        sleep(0.2)
                    max_id_list.append(min(check)-1)
                    group_count += 1
                except TwitterRateLimitError:
                    print 'rate limited; pausing for 900 seconds'
                    sleep(900)
                    continue

    with open('twitter_search_doximity_mention.csv', 'rb') as f:
        content = f.read().decode('utf-8')
    with open('twitter_search_doximity_mention.csv', 'wb') as f:
        f.write(content.encode('utf-16'))


FOLLOWER_KEYS = 'next_cursor ids'.split(' ')


@public
def search_followers_of_doximity():
    print "Searching for followers"
    with UnicodeCsvWriter('doximity_follower2.csv', 'wb') as csvwriter:
        header = ["screen_name"]  + FOLLOWER_KEYS
        csvwriter.writerow(header)
        count = 0
        screen_name = 'doximity'
        def check_next_cursor(next_cur, screen_name, count):
            if count == 0:
                print count, screen_name
                follower_info = get_followers_id(screen_name, next_cur)
                new_line = []
                new_line.append(screen_name)
                for key in FOLLOWER_KEYS:
                    print "KEY"
                    print key
                    try:
                        new_line.append(follower_info[key])
                    except KeyError as e:
                        print e
                        new_line.append(0)
                count += 1
                csvwriter.writerow(new_line)
                check_next_cursor(new_line[1], screen_name, count)
            else:
                print next_cur, screen_name, count
                if next_cur != 0:
                    print "COUNT, screen_name, NEXT_CUR"
                    print count, screen_name, next_cur
                    follower_info = get_followers_id(screen_name, next_cur)
                    new_line = []
                    new_line.append(screen_name)
                    for key in FOLLOWER_KEYS:
                        new_line.append(follower_info[key])
                    csvwriter.writerow(new_line)
                    count += 1
                    print new_line[1]
                    check_next_cursor(new_line[1], screen_name, count)
                else:
                    return
        check_next_cursor(-1, screen_name, count)
        print client_error_list



@public
def change_form():
    import pandas as pd
    import csv
    header = ["screen_name", "follower_user_id"]
    df = pd.DataFrame.from_csv("the_friends_20.csv", encoding='utf-16', sep='\t', header=0, index_col= False)
    with open('the_friends_20.out.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(header)
        for i in df.index:
            list_len = len(df["ids"][i].split())
            print df['screen_name'][i]
            for j in range(list_len):
                follower_id = str(df["ids"][i].split()[j]).strip(",").strip("[").strip("]")
                # print follower_id
                a.writerow([str(df["screen_name"][i]),follower_id])

def get_follower_names_using_lookup(user_ids):
    from time import sleep
    from birdy.twitter import TwitterClientError,TwitterRateLimitError
    for user_ids_group in group(user_ids, 100):
        user_list = list()
        for a in user_ids_group:
            if a == '':
                continue
            else:
                user_list.append(a)
        print "USERLIST"
        print user_list
        try:    
            response = client.api.users.lookup.get(user_id = user_list)
        except TwitterRateLimitError:
                print 'rate limited; pausing for 200 sec'
                sleep(200)
        except TwitterClientError:
                print 'Client Error; pausing for 200 sec'
                sleep(200)
        print "sleep 1sec"
        sleep(1)
        for user_info in response.data:
            print user_info
            yield user_info



KEYS2 = 'id screen_name name followers_count'.split(' ')
@public
def get_doximity_follower_info():
    '''
    Get info regarding doximity followers
    BEFORE RUNNING IT, delete the headerline for the input file
    '''
    print "Searching by screen_name of the followers"
    KEYS2 = 'id screen_name location name followers_count'.split(' ')
    import csv
    with open("doximity_follower_column.out.csv", 'rb') as csvfile:
        with UnicodeCsvWriter('doximity_follower_screen_name.csv', 'wb') as csvwriter:
            csvwriter.writerow(KEYS2)
            reader = csv.reader(csvfile)
            for user_info in get_follower_names_using_lookup(user_id for [screen_name, user_id] in reader):
                csvwriter.writerow([user_info[key] for key in KEYS2])


@public
def search_users_by_queries():
    '''
    Search by Queries
    '''

    print 'Fetching results'
    data = []
    for page_number in xrange(0, 5):
        print 'page', page_number, '...'
        page_data = client.api.users.search.get(q='hospitalist', page=page_number).data
        data += page_data


    # matching_users = data

    # #YAML
    # import yaml
    # print "Searching by queries"
    # output = [
    #     {key: user[key] for key in KEYS}
    #     for user in matching_users
    # ]
    # with open('twitter-test.out.yaml', 'wb') as f:
    #     f.write(yaml.safe_dump(clean(output), default_flow_style=False, width=80))

    # # CSV
    # import csv
    # with open('twitter-test.out.csv', 'wb') as f:
    #     csvwriter = csv.writer(f, delimiter='\t')
    #     csvwriter.writerow(KEYS)
    #     for user in matching_users:
    #         csvwriter.writerow([unicode(user[key]).encode('utf-8') for key in KEYS])

    # # rewrite in utf-16 because of Excel
    # with open('twitter-test.out.csv', 'rb') as f:
    #     content = f.read().decode('utf-8')
    # with open('twitter-test.out.csv', 'wb') as f:
    #     f.write(content.encode('utf-16'))


@public
def rate_limit_status():
    import json
    response = client.api.application.rate_limit_status.get()
    print json.dumps(response.data, sort_keys=True, indent=4)


def group(items, n):
    iterable = iter(items)
    while True:
        group = []
        for i, item in zip(xrange(n), iterable):
            group.append(item)
        if len(group) == 0:
            return
        yield group


def get_user_infos_by_screen_name_using_lookup(screen_names):
    from time import sleep
    from birdy.twitter import TwitterApiError, TwitterRateLimitError
    # count = 0
    for screen_names_group in group(screen_names, 100):
        screen_names_group_string = ','.join(screen_names_group)
        try:
            response = client.api.users.lookup.get(screen_name=screen_names_group_string)
            sleep(1)
            for user_info in response.data:
                yield user_info
        except TwitterRateLimitError:
            print 'rate limited; pausing for 450 seconds'
            sleep(450)
            continue
        except TwitterApiError:
            continue


def get_user_infos_by_screen_name_using_show(screen_names):
    for screen_name in screen_names:
        yield get_user_info_by_screen_name_using_show(screen_name)


def get_user_info_by_screen_name_using_show(screen_name):
    from time import sleep
    from birdy.twitter import TwitterApiError, TwitterRateLimitError, JSONObject

    while True:
        try:
            response = client.api.users.show.get(screen_name=screen_name)
            sleep(1)
            user_info = response.data
        except TwitterRateLimitError as e:
            print 'rate limited; pausing for 10 seconds'
            sleep(10)
            continue
        # People who get TwitterApi error will only print their screen_name
        except TwitterApiError as e:
            if e.status_code in (403, 404):
                response = screen_name
                print response
                user_info = JSONObject(screen_name=screen_name)
            else:  # unexpected errors
                print e.status_code
                raise e
        return user_info

@public
def search_by_screen_name():
    '''
    Search by screen_name
    '''
    print "Searching by screen name"
    import csv

    user_infos = []
    with open("email.csv", 'rU') as csvfile:
        with UnicodeCsvWriter('login_twitter_email.csv', 'wb') as csvwriter:
            csvwriter.writerow(KEYS)
            reader = csv.reader(csvfile, dialect='excel')
            for user_info in get_user_infos_by_screen_name_using_lookup(screen_name for [screen_name] in reader):
                print user_info['name']
                csvwriter.writerow([user_info[key] for key in KEYS])
                user_infos.append(user_info)


def get_retweets_by_screen_name(screen_name):
        from time import sleep
        from birdy.twitter import TwitterApiError, TwitterAuthError, TwitterRateLimitError, JSONObject
        while True:
            try:
                response = client.api.statuses.user_timeline.get(screen_name=screen_name, count = 20, exclude_replies = True, include_rts=False)
                retweet_info = response.data
            except TwitterRateLimitError as e:
                print 'rate limited; pausing for 200 sec'
                sleep(200)
                continue
            except TwitterAuthError as e:
                if e.status_code == 401:
                    print "one TwitterAuthError"
                    print screen_name
                    response = screen_name
                    retweet_info = JSONObject(screen_name = screen_name)
                else:
                    print e.status_code
                    raise e
            except TwitterApiError as e:
                if e.status_code in (403, 404):
                    response = screen_name
                    retweet_info = JSONObject(screen_name = screen_name)
                else:
                    print e.status_code
                    raise e
            return retweet_info

def get_retweeters_by_status_id(status_id):
    from time import sleep
    from birdy.twitter import TwitterRateLimitError
    while True:
        try:
            response = client.api.statuses.retweeters.ids.get(id=status_id)
            retweeeter_info = response.data
        except TwitterRateLimitError:
            print 'rate limited; pausing for 180 sec'
            sleep(180)
            continue
        return retweeeter_info


@public
def search_retweets_by_screename():
    '''
    find info regarding rewtweets by screen_name
    '''
    print "Searching for retweets"
    import csv
    retweet_data = []
    KEYS = 'id text created_at retweet_count'.split(' ')
    with open("twitter_handle2.csv", 'rU') as csvfile:
        with UnicodeCsvWriter('twitter-RETWEET.out.csv', 'wb') as csvwriter:
            header = KEYS + ["screen_name"]
            csvwriter.writerow(header)
            reader = csv.reader(csvfile, dialect='excel')
            for [screen_name] in reader:
                for user_info in get_retweets_by_screen_name(screen_name):
                    new_line = []
                    for key in KEYS:
                        try: 
                            new_line.append(user_info[key])
                        except TypeError:
                            new_line.append(0)
                    new_line.append(screen_name)
                    csvwriter.writerow(new_line)
                    retweet_data.append(user_info)


@public
def search_retweeters_by_id():
    print "Searching for retweeters"
    import csv
    KEYS = 'ids'.split(' ')
    with open("retweet_id6.csv", "rb") as csvfile:
        with UnicodeCsvWriter('twi.out.csv', 'wb') as csvwriter:
            header = ["status_id", "screen_name"] + KEYS
            csvwriter.writerow(header)
            reader = csv.reader(csvfile)
            for [statusid, count, screen_name] in reader:
                if count == '0':
                    continue
                else:    
                    retwitters = get_retweeters_by_status_id(statusid)
                    new_line =[]
                    new_line.append(screen_name)
                    new_line.append(statusid)
                    new_line.append(retwitters['ids'])
                    csvwriter.writerow(new_line)
                    print new_line


client_error_list = list()

def get_followers_id(screen_name, cursor = -1):
    from time import sleep
    from birdy.twitter import TwitterApiError, TwitterAuthError, TwitterClientError,TwitterRateLimitError, JSONObject

    while True:
        try:
            response = client.api.followers.ids.get(screen_name=screen_name, cursor = cursor)
            sleep(1)
            followers_id = response.data
        except TwitterRateLimitError as e:
            print 'rate limited; pausing for 450 seconds'
            sleep(450)
            continue
        except TwitterAuthError as e:
            if e.status_code == 401:
                print "one TwitterAuthError"
                response = screen_name
                followers_id = JSONObject(screen_name = screen_name)
            else:
                print e.status_code
                raise e
        # People who get TwitterApi error will only print their screen_name
        except TwitterApiError as e:
            if e.status_code in (403, 404):
                response = screen_name
                print e.status_code
                followers_id = JSONObject(screen_name = screen_name)
            else:  # unexpected errors
                print e.status_code
                raise e
                followers_id= JSONObject(screen_name = screen_name)
        except TwitterClientError as e:
            print 'TwitterClientError; pausing for 450 sec'
            client_error_list.append(screen_name)
            sleep(450)
            continue
        return followers_id

@public
def search_followers_id():
    print "Searching for followers"
    import csv
    with open("find_followers_20.csv", 'rU') as csvfile:
        with UnicodeCsvWriter('the_followers_20.csv', 'wb') as csvwriter:
            header = ["screen_name"]  + FOLLOWER_KEYS
            csvwriter.writerow(header)
            reader = csv.reader(csvfile, dialect='excel')
            for [screen_name] in reader:
                count = 0
                def check_next_cursor(next_cur, screen_name, count):
                    if count == 0:
                        print count, screen_name
                        follower_info = get_followers_id(screen_name, next_cur)
                        new_line = []
                        new_line.append(screen_name)
                        for key in FOLLOWER_KEYS:
                            try:
                                new_line.append(follower_info[key])
                            except KeyError as e:
                                print e
                                new_line.append(0)
                        count += 1
                        csvwriter.writerow(new_line)
                        check_next_cursor(new_line[1], screen_name, count)
                    else:
                        if next_cur != 0:
                            print count, screen_name, next_cur
                            follower_info = get_followers_id(screen_name, next_cur)
                            new_line = []
                            new_line.append(screen_name)
                            for key in FOLLOWER_KEYS:
                                new_line.append(follower_info[key])
                            csvwriter.writerow(new_line)
                            count += 1
                            print new_line[1]
                            check_next_cursor(new_line[1], screen_name, count)
                        else:
                            return
                check_next_cursor(-1, screen_name, count)
            print client_error_list
                # follower_infos.append(follower_info)

@public
def search_friends_id():
    print "Searching for friends"
    import csv
    with open("find_followers_20.csv", 'rU') as csvfile:
        with UnicodeCsvWriter('the_friends_20.csv', 'wb') as csvwriter:
            header = ["screen_name"]  + FOLLOWER_KEYS
            csvwriter.writerow(header)
            reader = csv.reader(csvfile, dialect='excel')
            for [screen_name] in reader:
                count = 0
                def check_next_cursor(next_cur, screen_name, count):
                    if count == 0:
                        print count, screen_name
                        follower_info = get_followers_id(screen_name, next_cur)
                        new_line = []
                        new_line.append(screen_name)
                        for key in FOLLOWER_KEYS:
                            try:
                                new_line.append(follower_info[key])
                            except KeyError as e:
                                print e
                                new_line.append(0)
                        count += 1
                        csvwriter.writerow(new_line)
                        check_next_cursor(new_line[1], screen_name, count)
                    else:
                        if next_cur != 0:
                            print count, screen_name, next_cur
                            follower_info = get_followers_id(screen_name, next_cur)
                            new_line = []
                            new_line.append(screen_name)
                            for key in FOLLOWER_KEYS:
                                new_line.append(follower_info[key])
                            csvwriter.writerow(new_line)
                            count += 1
                            print new_line[1]
                            check_next_cursor(new_line[1], screen_name, count)
                        else:
                            return
                check_next_cursor(-1, screen_name, count)
            print client_error_list
                # follower_infos.append(follower_info)



def get_follower_infos_by_screen_name_using_lookup(user_ids):
    from time import sleep
    from birdy.twitter import TwitterClientError,TwitterRateLimitError
    for user_ids_group in group(user_ids, 100):
        user_list = list()
        for a in user_ids_group:
            if a == '':
                continue
            else:
                user_list.append(a)
        print "USERLIST"
        print user_list
        try:    
            response = client.api.users.lookup.get(user_id = user_list)
        except TwitterRateLimitError:
                print 'rate limited; pausing for 200 sec'
                sleep(200)
        except TwitterClientError:
                print 'Client Error; pausing for 200 sec'
                sleep(200)
        print "sleep 15sec"
        sleep(16)
        for user_info in response.data:
            print user_info
            yield user_info

#################################
##Already filtered medical ids##
###################################
def list_to_column(input = "twitter-handle_follower_4500-2.csv", output = "twitter-handle_follower4500-2.out.csv"):
    import pandas as pd
    df = pd.DataFrame.from_csv(input, encoding='utf-16', sep='\t', header=0, index_col= False)
    import csv
    header = ["screen_name", "follower_user_id"]
    with open(output, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(header)
        for i in df.index:
            list_len = len(df["ids"][i].split())
            if df["ids"][i] == 0:
                #unathorized to view the followers
                continue
            else:       
                for j in range(list_len):
                    follower_id = str(df["ids"][i].split()[j]).strip(",").strip("[").strip("]")
                    print follower_id
                    a.writerow([str(df["screen_name"][i]),follower_id])


################################################
##### filter only medical ids #################
##############################################3
def filter_medical_ids(medical_handle_csv = 'medical_twitter_handles.csv', follower_input_csv = "twitter-handle_follower_5500.csv", follower_output_csv = 'twitter-handle_follower5500.out.csv'):
    import csv
    import pandas as pd
    medical_handle_list = list()
    with open(medical_handle_csv, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            medical_handle_list.extend(row)
    header = ["screen_name", "follower_user_id"]
    df = pd.DataFrame.from_csv(follower_input_csv, encoding='utf-16', sep='\t', header=0, index_col= False)
    with open(follower_output_csv, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(header)
        for i in df.index:
            list_len = len(df["ids"][i].split())
            if df["ids"][i] == 0:
                #unathorized to view the followers
                continue
            elif df['screen_name'][i] in medical_handle_list:
                print df['screen_name'][i]
                for j in range(list_len):
                    follower_id = str(df["ids"][i].split()[j]).strip(",").strip("[").strip("]")
                    # print follower_id
                    a.writerow([str(df["screen_name"][i]),follower_id])


# KEYS2 = 'id followers_count'.split(' ')
@public
def get_followers_follower_count():
    '''
    Get follower counts of the followers
    BEFORE RUNNING IT, delete the headerline for the input file
    '''
    print "Searching by screen_name of the followers"
    KEYS2 = 'id screen_name name followers_count'.split(' ')
    import csv
    with open("the_friends_20.out.csv", 'rU') as csvfile:
        with UnicodeCsvWriter('the_f_friends20.csv', 'wb') as csvwriter:
            csvwriter.writerow(KEYS2)
            reader = csv.reader(csvfile, dialect='excel')
            for user_info in get_follower_infos_by_screen_name_using_lookup(user_id for [screen_name, user_id] in reader):
                csvwriter.writerow([user_info[key] for key in KEYS2])

@public
def get_lists_members_of_twitter_doctors():
    LIST_KEYS = 'name screen_name twitter_id location'.split(' ')
    response = client.api.lists.members.get(slug = 'twitter-doctors', owner_screen_name = 'hrana', count = 5000)
    with UnicodeCsvWriter('twitter_doctors_list.csv', 'wb') as csvwriter:
        csvwriter.writerow(LIST_KEYS)
        for user in response.data['users']:
            row = []
            row.append(user['name'])
            row.append(user['screen_name'])
            row.append(user['id'])
            row.append(user['location'])
            the_description = user['description']
            the_description = the_description.replace("\n", "")
            the_description = the_description.replace("\r", "")
            row.append(the_description)
            csvwriter.writerow(row)



@public
def check_colleague_follower():
    import pandas as pd
    colleague_df = pd.DataFrame.from_csv("colleague20_list.csv", sep=',', header=0, index_col=False, encoding='utf-16')
    f_followers_10 = pd.DataFrame.from_csv("the_f_friends10.csv", sep='\t', header=0, index_col=False, encoding='utf-16')
    f_followers_20 = pd.DataFrame.from_csv("the_f_friends20.csv", sep='\t', header=0, index_col=False, encoding='utf-16')
    frames = [f_followers_10, f_followers_20]
    followers_df = pd.concat(frames)
    followers_df = followers_df.sort('name')
    # use the first letter of the name to look through the dataframe faster
    followers_df = followers_df.reset_index(drop = True)
    count = 0
    for i in colleague_df.index:
        for j in followers_df.index:
            print i, j
            if repr(colleague_df.loc[i, 'firstname']).lower() in repr(followers_df.loc[j, 'name']).lower():
                print "FIRST round"
                if str(colleague_df.loc[i, 'lastname']).lower() in str(followers_df.loc[j, 'name']).lower():
                    print colleague_df.loc[i, 'firstname'], colleague_df.loc[i, 'lastname'], followers_df.loc[i, 'name']
                    print count
                    count +=1
        print count


if __name__ == '__main__':
    from sys import argv
    try:
        public_commands[argv[1]](*argv[2:])
    except KeyboardInterrupt:
        print 'KeyboardInterrupt'
        exit(1)
