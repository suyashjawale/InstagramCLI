import sys
import os
import urllib.request
import requests
import json
from datetime import datetime
from urllib import parse
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller


class InstagramCLI():
    def __init__(self, username=None, password=None, hidden=True):
        try:
            if (username==None or password==None) or (username.strip()=="" or password.strip()==""):
                self.console_logger("Login Details cannot be null")
                exit()
            self.download_chromedriver()
            mobile_emulation = {

                "deviceMetrics": {"width": 400, "height": 850, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36"}
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 1
            })
            self.options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            self.options.add_argument("--disable-gpu")
            if hidden:
                self.options.headless = True
            self.options.add_argument('--no-sandbox')
            self.options.add_experimental_option(
                "mobileEmulation", mobile_emulation)
            self.options.add_argument('--ignore-certificate-errors-spki-list')
            self.options.add_argument('--ignore-ssl-errors')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--auto-open-devtools-for-tabs')
            self.query_hash = {"posts": "8c2a529969ee035a5063f2fc8602a0fd", "igtv": "bc78b344a68ed16dd5d7f264681c4c76",
                               "comment": "bc3296d1ce80a24b1b6e40b1e72903f5", "internal_comment": "1ee91c32fc020d44158a3192eda98247", "highlights": "d4d88dc1500312af6f937f7b804c68c3","similar_posts":"110b665208c5116ff70b1509c767633e"}
            self.console_logger("Initiating")
            self.driver = webdriver.Chrome(options=self.options)
            self.wait = WebDriverWait(self.driver, 100)
            self.driver.get("https://www.instagram.com/")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[text()="Log In"]'))).click()
            self.wait.until(EC.element_to_be_clickable(
                (By.NAME, "username"))).send_keys(username)
            self.wait.until(EC.element_to_be_clickable(
                (By.NAME, "password"))).send_keys(password)
            self.console_logger("Authenticating")
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="submit"]'))).click()
            login_req = self.driver.wait_for_request(
                'https://www.instagram.com/accounts/login/ajax/', timeout=100).response
            response = json.loads(login_req.body.decode("utf-8"))
            if login_req.status_code == 200 and response['status'] == "ok":
                if response['authenticated'] == True:
                    self.console_logger("Authentication Successful")
                    self.console_logger("Logging In - ETA 120 seconds")
                    try:
                        self.headers = self.driver.wait_for_request(
                            'reels_tray', timeout=100).headers
                    except:
                        self.console_logger("Login failed. Please try again.")
                        exit()

                    self.console_logger("Login Success")
                    self.console_logger("Use save_to_device=True. As some URLs are active only for 24 hrs.")
                    self.newheaders = {'x-ig-app-id': self.headers['x-ig-app-id'],
                                       'cookie': self.headers['cookie']}
                    csrf = re.search("csrftoken=.*?;", self.newheaders['cookie']).group().replace(
                        "csrftoken=", "").replace(";", "")
                    self.soft_headers = {
                        'x-csrftoken': csrf,
                        'x-ig-app-id': self.newheaders['x-ig-app-id'],
                        'cookie': self.newheaders['cookie'],
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                else:
                    self.console_logger(
                        "Authentication Failed - Incorrect Login Details")
                    exit()
            else:
                self.console_logger(
                    "Authentication Failed - Incorrect Login Details")
                exit()
        except Exception as e:
            self.exception(e)

    def download_chromedriver(self):
        try:
            chromedriver_autoinstaller.install()
        except Exception as e:
            self.exception(e)

    def exception(self, e):
        try:
            self.console_logger(f"Error occured.\nOpen github issue and upload error snapshot - https://github.com/suyashjawale/InstagramCLI/issues\nReason : {e}")
            self.close()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            exit()
        except Exception as e:
            print(e)
            self.close()
            exit()

    def console_logger(self, message, end="\n"):
        try:
            now = datetime.now()
            print(f'{now.strftime("[%d/%m/%Y %H:%M:%S]")} {message}', end=end)
        except Exception as e:
            self.exception(e)

    def save_to_files(self, filename, data):
        try:
            f = open(filename, "w")
            f.write(str(json.dumps(data, indent=4)))
            f.close()
            self.console_logger(f"Saved : {filename}")
        except Exception as e:
            self.exception(e)

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(e)

    def get_following(self, target_username, save_to_file=False):
        try:
            self.console_logger(
                "Disclaimer : Following list may contain duplicate and missing records. High risk of being blocked after 4k records.")
            if(target_username.strip() != ""):
                following = self.get_users(target_username, "following")
                if save_to_file and following:
                    self.save_to_files(
                        f"{target_username}_following.json", following)
                return following
        except Exception as e:
            self.exception(e)

    def get_followers(self, target_username, save_to_file=False):
        try:
            self.console_logger(
                "Disclaimer : Followers list may contain duplicate and missing records. High risk of being blocked after 4k records.")
            if(target_username.strip() != ""):
                followers = self.get_users(
                    target_username, "followers", "&search_surface=follow_list_page")
                if save_to_file and followers:
                    self.save_to_files(
                        f"{target_username}_followers.json", followers)
                return followers
        except Exception as e:
            self.exception(e)

    def get_users(self, target_username, types, extension=""):
        try:
            user_info = self.get_user_info(
                target_username, itype="implicit", use="user")
            if not user_info:
                return []
            self.console_logger(
                f"{target_username} {types.capitalize()} : {user_info[types]}")
            url = f"https://i.instagram.com/api/v1/friendships/{user_info['id']}/{types}/?count=12"
            users = json.loads(requests.request(
                "GET", url, headers=self.newheaders, data={}).text)
            try:
                next_max_id = users['next_max_id']
                big_list = users['big_list']
            except:
                next_max_id = None
            iteration = 2
            users = users['users']
            try:
                while(big_list != "false" and next_max_id != None):
                    self.console_logger(f"Iteration : {iteration}", end="\r")
                    main_req= requests.request("GET", f"{url}&max_id={next_max_id}{extension}", headers=self.newheaders, data={})
                    if main_req.status_code!=200:
                        self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                        break
                    res = json.loads(main_req.text)
                    users.extend(res['users'])
                    big_list = res['big_list']
                    next_max_id = res['next_max_id']
                    iteration += 1
            except Exception as e:
                pass
            return users
        except Exception as e:
            self.exception(e)

    def get_user_info(self, target_username, save_to_device=False, itype="explicit", use="general"):
        try:
            user_data = json.loads(requests.request("GET", f"https://www.instagram.com/{target_username}/?__a=1", headers=self.newheaders, data={}).text)
            if not user_data:
                self.console_logger("Non-existent account")
                return {}
            else:
                user_id = user_data['graphql']['user']['id']
                username = user_data['graphql']['user']['username']
                follower_count = int(
                    user_data['graphql']['user']['edge_followed_by']['count'])
                following_count = int(
                    user_data['graphql']['user']['edge_follow']['count'])

                if itype == "implicit" and use == "id":
                    return {"id": user_id}
                elif itype == "implicit" and use == "user":
                    return {"id": user_id, "followers": follower_count, "following": following_count}
                elif itype == "explicit":
                    data = dict()
                    data['user_id'] = user_id
                    data['username'] = username
                    data['full_name'] = user_data['graphql']['user']['full_name']
                    data['following_count'] = following_count
                    data['follower_count'] = follower_count
                    data['private'] = user_data['graphql']['user']['is_private']
                    data['verified'] = user_data['graphql']['user']['is_verified']
                    data['bio'] = user_data['graphql']['user']['biography']
                    data['category_name'] = user_data['graphql']['user']['category_name']
                    data['profile_pic_url'] = user_data['graphql']['user']['profile_pic_url_hd']
                    data['bio_url'] = user_data['graphql']['user']['external_url']
                    data['follows_you'] = user_data['graphql']['user']['follows_viewer']
                    data['fb_id'] = user_data['graphql']['user']['fbid']
                    data['you_follow'] = user_data['graphql']['user']['followed_by_viewer']
                    data['highlights_count'] = user_data['graphql']['user']['highlight_reel_count']
                    data['professional_account'] = user_data['graphql']['user']['is_professional_account']
                    data['posts_count'] = user_data['graphql']['user']['edge_owner_to_timeline_media']['count']
                    data['igtv_count'] = user_data['graphql']['user']['edge_felix_video_timeline']['count']

                    business_account = user_data['graphql']['user']['is_business_account']
                    if business_account:
                        data['business_address'] = user_data['graphql']['user']['business_address_json']
                        data['contact_business'] = user_data['graphql']['user']['business_contact_method']
                        data['business_email'] = user_data['graphql']['user']['business_email']
                        data['business_phone_number'] = user_data['graphql']['user']['business_phone_number']
                        data['business_category_name'] = user_data['graphql']['user']['business_category_name']
                    if save_to_device:
                        self.save_to_files(f"{target_username}.json", data)
                    return data
                elif itype == "implicit" and use == "post":
                    posts = user_data['graphql']['user']['edge_owner_to_timeline_media']['edges']
                    post_has_next_page = user_data['graphql']['user'][
                        'edge_owner_to_timeline_media']['page_info']['has_next_page']
                    post_end_cursor = user_data['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                    return {"id": user_id,"username":username,"posts": posts, "post_has_next_page": post_has_next_page, "post_end_cursor": post_end_cursor}
                elif itype == "implicit" and use == "igtv":
                    igtv = user_data['graphql']['user']['edge_felix_video_timeline']['edges']
                    igtv_has_next_page = user_data['graphql']['user']['edge_felix_video_timeline']['page_info']['has_next_page']
                    igtv_end_cursor = user_data['graphql']['user']['edge_felix_video_timeline']['page_info']['end_cursor']
                    return {"id": user_id,"username":username,"igtv": igtv, "igtv_has_next_page": igtv_has_next_page, "igtv_end_cursor": igtv_end_cursor}
        except Exception as e:
            self.exception(e)

    def download_posts(self, url, filename, ext):
        try:
            if not os.path.isfile(f"{filename}.{ext}"):
                urllib.request.urlretrieve(url, f"{filename}.{ext}")
        except Exception as e:
            self.exception(e)

    def replace_url(self, url, after_val):
        try:
            splitted = parse.urlsplit(url)
            query = dict(parse.parse_qsl(splitted.query))
            query['variables'] = json.loads(query['variables'])
            query['variables']['after'] = after_val
            query['variables'] = json.dumps(
                query['variables'], separators=(',', ':'))
            replaced = splitted._replace(query=parse.urlencode(query))
            return parse.urlunsplit(replaced)
        except Exception as e:
            self.exception(e)

    def abstraction(self, inode, caption, shortcode, post_count, save_to_device, folder_name, media_type, user_id, username):
        try:
            flag=False
            if inode['__typename'] == "GraphImage" and (media_type=="image" or media_type=="both"):
                if save_to_device:
                    self.download_posts(
                        inode['display_url'], f"{folder_name}/{username}_{inode['id']}", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.image_list.append(
                    {"image_id": inode['id'],"user_id":user_id,"username":username, "url": inode['display_url'], "caption": caption, "shortcode": shortcode})
                flag=True
            elif inode['__typename'] == "GraphVideo" and (media_type=="video" or media_type=="both"):
                if save_to_device:
                    self.download_posts(
                        inode['display_url'], f"{folder_name}/{username}_{inode['id']}_thumbnail", "png")
                    self.download_posts(
                        inode['video_url'], f"{folder_name}/{username}_{inode['id']}", "mp4")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.video_list.append({"video_id": inode['id'],"user_id":user_id,"username":username, "thumbnail": inode['display_url'],
                                       "url": inode['video_url'], "caption": caption, "shortcode": shortcode})
                flag=True
            if flag: self.counter += 1
            if self.counter == post_count+1:
                return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def extract_posts(self, edge_one, post_count, save_to_device, folder_name,media_type):
        try:
            for i in edge_one:
                caption = None
                try:
                    caption = i['node']['edge_media_to_caption']['edges'][0]['node']['text']
                except:
                    caption = ""
                shortcode = i['node']['shortcode']
                user_id = i['node']['owner']['id']
                username = i['node']['owner']['username']
                if i['node']['__typename'] == "GraphSidecar":
                    for j in i['node']['edge_sidecar_to_children']['edges']:
                        if self.abstraction(j['node'], caption, shortcode, post_count, save_to_device, folder_name, media_type, user_id,username) == "Limit Reached":
                            return "Limit Reached"
                elif self.abstraction(i['node'], caption, shortcode, post_count, save_to_device, folder_name, media_type, user_id,username) == "Limit Reached":
                    return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def make_folder(self, folder_name):
        try:
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, folder_name)
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)
        except Exception as e:
            self.exception(e)

    def get_posts(self, target_username, save_urls=False, save_to_device=False, post_count=50,media_type="both"):
        try:
            self.console_logger(f"Account Username : {target_username}")
            self.make_folder(f"{target_username}_posts")
            if post_count == "all":
                post_count = 58000000
            self.image_list = []
            self.video_list = []
            self.counter = 1
            user_data = self.get_user_info(
                target_username, itype="implicit", use="post")
            if not user_data:
                return {}
            main_url = f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['posts']}&variables=%7B%22id%22%3A%22{user_data['id']}%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFEWUg3VkxBa0ZZMW1mZXVud3RtdlgtRUdIZVVJRE1lVEJKYjJiS1pfMUdwTHNYNExBZ1pBc3ZubGFQQzBydHJMamZlMEpIZm5LM0tkSXQzc19jTXJERg%3D%3D%22%7D"
            if self.extract_posts(user_data['posts'], post_count, save_to_device, f"{target_username}_posts",media_type) != "Limit Reached":
                has_next_page = user_data['post_has_next_page']
                if self.image_list or self.video_list:
                    if has_next_page:
                        end_cursor = user_data['post_end_cursor']
                        iteration = 2
                        while has_next_page:
                            if save_to_device == False:
                                self.console_logger(
                                    f"Iteration : {iteration}", end="\r")
                            url = self.replace_url(main_url, end_cursor)
                            defi=requests.request("GET", url, headers=self.newheaders, data={})
                            if defi.status_code!=200:
                                self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                                break
                            response = json.loads(defi.text)['data']['user']['edge_owner_to_timeline_media']
                            has_next_page = response['page_info']['has_next_page']
                            end_cursor = response['page_info']['end_cursor']
                            if self.extract_posts(response['edges'], post_count, save_to_device, f"{target_username}_posts",media_type) == "Limit Reached":
                                break
                            iteration += 1
                else:
                    self.console_logger(
                        "Account may be private or has no posts")
                    return dict()
            data = {"image": self.image_list, "video": self.video_list}
            if save_urls:
                self.save_to_files(
                    f"{target_username}_posts/{target_username}_posts.json", data)
            return data
        except Exception as e:
            self.exception(e)

    def extract_reels(self, reels, reel_count, save_to_device, folder_name, save_music):
        try:
            for i in reels['items']:
                self.counter += 1
                reel_id = i['media']['id']
                reel_thumbnail = i['media']['image_versions2']['candidates'][0]['url']
                reel_url = i['media']['video_versions'][0]['url']
                shortcode = i['media']['code']
                try:
                    view_count= i['media']['view_count']
                except:
                    view_count=None
                try:
                    play_count = i['media']['play_count']
                except:
                    play_count=None
                try:
                    like_count = i['media']['like_count']
                except:
                    like_count=None
                    
                user_id=i['media']['user']['pk']
                target_username=i['media']['user']['username']
                    
                music=self.extract_music(i)
                try:
                    caption = i['media']['caption']['text']
                except:
                    caption = ""
                if save_to_device:
                    self.download_posts(
                        reel_url, f"{folder_name}/{target_username}_{reel_id}", "mp4")
                    self.download_posts(
                        reel_thumbnail, f"{folder_name}/{target_username}_{reel_id}_thumbnail", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                if save_music:
                    self.download_posts(music['download_url'],f"{folder_name}/{music['music_id']}_music","mp3")
                
                self.reel_list.append({"reel_id": reel_id,"username":target_username,"user_id":user_id, "shortcode": shortcode,
                                      "reel_thumbnail": reel_thumbnail, "reel_url": reel_url,"view_count":view_count,"play_count":play_count,"like_count":like_count,"caption": caption, "music":music})
                if self.counter == reel_count:
                    return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_reels(self, target_username, save_urls=False, save_to_device=False, reel_count=10,save_music=False):
        try:
            self.reel_list = []
            self.counter = 0
            self.console_logger(f"Account Username : {target_username}")
            if reel_count == "all":
                reel_count = 58000000
            self.make_folder(f"{target_username}_reels")
            user_data = self.get_user_info(
                target_username, itype="implicit", use="id")
            if not user_data:
                return []
            url = "https://i.instagram.com/api/v1/clips/user/"

            next_max_id = ""
            more_available = True
            iteration = 1
            while more_available:
                self.console_logger(f"Iteration : {iteration}", end="\r")
                defi=requests.request("POST", url, headers=self.soft_headers,data=f"target_user_id={user_data['id']}&page_size=9&max_id={next_max_id}")
                if defi.status_code!=200:
                    self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                    break
                response = json.loads(defi.text)
                res = self.extract_reels(
                    response, reel_count, save_to_device, f"{target_username}_reels",save_music)
                more_available = response['paging_info']['more_available']
                if save_to_device == False:
                    self.console_logger(f"Iteration : {iteration}", end="\r")
                if more_available == False or res == "Limit Reached":
                    break
                next_max_id = response['paging_info']['max_id']
                iteration += 1
            if save_urls:
                self.save_to_files(
                    f"{target_username}_reels/{target_username}_reels.json", self.reel_list)
            return self.reel_list
        except Exception as e:
            self.exception(e)

    def extract_single_hashtag_media(self, hashtag, data, save_to_device, tag_count, folder_name,media_type,username):
        try:
            sata = dict()
            if hashtag['media_type'] == 1 and (media_type=="image" or media_type=="both"):
                sata['url'] = hashtag['image_versions2']['candidates'][0]['url']
                sata['ids'] = hashtag['id']
                sata['alt_text'] = hashtag['accessibility_caption']
                self.counter += 1
                if save_to_device:
                    self.download_posts(
                        sata['url'], f"{folder_name}/{username}_{sata['ids']}", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.image_list.append({**sata, **data})
            elif hashtag['media_type'] == 2 and (media_type=="video" or media_type=="both"):
                sata['thumbnail'] = hashtag['image_versions2']['candidates'][0]['url']
                sata['ids'] = hashtag['id']
                sata['url'] = hashtag['video_versions'][0]['url']
                self.counter += 1
                if save_to_device:
                    self.download_posts(
                        sata['url'], f"{folder_name}/{username}_{sata['ids']}", "mp4")
                    self.download_posts(
                        sata['thumbnail'], f"{folder_name}/{username}_{sata['ids']}_thumbnail", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.video_list.append({**sata, **data})
            if self.counter == tag_count+1:
                return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def extract_hashtags(self, hashtag, save_to_device, tag_count, folder_name,media_type):
        try:
            for i in hashtag:
                for j in i['layout_content']['medias']:
                    data = dict()
                    data['shortcode'] = j['media']['code']
                    data['user_id'] = j['media']['user']['pk']
                    data['username'] = j['media']['user']['username']
                    data['full_name'] = j['media']['user']['full_name']
                    data['profile_pic'] = j['media']['user']['profile_pic_url']
                    try:
                        data['caption'] = j['media']['caption']['text']
                    except:
                        data['caption'] = ""
                    if j['media']['media_type'] == 8:
                        for k in j['media']['carousel_media']:
                            if self.extract_single_hashtag_media(k, data, save_to_device, tag_count, folder_name,media_type,data['username']) == "Limit Reached":
                                return "Limit Reached"
                    else:
                        if self.extract_single_hashtag_media(j['media'], data, save_to_device, tag_count, folder_name,media_type,data['username']) == "Limit Reached":
                            return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_hashtags(self, hashtag_name, save_urls=False, save_to_device=False, tag_count=50, hashtag_type="recent",media_type="both"):
        try:
            self.image_list = []
            self.video_list = []
            self.counter = 0
            self.make_folder(f"{hashtag_name}_hashtag")
            self.console_logger(f"Hashtag Search : {hashtag_name}")
            hashtag = json.loads(requests.request(
                "GET", f"https://www.instagram.com/explore/tags/{hashtag_name}/?__a=1", headers=self.newheaders, data={}).text)
            if "data" in hashtag:
                more_available = hashtag['data'][hashtag_type]['more_available']
                try:
                    next_max_id = hashtag['data'][hashtag_type]['next_max_id']
                except:
                    pass
                if self.extract_hashtags(hashtag['data'][hashtag_type]['sections'], save_to_device, tag_count, f"{hashtag_name}_hashtag",media_type) != "Limit Reached":
                    url = f"https://i.instagram.com/api/v1/tags/{hashtag_name}/sections/"
                    iteration = 1
                    while(more_available):
                        if save_to_device == False:
                            self.console_logger(
                                f"Iteration : {iteration}", end="\r")
                        defi=requests.request("POST", url, headers=self.soft_headers,data=f"include_persistent=0&max_id={next_max_id}&page={iteration}&tab={hashtag_type}")
                        if defi.status_code!=200:
                            self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                            break
                        response = json.loads(defi.text)
                        if self.extract_hashtags(response['sections'], save_to_device, tag_count, f"{hashtag_name}_hashtag",media_type) == "Limit Reached":
                            break
                        more_available = response['more_available']
                        try:
                            next_max_id = response['next_max_id']
                        except:
                            break
                        iteration += 1

            data = {"image": self.image_list, "video": self.video_list}
            if save_urls:
                self.save_to_files(
                    f"{hashtag_name}_hashtag/{hashtag_name}_{hashtag_type}_hashtag.json", data)
            return data
        except Exception as e:
            self.exception(e)

    def extract_igtv(self, igtv, mode, post_count, save_to_device, folder_name,username,user_id):
        try:
            for i in igtv:
                self.counter += 1
                ids = i['node']['id']
                shortcode = i['node']['shortcode']
                try:
                    url = i['node']['video_url']
                except:
                    if mode == "deep":
                        url = json.loads(requests.request(
                            "GET", f"https://www.instagram.com/tv/{shortcode}/?__a=1", headers=self.newheaders, data={}).text)['graphql']['shortcode_media']['video_url']
                    else:
                        url = "Video unavailable - Use mode='deep' as parameter"
                thumbnail = i['node']['display_url']
                title = i['node']['title']
                try:
                    caption = i['node']['edge_media_to_caption']['edges'][0]['node']['text']
                except:
                    caption = ""
                if save_to_device:
                    self.download_posts(
                        thumbnail, f"{folder_name}/{username}_{ids}_thumbnail", "png")
                    self.download_posts(url, f"{folder_name}/{username}_{ids}", "mp4")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.video_list.append({"id": ids,"username":username,"user_id":user_id ,"shortcode": shortcode, "title": title,
                                       "url": url, "thumbnail": thumbnail, "caption": caption})
                if self.counter == post_count:
                    return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_igtv_videos(self, target_username, save_urls=False, save_to_device=False, igtv_count=10, mode="easy"):
        try:
            self.console_logger(f"Account Username : {target_username}")
            if mode == "deep":
                self.console_logger(
                    "Warning : Choosing mode='deep' can result in multiple requests to Instagram Servers, which may freeze the account.")
            else:
                self.console_logger(
                    "Warning : Default value for parameter mode='easy'. Video url after first 12 videos not available.")
            self.make_folder(f"{target_username}_igtv")
            if igtv_count == "all":
                igtv_count = 58000000
            self.video_list = []
            self.counter = 0
            user_data = self.get_user_info(
                target_username, itype="implicit", use="igtv")
            if not user_data:
                return []
            main_url = f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['igtv']}&variables=%7B%22id%22%3A%22{user_data['id']}%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFEWUg3VkxBa0ZZMW1mZXVud3RtdlgtRUdIZVVJRE1lVEJKYjJiS1pfMUdwTHNYNExBZ1pBc3ZubGFQQzBydHJMamZlMEpIZm5LM0tkSXQzc19jTXJERg%3D%3D%22%7D"
            if self.extract_igtv(user_data['igtv'], mode, igtv_count, save_to_device, f"{target_username}_igtv",target_username,user_data['id']) != "Limit Reached":
                has_next_page = user_data['igtv_has_next_page']
                if self.video_list:
                    if has_next_page:
                        end_cursor = user_data['igtv_end_cursor']
                        iteration = 2
                        while has_next_page:
                            if save_to_device == False:
                                self.console_logger(
                                    f"Iteration : {iteration}", end="\r")
                            url = self.replace_url(main_url, end_cursor)
                            defi=requests.request("GET", url, headers=self.newheaders, data={})
                            if defi.status_code!=200:
                                self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                                break
                            response = json.loads(defi.text)['data']['user']['edge_felix_video_timeline']
                            has_next_page = response['page_info']['has_next_page']
                            try:
                                end_cursor = response['page_info']['end_cursor']
                            except:
                                pass
                            if self.extract_igtv(response['edges'], mode, igtv_count, save_to_device, f"{target_username}_igtv",target_username,user_data['id']) == "Limit Reached":
                                break
                            iteration += 1
                else:
                    self.console_logger(
                        "Account may be private or has no channels")
                    return []
            if save_urls:
                self.save_to_files(
                    f"{target_username}_igtv/{target_username}_igtv.json", self.video_list)
            return self.video_list
        except Exception as e:
            self.exception(e)

    def threaded_comment_abstraction(self, comments, cid, ctype):
        try:
            internal = 1
            for j in comments:
                self.console_logger(
                    f"Comment : {self.counter}.{internal}", end="\r")
                self.comment_list.append({
                    "cid": cid,
                    "ctype": ctype,
                    "tid": j['node']['id'],
                    "user_id": j['node']['owner']['id'],
                    "username": j['node']['owner']['username'],
                    "profile_pic": j['node']['owner']['profile_pic_url'],
                    "comment": j['node']['text']
                })
                internal += 1
        except Exception as e:
            self.exception(e)

    def extract_comments(self, comments, comment_count):
        try:
            for i in comments:
                self.counter += 1
                self.console_logger(f"Comment : {self.counter}", end="\r")
                cid = i['node']['id']
                comment = i['node']['text']
                user_id = i['node']['owner']['id']
                username = i['node']['owner']['username']
                profile_pic = i['node']['owner']['profile_pic_url']
                verified = i['node']['owner']['is_verified']
                self.comment_list.append({"cid": cid, "ctype": "parent", "user_id": user_id, "username": username,
                                         "profile_pic": profile_pic, "comment": comment, "verified": verified})
                has_next_page = i['node']['edge_threaded_comments']['page_info']['has_next_page']
                if has_next_page:
                    try:
                        end_cursor = i['node']['edge_threaded_comments']['page_info']['end_cursor']
                    except:
                        pass
                    self.threaded_comment_abstraction(
                        i['node']['edge_threaded_comments']['edges'], cid, "child")
                    internal_url = f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['internal_comment']}&variables=%7B%22comment_id%22%3A%22{cid}%22%2C%22first%22%3A6%2C%22after%22%3A%22QVFEYklqX25rRmN2T1NEekZOVFEyMXc1anI1bnNFUlFUNkJTdWVKcmZ5emY1U3JqT3JEWjBxRkh6cHFncFlnZ2h3NGZhS09uQVN1bWJuRHp0LWN1RWYxYQ%3D%3D%22%7D"
                    while(has_next_page):
                        url = self.replace_url(internal_url, end_cursor)
                        response = json.loads(requests.request("GET", url, headers=self.newheaders, data={}).text)[
                            'data']['comment']['edge_threaded_comments']
                        has_next_page = response['page_info']['has_next_page']
                        try:
                            end_cursor = response['page_info']['end_cursor']
                        except:
                            pass
                        self.threaded_comment_abstraction(
                            response['edges'], cid, "child")
                if comment_count == self.counter:
                    return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_comments(self, media_link, save_comments=False, comment_count=50):
        try:
            if requests.get(media_link).status_code!=200:
                self.console_logger("404 Not found")
                return {}
            media_link = media_link.split("/")
            shortcode = media_link[4]
            self.counter = 0
            self.comment_list = []
            if comment_count == "all":
                comment_count = 58000000
            user_agent = {
                "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36"}
            metadata = json.loads(requests.request(
                "GET", f"https://www.instagram.com/p/{shortcode}/comments/?__a=1", headers={**user_agent, **self.newheaders}, data={}).text)

            owner = dict()
            owner['owner_id'] = metadata['graphql']['shortcode_media']['owner']['id']
            owner['owner_name'] = metadata['graphql']['shortcode_media']['owner']['full_name']
            owner['shortcode'] = shortcode
            owner['owner_username'] = metadata['graphql']['shortcode_media']['owner']['username']
            self.console_logger(f"Belongs to : {owner['owner_username']}")
            self.make_folder(f"{owner['owner_username']}_{shortcode}_comments")
            comments = metadata['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
            has_next_page = metadata['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
            end_cursor = metadata['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']

            main_url = f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['comment']}&variables=%7B%22shortcode%22%3A%22{shortcode}%22%2C%22first%22%3A12%2C%22after%22%3A%22%7B%5C%22cached_comments_cursor%5C%22%3A+%5C%2217893656386382493%5C%22%2C+%5C%22bifilter_token%5C%22%3A+%5C%22KA0BBAAQAAgA_f__AUCAAA%3D%3D%5C%22%7D%22%7D"
            if self.extract_comments(comments, comment_count) != "Limit Reached":
                try:
                    while has_next_page:
                        url = self.replace_url(main_url, end_cursor)
                        defi=requests.request("GET", url, headers={**user_agent, **self.newheaders}, data={})
                        if defi.status_code!=200:
                            self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                            break
                        response = json.loads(defi.text)['data']['shortcode_media']['edge_media_to_parent_comment']
                        has_next_page = response['page_info']['has_next_page']
                        try:
                            end_cursor = response['page_info']['end_cursor']
                        except:
                            break
                        if self.extract_comments(response['edges'], comment_count) == "Limit Reached":
                            break
                except Exception as e:
                    print(e)
            data = {"owner": owner, "comments": self.comment_list}
            if save_comments:
                self.save_to_files(
                    f"{owner['owner_username']}_{shortcode}_comments/{shortcode}_comments.json", data)
            return data
        except Exception as e:
            self.exception(e)

    def extract_story(self, node, save_to_device, folder_name, story_count,target_username,user_id,media_type):
        try:
            sid = node['id']
            shortcode = node['code']
            if node['media_type'] == 2 and (media_type=="video" or media_type=="both"):
                url = node['video_versions'][0]['url']
                thumbnail = node['image_versions2']['candidates'][0]['url']
                self.counter+=1
                if save_to_device:
                    self.download_posts(
                        thumbnail, f"{folder_name}/{target_username}_{sid}_thumbnail", "png")
                    self.download_posts(url, f"{folder_name}/{target_username}_{sid}", "mp4")
                self.video_list.append(
                    {"sid": sid, "username":target_username,"user_id":user_id, "shortcode": shortcode, "thumbnail": thumbnail, "url": url})
            elif node['media_type'] == 1 and (media_type=="image" or media_type=="both"):
                url = node['image_versions2']['candidates'][0]['url']
                self.counter+=1
                if save_to_device:
                    self.download_posts(url, f"{folder_name}/{target_username}_{sid}", "png")
                self.image_list.append(
                    {"sid": sid, "username":target_username,"user_id":user_id,"shortcode": shortcode, "url": url})
            if story_count+1 == self.counter:
                return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_stories(self, target_username, save_urls=False, save_to_device=False, story_count=50,media_type="both"):
        try:
            user_data = self.get_user_info(
                target_username, itype="implicit", use="id")
            if not user_data:
                return {}
            user_id = user_data['id']
            url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={user_id}"
            defi=requests.request("GET", url, headers=self.newheaders, data={})
            if defi.status_code!=200:
                self.console_logger("Something went wrong")
                return {}
            response = json.loads(defi.text)
            self.make_folder(f"{target_username}_stories")
            self.image_list = []
            self.video_list = []
            if story_count == "all":
                story_count = 58000000
            self.counter = 1
            reel_response=response['reels']
            if not reel_response:
                self.console_logger("No stories available")
                return {}
            for i in reel_response[str(user_id)]['items']:
                if self.extract_story(i, save_to_device, f"{target_username}_stories", story_count,target_username,user_id,media_type) == "Limit Reached":
                    break
                if save_to_device:
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                else:
                    self.console_logger(
                        f"Iteration : {self.counter}", end="\r")
            data = {"image": self.image_list, "video": self.video_list}
            if save_urls:
                self.save_to_files(
                    f"{target_username}_stories/{target_username}_stories.json", data)
            return data
        except Exception as e:
            self.exception(e)

    def get_highlights(self, target_username, save_urls=False, save_to_device=False, story_count=50,media_type="both"):
        try:
            user_data = self.get_user_info(
                target_username, itype="implicit", use="id")
            if not user_data:
                return {}
            user_id = user_data['id']
            self.make_folder(f"{target_username}_highlights")
            if story_count == "all":
                story_count = 58000000
            self.counter = 1
            url = f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['highlights']}&variables=%7B%22user_id%22%3A%22{user_id}%22%2C%22include_chaining%22%3Atrue%2C%22include_reel%22%3Afalse%2C%22include_suggested_users%22%3Afalse%2C%22include_logged_out_extras%22%3Afalse%2C%22include_highlight_reels%22%3Atrue%2C%22include_live_status%22%3Afalse%7D"
            defi=requests.request("GET", url, headers=self.newheaders, data={})
            if defi.status_code!=200:
                self.console_logger("Something went wrong")
                return {}
            response = json.loads(defi.text)
            reel_ids = [i['node']['id'] for i in response['data']
                        ['user']['edge_highlight_reels']['edges']]
            reel_ids = [reel_ids[i:i + 3] for i in range(0, len(reel_ids), 3)]
            data = dict()
            for i in reel_ids:
                url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=highlight%3A{'&reel_ids=highlight%3A'.join(i)}"
                defi=requests.request("GET", url, headers=self.newheaders, data={})
                if defi.status_code!=200:
                    self.console_logger("Something went wrong.")
                    break
                response = json.loads(defi.text)
                for j in i:
                    high = response['reels'][f"highlight:{j}"]
                    title = high['title']
                    self.image_list = []
                    self.video_list = []
                    for k in high['items']:
                        if save_to_device:
                            self.console_logger(
                                f"Downloaded : {self.counter}", end="\r")
                        else:
                            self.console_logger(
                                f"Iteration : {self.counter}", end="\r")
                        if self.extract_story(k, save_to_device, f"{target_username}_highlights", story_count,target_username,user_id,media_type) == "Limit Reached":
                            data[title] = {
                                "image": self.image_list, "video": self.video_list}
                            if save_urls:
                                self.save_to_files(
                                    f"{target_username}_highlights/{target_username}_highlights.json", data)
                            return data
                    data[title] = {"image": self.image_list,
                                   "video": self.video_list}
            if save_urls:
                self.save_to_files(
                    f"{target_username}_highlights/{target_username}_highlights.json", data)
            return data
        except Exception as e:
            self.exception(e)

    def find_similar_reels(self,music_id,folder,save_urls,save_to_device,reel_count,save_music):
        try:
            next_max_id=""
            has_next_page=True
            url="https://i.instagram.com/api/v1/clips/music/"
            self.counter=0
            self.reel_list = []
            self.make_folder(f"{folder}_reels")
            iteration=1
            while(has_next_page):
                payload=f'audio_cluster_id={music_id}&original_sound_audio_asset_id={music_id}&max_id={next_max_id}'
                response = requests.request("POST", url, headers=self.soft_headers, data=payload)
                if response.status_code!=200:
                    self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                    break
                response=json.loads(response.text)
                if not save_to_device:
                    self.console_logger(f"Iteration : {iteration}", end="\r")
                if self.extract_reels(response,reel_count,save_to_device,f"{folder}_reels",save_music)=="Limit Reached":
                    break
                iteration+=1
                try:
                    next_max_id=response['paging_info']['max_id']
                except:
                    next_max_id=""
                has_next_page=response['paging_info']['more_available']
            if save_urls:
                self.save_to_files(
                    f"{folder}_reels/{folder}_reels.json", self.reel_list)
            return self.reel_list
        except Exception as e:
            self.exception(e)

    def extract_music(self,response):
        try:
            try:
                music=response['graphql']['shortcode_media']['clips_music_attribution_info']
                return {"music_id" : music['audio_id'],"music_name": music['song_name'],"artist_name":music['artist_name']}
            except:
                if "items" in response:
                    music= response["items"][0]['clips_metadata']
                elif "media" in response:
                    music= response["media"]['clips_metadata']
                try:
                    temp={}
                    temp["music_id"]= music['music_info']['music_asset_info']['audio_cluster_id'] 
                    temp["music_name"]= music['music_info']['music_asset_info']['title']
                    temp["download_url"]= music['music_info']['music_asset_info']['fast_start_progressive_download_url']
                    try:
                        temp['artist_id']= music['music_info']['music_consumption_info']['ig_artist']['pk']
                        temp['artist_username']= music['music_info']['music_consumption_info']['ig_artist']['username']
                        temp['artist_name']= music['music_info']['music_consumption_info']['ig_artist']['full_name']
                        temp['is_private']= music['music_info']['music_consumption_info']['ig_artist']['is_private']
                        temp['is_verified']= music['music_info']['music_consumption_info']['ig_artist']['is_verified']
                    except:
                        temp["artist_name"]= music['music_info']['music_asset_info']['display_artist']
                    return temp
                except:
                    try:
                        temp={}
                        temp['music_id']= music['original_sound_info']['audio_asset_id']
                        temp['music_name']= music['original_sound_info']['original_audio_title']
                        temp['download_url']= music['original_sound_info']['progressive_download_url']
                        try:
                            temp['artist_id']= music['original_sound_info']['ig_artist']['pk']
                            temp['artist_username']= music['original_sound_info']['ig_artist']['username']
                            temp['artist_name']= music['original_sound_info']['ig_artist']['full_name']
                            temp['is_private']= music['original_sound_info']['ig_artist']['is_private']
                            temp['is_verified']= music['original_sound_info']['ig_artist']['is_verified']
                        except:
                            temp['artist_name']=""
                        return temp
                    except:
                        return {}
        except Exception as e:
            self.exception(e)

    def get_similar_reels(self,reel_source=None,save_urls=False,save_to_device=False,reel_count=10,save_music=False):
        try:
            if reel_count=="all":
                reel_count= 58000000
            if reel_source:
                if str(reel_source).isnumeric():
                    self.find_similar_reels(reel_source,reel_source,save_urls,save_to_device,reel_count,save_music)
                else:
                    reel_source=reel_source.split("/")
                    if len(reel_source)==1:
                        reel_source=reel_source[0]
                    else:
                        reel_source=reel_source[4]
                    url = f"https://www.instagram.com/reel/{reel_source}/?__a=1"
                    defi=requests.request("GET", url, headers=self.newheaders,data={})
                    if defi.status_code!=200:
                        self.console_logger("Invalid reel_source.")
                        return {}
                    else:
                        response=json.loads(defi.text)
                        music=self.extract_music(response)
                        if music:
                            self.console_logger(f"Song {music['music_name']} by {music['artist_name']}.")
                            self.find_similar_reels(music['music_id'],music['music_id'],save_urls,save_to_device,reel_count,save_music)
                        else:
                            self.console_logger("No reels found.")
                            return {}
            else:
                self.console_logger("Please provide reel_url or music id to proceed.")
                return {}
        except Exception as e:
            self.exception(e)

    def get_similar_posts(self,media_url,save_urls=False,save_to_device=False,post_count=10,media_type="both"):
        try:
            media_url=media_url.replace("?utm_source=ig_web_copy_link","")
            response=requests.request("GET",f"{media_url}?__a=1",headers=self.newheaders,data={})
            if response.status_code!=200:
                self.console_logger("Invalid url")
                return {}
            else:
                response=json.loads(response.text)
                try:
                    post_id=response['graphql']['shortcode_media']['id']
                except:
                    post_id= response['items'][0]['pk']
                url=f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['similar_posts']}&variables=%7B%22media_id%22%3A%22{post_id}%22%2C%22surface%22%3A%22WEB_EXPLORE_MEDIA_GRID%22%2C%22first%22%3A12%7D"
                
                response = requests.request("GET", url, headers=self.newheaders, data={})
                if response.status_code!=200:
                    self.console_logger("Something went wrong. Please try again.")
                    return {}
                else:
                    self.image_list = []
                    self.video_list = []
                    self.counter = 1
                    response=json.loads(response.text)
                    now = datetime.now()
                    variable=f'{now.strftime("%d_%m_%Y_%H_%M_%S")}_similar_posts'
                    self.make_folder(variable)
                    if self.extract_posts(response['data']['user']['edge_web_media_chaining']['edges'], post_count, save_to_device, variable, media_type) != "Limit Reached":
                        more_available=response['data']['user']['edge_web_media_chaining']['page_info']['has_next_page']
                        iteration=1
                        while more_available:
                            if not save_to_device:
                                self.console_logger(f"Iteration : {iteration}", end="\r")
                            next_max_id=response['data']['user']['edge_web_media_chaining']['page_info']['end_cursor']
                            url=f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['similar_posts']}&variables=%7B%22media_id%22%3A%22{post_id}%22%2C%22surface%22%3A%22WEB_EXPLORE_MEDIA_GRID%22%2C%22first%22%3A12%2C%22after%22%3A%22{next_max_id}%22%7D"

                            response = requests.request("GET", url, headers=self.newheaders, data={})
                            if response.status_code!=200:
                                self.console_logger("Bro, calm down. The system has fried up. Collected data will be saved.")
                                break
                            response=json.loads(response.text)
                            more_available=response['data']['user']['edge_web_media_chaining']['page_info']['has_next_page']
                            if self.extract_posts(response['data']['user']['edge_web_media_chaining']['edges'], post_count, save_to_device, variable, media_type) == "Limit Reached":
                                break
                            iteration+=1

                    data = {"image": self.image_list, "video": self.video_list}
                    if save_urls:
                        self.save_to_files(f"{variable}/similar_posts.json", data)
                    return data
        except Exception as e:
            self.exception(e)

    def get_story_timeline(self,save_urls=False,save_to_device=False,story_count=10,media_type="both"):
        try:
            url = "https://i.instagram.com/api/v1/feed/reels_tray/"
            response = requests.request("GET", url, headers=self.newheaders, data={})
            if response.status_code!=200:
                self.console_logger("Something went wrong. Please try again.")
                return {}
            else:
                if story_count == "all":
                    story_count = 58000000
                self.counter = 1
                self.console_logger("Some stories may not be available.")
                response=json.loads(response.text)
                now = datetime.now()
                variable=f'{now.strftime("%d_%m_%Y_%H_%M_%S")}_my_feed_stories'
                self.make_folder(variable)
                self.image_list = []
                self.video_list = []
                iteration=1
                for i in response['tray']:
                    if not save_to_device:
                        self.console_logger(f"Iteration : {iteration}", end="\r")
                    if "items" in i:
                        for j in i['items']:
                            if self.extract_story(j,save_to_device,variable,story_count,i['user']['username'],i['user']['pk'],media_type)=="Limit Reached":
                                break
                    iteration+=1

                data = {"image": self.image_list, "video": self.video_list}
                if save_urls:
                    self.save_to_files(f"{variable}/feed_stories.json", data)
                return data
        except Exception as e:
            self.exception(e)