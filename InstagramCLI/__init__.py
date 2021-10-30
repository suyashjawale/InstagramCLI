import sys
import os
import urllib.request
import requests
import json
from datetime import datetime
import urllib.request
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
                               "comment": "bc3296d1ce80a24b1b6e40b1e72903f5", "internal_comment": "1ee91c32fc020d44158a3192eda98247", "highlights": "d4d88dc1500312af6f937f7b804c68c3"}
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
                "Disclaimer : Following list may contain duplicate and missing records.")
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
                "Disclaimer : Followers list may contain duplicate and missing records.")
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
                    res = json.loads(requests.request(
                        "GET", f"{url}&max_id={next_max_id}{extension}", headers=self.newheaders, data={}).text)
                    users.extend(res['users'])
                    big_list = res['big_list']
                    next_max_id = res['next_max_id']
                    iteration += 1
            except Exception as e:
                pass
            return users
        except Exception as e:
            self.exception(e)

    def tiny_url(self, url):
        try:
            apiurl = "http://tinyurl.com/api-create.php?url="
            tinyurl = urllib.request.urlopen(apiurl + url).read()
            return tinyurl.decode("utf-8")
        except Exception as e:
            self.exception(e)

    def get_user_info(self, target_username, save_to_device=False, itype="explicit", use="general"):
        try:
            user_data = json.loads(requests.request(
                "GET", f"https://www.instagram.com/{target_username}/?__a=1", headers=self.newheaders, data={}).text)
            if not user_data:
                self.console_logger("Non-existent account")
                return {}
            else:
                user_id = user_data['graphql']['user']['id']
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
                    data['username'] = user_data['graphql']['user']['username']
                    data['full_name'] = user_data['graphql']['user']['full_name']
                    data['following_count'] = following_count
                    data['follower_count'] = follower_count
                    data['private'] = user_data['graphql']['user']['is_private']
                    data['verified'] = user_data['graphql']['user']['is_verified']
                    data['bio'] = user_data['graphql']['user']['biography']
                    data['category_name'] = user_data['graphql']['user']['category_name']
                    data['profile_pic_url'] = self.tiny_url(
                        user_data['graphql']['user']['profile_pic_url_hd'])
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
                    return {"id": user_id, "posts": posts, "post_has_next_page": post_has_next_page, "post_end_cursor": post_end_cursor}
                elif itype == "implicit" and use == "igtv":
                    igtv = user_data['graphql']['user']['edge_felix_video_timeline']['edges']
                    igtv_has_next_page = user_data['graphql']['user']['edge_felix_video_timeline']['page_info']['has_next_page']
                    igtv_end_cursor = user_data['graphql']['user']['edge_felix_video_timeline']['page_info']['end_cursor']
                    return {"id": user_id, "igtv": igtv, "igtv_has_next_page": igtv_has_next_page, "igtv_end_cursor": igtv_end_cursor}
        except Exception as e:
            self.exception(e)

    def download_posts(self, url, filename, ext):
        try:
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

    def abstraction(self, inode, caption, shortcode, post_count, save_to_device, folder_name):
        try:
            self.counter += 1
            if inode['__typename'] == "GraphImage":
                if save_to_device:
                    self.download_posts(
                        inode['display_url'], f"{folder_name}/{inode['id']}", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.image_list.append(
                    {"id": inode['id'], "url": inode['display_url'], "caption": caption, "shortcode": shortcode})
            elif inode['__typename'] == "GraphVideo":
                if save_to_device:
                    self.download_posts(
                        inode['display_url'], f"{folder_name}/{inode['id']}_thumbnail", "png")
                    self.download_posts(
                        inode['video_url'], f"{folder_name}/{inode['id']}", "mp4")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.video_list.append({"id": inode['id'], "thumbnail": inode['display_url'],
                                       "url": inode['video_url'], "caption": caption, "shortcode": shortcode})
            if self.counter == post_count:
                return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def extract_posts(self, edge_one, post_count, save_to_device, folder_name):
        try:
            for i in edge_one:
                caption = None
                try:
                    caption = i['node']['edge_media_to_caption']['edges'][0]['node']['text']
                except:
                    caption = ""
                shortcode = i['node']['shortcode']
                if i['node']['__typename'] == "GraphSidecar":
                    for j in i['node']['edge_sidecar_to_children']['edges']:
                        if self.abstraction(j['node'], caption, shortcode, post_count, save_to_device, folder_name) == "Limit Reached":
                            return "Limit Reached"
                elif self.abstraction(i['node'], caption, shortcode, post_count, save_to_device, folder_name) == "Limit Reached":
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

    def get_posts(self, target_username, save_urls=False, save_to_device=False, post_count=50):
        try:
            self.console_logger(f"Account Username : {target_username}")
            self.make_folder(f"{target_username}_posts")
            if post_count == "all":
                post_count = 58000000
            self.image_list = []
            self.video_list = []
            self.counter = 0
            user_data = self.get_user_info(
                target_username, itype="implicit", use="post")
            if not user_data:
                return {}
            main_url = f"https://www.instagram.com/graphql/query/?query_hash={self.query_hash['posts']}&variables=%7B%22id%22%3A%22{user_data['id']}%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFEWUg3VkxBa0ZZMW1mZXVud3RtdlgtRUdIZVVJRE1lVEJKYjJiS1pfMUdwTHNYNExBZ1pBc3ZubGFQQzBydHJMamZlMEpIZm5LM0tkSXQzc19jTXJERg%3D%3D%22%7D"
            if self.extract_posts(user_data['posts'], post_count, save_to_device, f"{target_username}_posts") != "Limit Reached":
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
                            response = json.loads(requests.request("GET", url, headers=self.newheaders, data={}).text)[
                                'data']['user']['edge_owner_to_timeline_media']
                            has_next_page = response['page_info']['has_next_page']
                            end_cursor = response['page_info']['end_cursor']
                            if self.extract_posts(response['edges'], post_count, save_to_device, f"{target_username}_posts") == "Limit Reached":
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

    def extract_reels(self, reels, reel_count, save_to_device, folder_name):
        try:
            for i in reels['items']:
                self.counter += 1
                reel_id = i['media']['id']
                reel_thumbnail = i['media']['image_versions2']['candidates'][0]['url']
                reel_url = i['media']['video_versions'][0]['url']
                shortcode = i['media']['code']
                try:
                    caption = i['media']['caption']['text']
                except:
                    caption = ""
                if save_to_device:
                    self.download_posts(
                        reel_url, f"{folder_name}/{reel_id}", "mp4")
                    self.download_posts(
                        reel_thumbnail, f"{folder_name}/{reel_id}_thumbnail", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.reel_list.append({"reel_id": reel_id, "shortcode": shortcode,
                                      "reel_thumbnail": reel_thumbnail, "reel_url": reel_url, "caption": caption})
                if self.counter == reel_count:
                    return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_reels(self, target_username, save_urls=False, save_to_device=False, reel_count=10):
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
                response = json.loads(requests.request("POST", url, headers=self.soft_headers,
                                      data=f"target_user_id={user_data['id']}&page_size=9&max_id={next_max_id}").text)
                res = self.extract_reels(
                    response, reel_count, save_to_device, f"{target_username}_reels")
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

    def extract_single_hashtag_media(self, hashtag, data, save_to_device, tag_count, folder_name):
        try:
            sata = dict()
            self.counter += 1
            if hashtag['media_type'] == 1:
                sata['url'] = hashtag['image_versions2']['candidates'][0]['url']
                sata['ids'] = hashtag['id']
                sata['alt_text'] = hashtag['accessibility_caption']
                if save_to_device:
                    self.download_posts(
                        sata['url'], f"{folder_name}/{sata['ids']}", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.image_list.append({**sata, **data})
            elif hashtag['media_type'] == 2:
                sata['thumbnail'] = hashtag['image_versions2']['candidates'][0]['url']
                sata['ids'] = hashtag['id']
                sata['url'] = hashtag['video_versions'][0]['url']
                if save_to_device:
                    self.download_posts(
                        sata['url'], f"{folder_name}/{sata['ids']}", "mp4")
                    self.download_posts(
                        sata['thumbnail'], f"{folder_name}/{sata['ids']}_thumbnail", "png")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.video_list.append({**sata, **data})
            if self.counter == tag_count:
                return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def extract_hashtags(self, hashtag, save_to_device, tag_count, folder_name):
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
                            if self.extract_single_hashtag_media(k, data, save_to_device, tag_count, folder_name) == "Limit Reached":
                                return "Limit Reached"
                    else:
                        if self.extract_single_hashtag_media(j['media'], data, save_to_device, tag_count, folder_name) == "Limit Reached":
                            return "Limit Reached"
        except Exception as e:
            self.exception(e)

    def get_hashtags(self, hashtag_name, save_urls=False, save_to_device=False, tag_count=50, hashtag_type="recent"):
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
                if self.extract_hashtags(hashtag['data'][hashtag_type]['sections'], save_to_device, tag_count, f"{hashtag_name}_hashtag") != "Limit Reached":
                    url = f"https://i.instagram.com/api/v1/tags/{hashtag_name}/sections/"
                    iteration = 1
                    while(more_available):
                        if save_to_device == False:
                            self.console_logger(
                                f"Iteration : {iteration}", end="\r")
                        response = json.loads(requests.request("POST", url, headers=self.soft_headers,
                                              data=f"include_persistent=0&max_id={next_max_id}&page={iteration}&tab={hashtag_type}").text)
                        if self.extract_hashtags(response['sections'], save_to_device, tag_count, f"{hashtag_name}_hashtag") == "Limit Reached":
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

    def extract_igtv(self, igtv, mode, post_count, save_to_device, folder_name):
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
                        thumbnail, f"{folder_name}/{ids}_thumbnail", "png")
                    self.download_posts(url, f"{folder_name}/{ids}", "mp4")
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                self.video_list.append({"id": ids, "shortcode": shortcode, "title": title,
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

            if self.extract_igtv(user_data['igtv'], mode, igtv_count, save_to_device, f"{target_username}_igtv") != "Limit Reached":
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
                            response = json.loads(requests.request("GET", url, headers=self.newheaders, data={}).text)[
                                'data']['user']['edge_felix_video_timeline']
                            has_next_page = response['page_info']['has_next_page']
                            try:
                                end_cursor = response['page_info']['end_cursor']
                            except:
                                pass
                            if self.extract_igtv(response['edges'], mode, igtv_count, save_to_device, f"{target_username}_igtv") == "Limit Reached":
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

                        response = json.loads(requests.request("GET", url, headers={
                                              **user_agent, **self.newheaders}, data={}).text)['data']['shortcode_media']['edge_media_to_parent_comment']

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

    def extract_story(self, node, save_to_device, folder_name, story_count):
        try:
            sid = node['id']
            shortcode = node['code']
            if node['media_type'] == 2:
                url = node['video_versions'][0]['url']
                thumbnail = node['image_versions2']['candidates'][0]['url']
                if save_to_device:
                    self.download_posts(
                        thumbnail, f"{folder_name}/{sid}_thumbnail", "png")
                    self.download_posts(url, f"{folder_name}/{sid}", "mp4")
                self.video_list.append(
                    {"sid": sid, "shortcode": shortcode, "thumbnail": thumbnail, "url": url})
            elif node['media_type'] == 1:
                url = node['image_versions2']['candidates'][0]['url']
                if save_to_device:
                    self.download_posts(url, f"{folder_name}/{sid}", "png")
                self.image_list.append(
                    {"sid": sid, "shortcode": shortcode, "url": url})
            if story_count == self.counter:
                return "Limit Reached"
            self.counter += 1
        except Exception as e:
            self.exception(e)

    def get_stories(self, target_username, save_urls=False, save_to_device=False, story_count=50):
        try:
            user_data = self.get_user_info(
                target_username, itype="implicit", use="id")
            if not user_data:
                return {}
            user_id = user_data['id']
            url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={user_id}"
            response = json.loads(requests.request(
                "GET", url, headers=self.newheaders, data={}).text)
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
                if self.extract_story(i, save_to_device, f"{target_username}_stories", story_count) == "Limit Reached":
                    break
                if save_to_device:
                    self.console_logger(
                        f"Downloaded : {self.counter}", end="\r")
                else:
                    self.console_logger(
                        f"Iteration : {self.counter}", end="\r")
            data = {"owner": {"id": user_id, "username": target_username},
                    "image": self.image_list, "video": self.video_list}
            if save_urls:
                self.save_to_files(
                    f"{target_username}_stories/{target_username}_stories.json", data)
            return data
        except Exception as e:
            self.exception(e)

    def get_highlights(self, target_username, save_urls=False, save_to_device=False, story_count=50):
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
            response = json.loads(requests.request(
                "GET", url, headers=self.newheaders, data={}).text)
            reel_ids = [i['node']['id'] for i in response['data']
                        ['user']['edge_highlight_reels']['edges']]
            reel_ids = [reel_ids[i:i + 3] for i in range(0, len(reel_ids), 3)]
            data = {"owner": {"id": user_id, "username": target_username}}
            for i in reel_ids:
                url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=highlight%3A{'&reel_ids=highlight%3A'.join(i)}"
                response = json.loads(requests.request(
                    "GET", url, headers=self.newheaders, data={}).text)
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
                        if self.extract_story(k, save_to_device, f"{target_username}_highlights", story_count) == "Limit Reached":
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
