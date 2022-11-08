import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup
import os
import logging
import sys
import urllib.request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

class InstagramCLI():
    def __init__(self, username=None, password=None):
        try:
            logging.info("-----------------------------------")
            self.session = requests.Session()
    
            self.session.cookies.update({
                "csrftoken":"",
                "ds_user_id":"",
                "ig_did":"",
                "ig_nrcb":"",
                "rur":"",
                "sessionid":""
            })

            base_request = self.session.get('https://www.instagram.com/')
            
            self.session.headers = {'Referer': 'https://www.instagram.com/','user-agent': 'Instagram 123.0.0.21.114 (iPhone; CPU iPhone OS 11_4 like Mac OS X; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/605.1.15'}

            self.session.headers.update({'X-CSRFToken': base_request.cookies['csrftoken']})

            self.credentials = {'username': username, 'password': password}
            response = self.session.post('https://www.instagram.com/accounts/login/ajax/', data=self.credentials, allow_redirects=True)

            if response.status_code == 200:
                self.session.headers.update({'x-ig-app-id': '936619743392459', 'X-CSRFToken': response.cookies['csrftoken'], 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
                self.cookies = response.cookies
                response = response.json()
                if response['authenticated']:
                    logging.info("Login Successful")
                else:
                    raise Exception("Login Failed.")
            else:
                if "two_factor_required" in response.json():
                    # Two factor authentication is enabled for your account. Please disable it for sometime. You can enable it again after finishing scraping. Its not like i can't add input() to accept otp. It's just that taking user otp input while program execution feels different. Eg. I mean if someone includes this library in their code and the program just stops to take input() the whole process will stop. Then there is no point in making an automated library. In future if i feel to add it i will surely add this functionality. But for now its not there.
                    raise Exception("Two factor authentication is enabled. Please disable it.")
                else:
                    raise Exception("Login Failed")
        except Exception as e:
            self.error_smaco(e, "__init__")

    def error_smaco(self, e, message):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.error("\nError in %s function at line %s.\nError Message - %s\nType - %s\nPlease try again. If issue persists,then open github issue and upload error snapshot - https://github.com/suyashjawale/InstagramCLI/issues""", message, exc_tb.tb_lineno, e, exc_type)
        exit()

    def make_folder(self,optimized):
        try:
            dt_string = ""
            if optimized['timestamp_folder']:
                dt_string = optimized['dt_string']
            path = os.path.join(os.getcwd(), optimized['folder'] ,f"{optimized['sub_folder']}{dt_string}")
            if not os.path.isdir(path):
                os.makedirs(path)
        except Exception as e:
            self.error_smaco(e,"make_folder")

    def save_json(self, optimized, data):
        try:
            dt_string = ""
            dt_file = ""

            if optimized['timestamp_folder']:
                dt_string = optimized['dt_string']            
            
            if optimized['timestamp_file']:
                dt_file = optimized['dt_string']

            path = os.path.join(os.getcwd(),optimized['folder'],f"{optimized['sub_folder']}{dt_string}", f"{optimized['filename']}{dt_file}.json")

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.error_smaco(e,"save_json")

    def download(self, url, optimized, filename, ext):
        try:
            dt_string = ""
            if optimized['timestamp_folder']:
                dt_string = optimized['dt_string']
            path = os.path.join(os.getcwd(), optimized['folder'] ,f"{optimized['sub_folder']}{dt_string}",f"{filename}.{ext}")
            if not os.path.isfile(path):
                urllib.request.urlretrieve(url, path)
        except Exception as e:
            self.error_smaco(e, "download")

    def get_info(self, username=None):
        try:
            payload = {
                "username": username
            }
            res = self.session.get(
                "https://i.instagram.com/api/v1/users/web_profile_info/", cookies=self.cookies, params=payload)
            if res.status_code == 200:
                return res.json(), True
            else:
                logging.error("User not found")
                return {}, False
        except Exception as e:
            self.error_smaco(e, "__init__")

    def get_following(self, username=None, save=True, optimzations={}):
        now = datetime.now()
        dt_string = now.strftime("_%d_%m_%Y_%H_%M_%S")
        optimzed = {
            "count" : optimzations.get("count","all"),
            "folder" : optimzations.get("folder",username),
            "sub_folder" : optimzations.get("sub_folder","following"),
            "filename" : optimzations.get("filename", f"{username}_following"),
            "timestamp_folder" : optimzations.get("timestamp_folder",False),
            "timestamp_file" : optimzations.get("timestamp_file",False),
            "dt_string" : dt_string
        }
        return self.get_users(username, save, cli_context="following",optimized=optimzed)

    def get_followers(self, username=None, save=True, optimzations={}):
        now = datetime.now()
        dt_string = now.strftime("_%d_%m_%Y_%H_%M_%S")
        optimzed = {
            "count" : optimzations.get("count","all"),
            "folder" : optimzations.get("folder",username),
            "sub_folder" : optimzations.get("sub_folder","followers"),
            "filename" : optimzations.get("filename", f"{username}_followers"),
            "timestamp_folder" : optimzations.get("timestamp_folder",False),
            "timestamp_file" : optimzations.get("timestamp_file",False),
            "dt_string" : dt_string
        }
        return self.get_users(username, save, cli_context="followers",optimized=optimzed)

    def get_users(self, username, save, cli_context, optimized):
        try:
            if username != None:
                user_info, status = self.get_info(username)
                if status:
                    big_list = True
                    users = []
                    res = {"next_max_id": None}
                    user_id = user_info['data']['user']['id']
                    logging.info(f"Fetching {username} {cli_context} data")
                    if optimized['count']=="all":
                        optimized['count'] = int(user_info['data']['user']['edge_follow']['count'])
                    search_surface = None
                    if cli_context == "followers":
                        search_surface = "follow_list_page"
                    try:
                        self.counter=0
                        while big_list and self.counter<optimized['count']:
                            payload = {
                                "count": 12,
                                "max_id": res['next_max_id'],
                                "search_surface": search_surface
                            }
                            self.counter+=12
                            res = self.session.get(
                                f"https://i.instagram.com/api/v1/friendships/{user_id}/{cli_context}/", cookies=self.cookies, params=payload).json()
                            big_list = res['big_list']
                            users.extend(res['users'])
                    except Exception as e:
                        self.error_smaco(e,"")
                        logging.error(f'Cannot scrape user {cli_context}.')
                    if save:
                        self.make_folder(optimized)
                        self.save_json(optimized, data=users)
                    return users
                else:
                    return []
            else:
                logging.error("Please enter valid user.")
                return []
        except Exception as e:
            self.error_smaco(e, f"get_{cli_context}")

    def search(self, query=None, save=True, optimizations={}):
        try:
            if query != None:
                payload = {
                    "context": "blended",
                    "query": query,
                    "rank_token": 0.9938973991144522,
                    "include_reel": "true"
                }
                res = self.session.get("https://i.instagram.com/api/v1/web/search/topsearch/", cookies=self.cookies, params=payload)
                if res.status_code==200:
                    optimized = {
                        "raw_response" : optimizations.get("raw_response",False), 
                        "count" : optimizations.get("count","all"),
                        "save_sd_photo" : optimizations.get("save_sd_photo",False),
                        "save_hd_photo" : optimizations.get("save_hd_photo", False),
                        "folder" : optimizations.get("folder", query),
                        "sub_folder" : optimizations.get("sub_folder", "search"),
                        "filename" : optimizations.get("filename", f"{query}_results"),
                        "timestamp_folder" : optimizations.get("timestamp_folder",False),
                        "timestamp_file" : optimizations.get("timestamp_file",False),
                        "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S")
                    }
                    if optimized['count']=="all":
                        optimized['count']=100000
                    res = res.json()
                    logging.info("Fetching data")
                    self.make_folder(optimized)
                    self.posts=[]

                    for j,i in enumerate(res['users']):
                        if not optimized['raw_response']:
                            self.posts.append(i)
                        if j==optimized['count']:
                            break
                        if optimized['save_sd_photo']:
                            self.download(i['user']['profile_pic_url'],optimized,f"{i['user']['username']}_sd","png")
                        if optimized['save_hd_photo']:
                            user_info, _ = self.get_info(i['user']['username'])
                            self.download(user_info['data']['user']['profile_pic_url_hd'],optimized,f"{i['user']['username']}_hd","png")
                    if optimized['raw_response']:
                        self.posts= res
                else:
                    logging.error("Error. Please try again")
                
                if save:
                    self.save_json(optimized, self.posts)
                return self.posts
            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Invalid query")
                return []
        except Exception as e:
            self.error_smaco(e, "search")

    def abstraction(self, response, optimized, single_post):
        try:
            self.counter += 1
            post_id = response['id']
            if response['media_type'] == 1 and (optimized['media_type'] == "photo" or optimized['media_type'] == "both"):
                img_url = response['image_versions2']['candidates'][0]['url']
                if optimized['save_photo']:
                    self.download(img_url, optimized, post_id, 'png')
                if not optimized['raw_response']:
                    accessibility_caption = response.get(
                        "accessibility_caption", "None")
                    self.posts['image'].append(
                        {**single_post, **{"post_id": post_id, "image_url": img_url, "acccesibility_caption": accessibility_caption}})

            elif response['media_type'] == 2 and (optimized['media_type'] == "video" or optimized['media_type'] == "both"):

                thumbnail = response['image_versions2']['candidates'][0]['url']
                video_url = response['video_versions'][0]['url']
                single_post['music_id'] = single_post['music_title'] = single_post['music_url'] = single_post['artist_id'] = single_post[
                    'artist_username'] = single_post['artist_name'] = single_post['is_private'] = single_post['is_verified'] = None

                if optimized['context'] == "reels":
                    if response['clips_metadata']['music_info'] != None:
                        music_url = response['clips_metadata']['music_info']
                        music_name = music_url['music_asset_info']['title']
                        if not optimized['raw_response']:
                            single_post['music_id'] = music_url['music_asset_info']['audio_cluster_id']
                            single_post['music_url'] = music_url['music_asset_info']['fast_start_progressive_download_url']
                            single_post['music_title'] = music_name

                            try:
                                single_post['artist_id'] = music_url['music_consumption_info']['ig_artist']['pk']
                                single_post['artist_username'] = music_url['music_consumption_info']['ig_artist']['username']
                                single_post['artist_name'] = music_url['music_consumption_info']['ig_artist']['full_name']
                                single_post['is_private'] = music_url['music_consumption_info']['ig_artist']['is_private']
                                single_post['is_verified'] = music_url['music_consumption_info']['ig_artist']['is_verified']
                            except:
                                single_post["artist_name"] = music_url['music_asset_info']['display_artist']

                        if optimized['save_music']:
                            self.download(
                                music_url['music_asset_info']['fast_start_progressive_download_url'], optimized,music_name, 'mp3')

                if optimized['save_video']:
                    self.download(
                        video_url, optimized ,post_id, 'mp4')
                if optimized['save_video_thumbnail']:
                    self.download(
                        thumbnail, optimized ,f"{post_id}_thumbnail", 'png')
                if not optimized['raw_response']:
                    self.posts['video'].append(
                        {**single_post, **{"post_id": post_id, "thumbnail": thumbnail, "video_url": video_url}})

        except Exception as e:
            self.error_smaco(e, "abstraction")

    def extract_media(self, response, optimized):
        try:
            for i in response:
                single_post = {}
                if not optimized['raw_response']:
                    single_post['shortcode'] = i['code']
                    single_post['like_count'] = i.get("like_count", 0)

                    if optimized['context'] == "reels":
                        single_post['view_count'] = i.get("view_count", None)
                        single_post['play_count'] = i.get("play_count", None)
                    try:
                        single_post['username'] = i['user']['username']
                    except:
                        single_post['username'] = ""
                    single_post['user_id'] = i['user']['pk']
                    single_post['caption'] = ""
                    try:
                        single_post['caption'] = i['caption']['text']
                    except:
                        pass

                if i['media_type'] == 8:
                    for j in i['carousel_media']:
                        self.abstraction(j, optimized, single_post)
                else:
                    self.abstraction(i, optimized, single_post)
        except Exception as e:
            self.error_smaco(e, "extract_media")

    def get_posts(self, username=None, save=True, optimizations={}):
        try:
            if username != None:
                user_info, status = self.get_info(username)
                if status:
                    optimized = {
                        "raw_response": optimizations.get("raw_response", False),
                        "media_type": optimizations.get("media_type", "both"),
                        "count": optimizations.get("count", 24),
                        "save_photo": optimizations.get("save_photo", False),
                        "save_video": optimizations.get("save_video", False),
                        "save_video_thumbnail": optimizations.get("save_video_thumbnail", False),
                        "folder":  optimizations.get("folder", username),
                        "sub_folder":  optimizations.get("sub_folder", "posts"),
                        "filename" : optimizations.get("filename", f"{username}_posts"),
                        "save_music": False,
                        "context": "posts",
                        "timestamp_folder" : optimizations.get("timestamp_folder",False),
                        "timestamp_file" : optimizations.get("timestamp_file",False),
                        "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S")
                    }
                    if optimized['count'] == "all":
                        try:
                            optimized['count'] = int(
                                user_info['data']['user']['edge_owner_to_timeline_media']['count'])
                        except:
                            optimized['count'] = 100000

                    self.make_folder(optimized)
                    self.posts = {"image": [], "video": []}
                    if optimized['raw_response']:
                        self.posts = []
                    res = {"next_max_id": None}
                    user_id = user_info['data']['user']['id']
                    more_available = True
                    self.counter = 0
                    logging.info("Fetching Data")
                    try:
                        while more_available and self.counter < optimized['count']:
                            payload = {
                                "count": 12,
                                "max_id": res['next_max_id']
                            }
                            res = self.session.get(
                                f"https://i.instagram.com/api/v1/feed/user/{user_id}/", cookies=self.cookies, params=payload).json()
                            more_available = res['more_available']

                            if optimized['raw_response'] and optimized['media_type'] == "both" and optimized['save_photo'] == False and optimized['save_video'] == False and optimized['save_video_thumbnail'] == False:
                                self.counter += 1
                                self.posts.extend(res['items'])
                            elif optimized['raw_response']:
                                self.posts.extend(res['items'])
                                self.extract_media(res['items'], optimized)
                            else:
                                self.extract_media(res['items'], optimized)
                    except Exception as e:
                        logging.error(
                            f'Execution terminated. Reasons - Limit Reached | Private account | Only God knows')
                    if save:
                        self.save_json(optimized, self.posts)
                    return self.posts
                else:
                    return []
            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Please enter valid user.")
                return []
        except Exception as e:
            self.error_smaco(e, "get_posts")

    def get_reels(self, username=None, save=True, optimizations={}):
        try:
            if username != None:
                user_info, status = self.get_info(username)
                if status:
                    optimized = {
                        "raw_response": optimizations.get("raw_response", False),
                        "media_type": "video",
                        "count": optimizations.get("count", 18),
                        "save_video": optimizations.get("save_video", False),
                        "save_video_thumbnail": optimizations.get("save_video_thumbnail", False),
                        "save_music": optimizations.get("save_music", False),
                        "folder": optimizations.get("folder", username),
                        "filename" : optimizations.get("filename",f"{username}_reels"),
                        "sub_folder": optimizations.get("sub_folder", "reels"),
                        "context": "reels",
                        "timestamp_folder" : optimizations.get("timestamp_folder",False),
                        "timestamp_file" : optimizations.get("timestamp_file",False),
                        "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S")
                    }

                    if optimized['count'] == "all":
                        optimized['count'] = 100000

                    self.make_folder(optimized)

                    self.posts = {"image": [], "video": []}
                    if optimized['raw_response']:
                        self.posts = []
                    more_available = True
                    self.counter = 0
                    res = {"paging_info": {"max_id": None}}

                    user_id = user_info['data']['user']['id']
                    logging.info("Fetching Data")
                    try:
                        while more_available and self.counter < optimized['count']:
                            payload = {
                                "target_user_id": user_id,
                                "page_size": 9,
                                "max_id": res['paging_info']['max_id'],
                                "include_feed_video": "true"
                            }
                            res = self.session.post(
                                "https://i.instagram.com/api/v1/clips/user/", cookies=self.cookies, data=payload).json()
                            more_available = res['paging_info']['more_available']

                            if optimized['raw_response'] and optimized['save_video'] == False and optimized['save_video_thumbnail'] == False and optimized['save_music'] == False:
                                self.posts.extend(res['items'])
                            elif optimized['raw_response']:
                                self.posts.extend(res['items'])
                                self.extract_media(
                                    [i['media'] for i in res['items']], optimized)
                            else:
                                self.extract_media(
                                    [i['media'] for i in res['items']], optimized)
                    except Exception as e:
                        logging.error(
                            f'Execution terminated. Reasons - Limit Reached | Private account | Only God knows')
                    if save:
                        self.save_json(optimized, self.posts)
                    return self.posts
                else:
                    return []
            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Please enter valid user.")
                return []
        except Exception as e:
            self.error_smaco(e, "get_reels")

    def get_music_reels(self, music_id=None, save=True, optimizations={}):
        try:
            if music_id != None:
                optimized = {
                    "raw_response": optimizations.get("raw_response", False),
                    "media_type": "video",
                    "count": optimizations.get("count", 30),
                    "save_video": optimizations.get("save_video", False),
                    "save_video_thumbnail": optimizations.get("save_video_thumbnail", False),
                    "save_music": optimizations.get("save_music", False),
                    "folder": optimizations.get("folder", music_id),
                    "filename" : optimizations.get("filename", f"{music_id}_reels"),
                    "sub_folder": optimizations.get("sub_folder", "reels"),
                    "context": "reels",
                    "timestamp_folder" : optimizations.get("timestamp_folder",False),
                    "timestamp_file" : optimizations.get("timestamp_file",False),
                    "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S")
                }

                if optimized['count'] == "all":
                    optimized['count'] = 100000

                self.make_folder(optimized)

                self.posts = {"image": [], "video": []}
                if optimized['raw_response']:
                    self.posts = []

                more_available = True
                self.counter = 0
                res = {"paging_info": {"max_id": None}}

                logging.info("Fetching Data")
                try:
                    while more_available and self.counter < optimized['count']:
                        payload = {
                            "audio_cluster_id": music_id,
                            "original_sound_audio_asset_id": music_id,
                            "max_id": res['paging_info']['max_id']
                        }

                        res = self.session.post(
                            "https://i.instagram.com/api/v1/clips/music/", cookies=self.cookies, data=payload).json()
                        more_available = res['paging_info']['more_available']

                        if optimized['raw_response'] and optimized['save_video'] == False and optimized['save_video_thumbnail'] == False and optimized['save_music'] == False:
                            self.posts.extend(res['items'])
                        elif optimized['raw_response']:
                            self.posts.extend(res['items'])
                            self.extract_media([i['media'] for i in res['items']], optimized)
                        else:
                            self.extract_media([i['media'] for i in res['items']], optimized)
                except Exception as e:
                    logging.error(f'Execution terminated. Reasons - Limit Reached | Private account | Only God knows')
                if save:
                    self.save_json(optimized, self.posts)
                return self.posts
            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Please enter valid user.")
                return []
        except Exception as e:
            self.error_smaco(e, "get_similar_reels")

    def get_story(self, username=None, save=True, optimizations={}):
        try:
            if username != None:
                user_info, status = self.get_info(username)
                if status:
                    optimized = {

                        "raw_response": optimizations.get("raw_response", False),
                        "media_type": optimizations.get("media_type", "both"),
                        "save_photo": optimizations.get("save_photo", False),
                        "save_video": optimizations.get("save_video", False),
                        "save_video_thumbnail": optimizations.get("save_video_thumbnail", False),
                        "folder":  optimizations.get("folder", username),
                        "sub_folder":  optimizations.get("sub_folder", "story"),
                        "save_music": False,
                        "filename" : optimizations.get("filename", f"{username}_story"),
                        "timestamp_folder" : optimizations.get("timestamp_folder",False),
                        "timestamp_file" : optimizations.get("timestamp_file",False),
                        "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S"),
                        "context": "posts"
                    }

                    user_id = user_info['data']['user']['id']
                    payload = {
                        "reel_ids": user_id
                    }
                    self.counter = 0
                    logging.info("Fetching Data")
                    self.make_folder(optimized)
                    self.posts = {"image": [], "video": []}

                    if optimized['raw_response']:
                        self.posts = []
                    res = self.session.get(
                        "https://i.instagram.com/api/v1/feed/reels_media/", cookies=self.cookies, params=payload)

                    if res.status_code == 200:
                        res = res.json()
                        if res['reels_media']:
                            res = res['reels_media'][0]
                            if optimized['raw_response'] and optimized['media_type'] == "both" and optimized['save_photo'] == False and optimized['save_video'] == False and optimized['save_video_thumbnail'] == False:
                                self.posts.extend(res['items'])

                            elif optimized['raw_response']:
                                self.posts.extend(res['items'])
                                self.extract_media(res['items'], optimized)

                            else:
                                self.extract_media(res['items'], optimized)
                        else:
                            logging.info("No stories available. | Account is private.")
                        if save:
                            self.save_json(optimized, self.posts)
                        return self.posts
                    else:
                        logging.error("Error. while fetching stories")
            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Please enter valid user.")
                return []
        except Exception as e:
            self.error_smaco(e, "get_story")

    def extract_comments(self, comments, optimizations):
        try:
            for i in comments:
                self.counter += 1
                toast = {
                    "cid": i['pk'],
                    "ctype": "parent",
                    "text": i.get('text', None),
                    "utc_time": i['created_at_utc'],
                    "user_id": i['user']['pk'],
                    "username": i['user']['username'],
                    "fullname": i['user']['full_name'],
                    "is_private": i['user']['is_private'],
                    "is_verified": i['user']['is_private']
                }
                self.comments.append(toast)
                if optimizations['child_comments'] and i.get('child_comment_count', 0) > 0:
                    payload = {
                        "max_id": ""
                    }
                    response = self.session.get(
                        f"https://i.instagram.com/api/v1/media/{optimizations['post_id']}/comments/{i['pk']}/child_comments/", cookies=self.cookies, params=payload)
                    if response.status_code == 200:
                        response = response.json()
                        for j in response['child_comments']:
                            toast = {
                                "cid": j['pk'],
                                "ctype": "child",
                                "text": j.get('text', None),
                                "utc_time": j['created_at_utc'],
                                "user_id": j['user']['pk'],
                                "username": j['user']['username'],
                                "fullname": j['user']['full_name'],
                                "is_private": j['user']['is_private'],
                                "is_verified": j['user']['is_private']
                            }
                            self.comments.append(toast)
        except Exception as e:
            self.error_smaco(e, "extract_comments")

    def get_comments(self, shortcode=None, save=True, optimizations={}):
        try:
            if shortcode != None:
                res = requests.request(
                    "GET", f"https://www.instagram.com/p/{shortcode}/", headers={}, data={})
                soup = BeautifulSoup(res.text, 'html.parser')

                post_id = soup.find("meta", {"property": "al:ios:url"})
                post_id = post_id['content'].replace(
                    "instagram://media?id=", "")
                optimized = {
                    "raw_response": optimizations.get("raw_response", False),
                    "count": optimizations.get("count", 60),
                    "child_comments": optimizations.get("child_comments", False),
                    "folder" : optimizations.get("folder",shortcode),
                    "filename" : optimizations.get("filename",f"{shortcode}_comments"),
                    "sub_folder" : optimizations.get("sub_folder","comments"),
                    "post_id": post_id,
                    "timestamp_folder" : optimizations.get("timestamp_folder",False),
                    "timestamp_file" : optimizations.get("timestamp_file",False),
                    "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S"),
                }
                more_available = True
                self.counter = 0
                if optimized['count'] == "all":
                    optimized['count'] = 100000000
                res = {"next_min_id": None}
                self.counter = 0
                self.comments = []
                logging.info("Fetching data")
                self.make_folder(optimized)
                try:
                    while more_available and self.counter < optimized['count']:
                        payload = {
                            "can_support_threading": "true",
                            "min_id": res['next_min_id']
                        }
                        res = self.session.get(
                            f"https://i.instagram.com/api/v1/media/{post_id}/comments/", cookies=self.cookies, params=payload).json()
                        more_available = res['has_more_headload_comments']
                        if optimized['raw_response'] and optimized['fetch_child_comments'] == False:
                            self.counter += len(res['comments'])
                            self.comments.extend(res['comments'])
                        else:
                            self.extract_comments(res['comments'], optimized)
                except Exception as e:
                    logging.error(
                        f'Execution terminated. Reasons - Limit Reached | Private account | Only God knows')
                if save:
                    self.save_json(optimized, self.comments)
                return self.comments
            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Please enter valid post.")
                return []
        except Exception as e:
            self.error_smaco(e, "get_comments")

    def get_highlights(self, username=None, save=True, optimizations={}):
        try:
            if username != None:
                user_info, status = self.get_info(username)
                if status:
                    user_id = user_info['data']['user']['id']
                    optimized = {
                        "raw_response": optimizations.get("raw_response", False),
                        "media_type": optimizations.get("media_type", "both"),
                        "highlight_count": optimizations.get("highlight_count", 4),
                        "story_count": optimizations.get("story_count", 10),
                        "save_photo": optimizations.get("save_photo", False),
                        "save_video": optimizations.get("save_video", False),
                        "save_video_thumbnail": optimizations.get("save_video_thumbnail", False),
                        "folder":  optimizations.get("folder", username),
                        "sub_folder":  optimizations.get("sub_folder", "highlights"),
                        "save_music": False,
                        "filename" : f"{username}_highlights",
                        "context": "posts",
                        "timestamp_folder" : optimizations.get("timestamp_folder",False),
                        "timestamp_file" : optimizations.get("timestamp_file",False),
                        "dt_string" : datetime.now().strftime("_%d_%m_%Y_%H_%M_%S")
                    }

                    if optimized['highlight_count'] == "all":
                        optimized['highlight_count'] = 10000000

                    if optimized['story_count'] == "all":
                        optimized['story_count'] = 10000000

                    user_id = user_info['data']['user']['id']
                    self.counter = 0
                    logging.info("Fetching Data")
                    self.make_folder(optimized)
                    self.posts = {"image": [], "video": []}

                    if optimized['raw_response']:
                        self.posts = []

                    res = self.session.get(f"https://www.instagram.com/graphql/query/?query_hash=d4d88dc1500312af6f937f7b804c68c3&variables=%7B%22user_id%22%3A%22{user_id}%22%2C%22include_chaining%22%3Afalse%2C%22include_reel%22%3Afalse%2C%22include_suggested_users%22%3Afalse%2C%22include_logged_out_extras%22%3Afalse%2C%22include_highlight_reels%22%3Atrue%2C%22include_live_status%22%3Afalse%7D", cookies=self.cookies)

                    highlights = {}
                    if res.status_code == 200:
                        res = res.json()
                        lists = [i['node']['id'] for i in res['data']['user']['edge_highlight_reels']['edges']][:optimized['highlight_count']]
                        batch = 3
                        for travel in range(0,len(lists),batch):
                            res = "&".join([f"reel_ids=highlight%3A{i}" for i in lists[travel:travel + batch]])
                            res = self.session.get(f"https://i.instagram.com/api/v1/feed/reels_media/?{res}", cookies=self.cookies)
                            if res.status_code == 200:
                                res = res.json()
                                if optimized['raw_response'] and optimized['media_type'] == "both" and optimized['save_photo'] == False and optimized['save_video'] == False and optimized['save_video_thumbnail'] == False:
                                    for i in res['reels_media']:
                                        highlights[i['title']] = i['items']
                                elif optimized['raw_response']:
                                    for i in res['reels_media']:
                                        items = i['items']
                                        max_len = len(items) if optimized['story_count']>=len(items) else optimized['story_count']
                                        highlights[i['title']] = items[:max_len]
                                        self.extract_media(items[:max_len], optimized)
                                else:
                                    for i in res['reels_media']:
                                        items = i['items']
                                        max_len = len(items) if optimized['story_count']>=len(items) else optimized['story_count']
                                        highlights[i['title']] = items[:max_len]
                                        self.posts = {"image": [], "video": []}
                                        self.extract_media(items[:max_len], optimized)
                                        highlights[i['title']] = self.posts
                            else:
                                logging.error("aOOPS error occured")

                        if save:
                            self.save_json(optimized, highlights)
                        return highlights
                    else:
                        logging.error("Error. while fetching stories")

            else:
                # Now here you might feel why i have added return instead of raising exception. Cause if someone is running multiple functions and if one function raised exception. the whole program will exit(). Cause the error_smaco has an exit() in it. But for login functionality. I have added exception as there is no point in moving forward if error occurs.
                logging.error("Please enter valid username.")
                return []
        except Exception as e:
            self.error_smaco(e, "get_highlights")
