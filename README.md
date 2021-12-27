# InstagramCLI 
InstagramCLI is the most advanced scraping library made by reverse-engineering the Instagram API calls which has low latency.
InstagramCLI can be used as a data-gathering tool for data science and osint practices.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) 
#####
[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)   [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)   [![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-380/) [![Python 3.9](https://img.shields.io/badge/python-3.9-violet.svg)](https://www.python.org/downloads/release/python-390/) 

#### Checkout repo 
[![forthebadge made-with-python](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/suyashjawale/InstagramCLI) 

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install InstagramCLI.
```bash
pip install InstagramCLI
```
##### Limitations 
- Works on **Chrome Browser** only on **Windows OS**.
## Documentation and Usage



### 1. get_user_info() 
Get information about a user.
```python
get_user_info(target_username,save_to_device=False)
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_to_device     | Save response to json file | **True** or **False** | **False**      |

### Response
```
{
    "user_id": string,                     // Instagram id of user
    "username": string,                    // Instagram username of user
    "full_name": string,                   // Instagram name of user
    "following_count": int,                // Following count of user
    "follower_count": int,                 // Follower count of user
    "private": boolean,                    // Account is private= True else False
    "verified": boolean,                   // Account is verified=True else False
    "bio": string,                         // Bio text
    "category_name": string,               // Person category name
    "profile_pic_url": string,             // Tiny url link
    "bio_url": string,                     // Website link  
    "follows_you": boolean,                // If the user follows you
    "fb_id": string,                       // Facebook profile id
    "you_follow": boolean,                 // If you follow the user
    "highlights_count": int,               // Number of highlights present on profile
    "professional_account": boolean,       // If the account is professional account
    "posts_count": int,                    // Number of posts on account
    "igtv_count": int                      // Number of igtv videos on account
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_user_info(target_username="instagram",save_to_device=True)
cli.close()
```
####
_________________________

### 2. get_followers()
Get followers of particluar account.
```python
get_followers(target_username, save_to_file=False)
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_to_device     | Save followers list to json file | **True** or **False** | **False**      |

### Response
```
#List of dictionaries
[
    {
        "pk": int,                                    // Instagram Id of user
        "username": string,                           // Instagram Username 
        "full_name": string,                          // Name
        "is_private": boolean,                        // If account private - True else False
        "profile_pic_url": string,                    // Url for Profile Pic
        "profile_pic_id": string,                     // Id for for profile pic
        "is_verified": boolean,                       // Verified account tag
        "follow_friction_type": int,                  // Don't know
        "has_anonymous_profile_picture": boolean,     // Default Profile icon
        "account_badges": list,                       // Don't know
        "latest_reel_media": int                      // story id
    }
    ...
]
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_followers(target_username="suyash.jawale", save_to_file=True)
cli.close()
```
####
_________________________

### 3. get_following()
Get following of particular account.
```python
get_following(target_username, save_to_file=False)
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_to_device     | Save following list to json file | **True** or **False** | **False**      |

### Response
```
#List of dictionaries
[
    {
        "pk": int,                                    // Instagram Id of user
        "username": string,                           // Instagram Username 
        "full_name": string,                          // Name
        "is_private": boolean,                        // If account private - True else False
        "profile_pic_url": string,                    // Url for Profile Pic
        "profile_pic_id": string,                     // Id for for profile pic
        "is_verified": boolean,                       // Verified account tag
        "follow_friction_type": int,                  // Don't know
        "has_anonymous_profile_picture": boolean,     // Default Profile icon
        "account_badges": list,                       // Don't know
        "latest_reel_media": int                      // story id
    }
    ...
]
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_following(target_username="instagram", save_to_file=True)
cli.close()
```
####
_________________________

### 4. get_posts()
Fetch post media and post metadata.
```python
get_posts(target_username,save_urls=False,save_to_device=False,post_count=50,media_type="both")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save images and videos to device | **True** or **False** | **False**      |
|post_count|Number of post to scrape|**all** or **number**|**50**|
|media_type|Scrape only image or video or both |**image** or **video** or **both**|**both**|

### Response
```
{
    "image": [
        {
            "image_id": string,          // Image id
            "user_id": string,           // IG id of user
            "username": string,          // IG username of user
            "url": string,               // Url for image
            "caption": string,           // Image Caption
            "shortcode": string          // Image identifier code
        }
    ],
    "video": [
        {
            "video_id": string,          // Video Id
            "user_id": string,           // IG id of user
            "username": string,          // IG username of user
            "thumbnail": string,         // Video thumbnail
            "url": string,               // video download url
            "caption": string,           // Video Caption
            "shortcode": string          // Video identifier code
        }
    ]
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_posts(target_username="instagram",save_urls=True,save_to_device=False,post_count=10,media_type="image")
cli.close()
```
####
_________________________


### 5. get_reels()
Fetch reel videos and metadata.
```python
get_reels(target_username,save_urls=False,save_to_device=False,reel_count=10,save_music=False)
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save images and videos to device | **True** or **False** | **False**      |
|reel_count|Number of reels to scrape|**all** or **number**|**10**|
|save_music|Save music to mp3|**True** or **False**|**False**|

### Response
```
#List of dictionaries
[
{
        "reel_id": string,                   // id of reel
        "username": string,                  // User of reel owner 
        "user_id": int,                      // User id of reel owner
        "shortcode": string,                 // reel identifier
        "reel_thumbnail": string,            // reel thumbnail
        "view_count": int,                   // view count of video
        "play_count": int,                   // play count of video
        "like_count": int,                   // like count of video
        "caption": string,                   // reel caption
        "music": {
            "music_id": string,              // Music id 
            "music_name": string,            // Music name
            "download_url": string,          // Download link for mp3 
            "artist_id": int,                // Music owner id
            "artist_username": string,       // Music owner username
            "artist_name": string,           // Music owner name
            "is_private": boolean,           // Music owner-is private account 
            "is_verified": boolean           // Music owner-is verified account
        }
    },
    ...
]
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_reels(target_username="instagram",save_urls=True,save_to_device=False,reel_count="all",save_music=True)
cli.close()
```
####
_________________________

### 6. get_hashtags()
Search and fetch hashtag media and metadata.
```
get_hashtags(hashtag_name,save_urls=False,save_to_device=False,tag_count=50,hashtag_type="recent",media_type="both")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|hashtag_name       | Name of hashtag to scrape     | --    | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save images and videos to device | **True** or **False** | **False**      |
|tag_count|Number of reels to scrape|**all** or **number**|**50**|
|hashtag_type|Scrape "recent" or "top" hashtags.|**recent** or **top**|**recent**|
|media_type|Scrape only image or video or both |**image** or **video** or **both**|**both**|
### Response
```
{
    "image": [
        {
            "url": string,               // image url 
            "ids": string,               // image id  
            "alt_text": string,          // text describing photo
            "shortcode": string,         // image identifier
            "user_id": int,              // profile id of user who posted
            "username": string,          // username of person who posted
            "full_name": string,         // name of user who posted
            "profile_pic": string,       // profile url of user who posted
            "caption": string            // image caption
        }
        ],
    "video": [
        {
            "thumbnail": string,        // Video thumbnail 
            "ids": string,              // video id
            "url": string,              // video url
            "shortcode": string,        // video shortcode
            "user_id": int,             // profile id of person who posted
            "username": string,         // username of person who posted
            "full_name": string,        // Name of person who posted
            "profile_pic": string,      // Profile pic url for person
            "caption": string           // video caption
        }
    ]
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_hashtags(hashtag_name="carvideos",save_urls=True,save_to_device=False,tag_count=20,hashtag_type="top")
cli.close()
```
####
_________________________

### 7. get_igtv_videos()
Get IGTV video media and metadata. 
```
get_igtv_videos(target_username,save_urls=False,save_to_device=False,igtv_count=10,mode="easy")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save images and videos to device | **True** or **False** | **False**      |
|igtv_count|Number of videos to scrape|**all** or **number**|**10**|
|mode|There are two types of mode. For mode="easy" , url after 12 videos will be missing. Choose mode="deep" if you want url for all videos(which may freeze your account for multiple requests)|**deep** or **easy**|**easy**|

### Response
```
#List of dictionaries
[
    {
        "id": string,                    // igtv video id
        "shortcode": string,             // video identifier
        "title": string,                 // video title 
        "url": string,                   // video url
        "caption": string                // video caption
    },
    ...
]
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_igtv_videos(target_username="instagram",save_urls=True,save_to_device=False,igtv_count=10,mode="deep")
cli.close()
```
####
_________________________

### 8. get_comments()
Scrape comments for any media.
```
get_comments(media_link,save_comments=False,comment_count=50)
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|media_link     | Link to post/reel/igtv    | --    | --    |
|save_comments|Save response to json file|**True** or **False**|**False**|
|comment_count      | Count of comments to scrape | **all** or **number** | **50**      |


### Response
```
{
    "owner": {
        "owner_id": string,                       // Instagram id of person who owns media
        "owner_name": string,                     // Name of person who owns media
        "shortcode": string,                      // Post identifier
        "owner_username": string                  // username of person who owns media
    },
    "comments": [
        {
            "cid": "string,                       // id of comment
            "ctype": string,                      // type of comment - parent
            "user_id": string,                    // Instagram id of person who commented
            "username": string,                   // Username of person who commented
            "profile_pic": string,                // Profile Picture of person who commented
            "comment": string,                    // Comment which the person made
            "verified": boolean                   // Person who commented is verified
        },
        {
            "cid": string,                        // comment id for above comment - as this is reply for above comment
            "ctype": string,                      // type of comment - child
            "tid": string,                        // comment id of this comment
            "user_id": string,                    // Instagram id for person who commented above comment
            "username": string,                   // username of person who commented above comment
            "profile_pic": string,                // profile pic of person who commented above comment
            "comment": string                     // reply to above comment
        },
        ...
    ]
}
```
#### Where to find link ⤵️

![MarineGEO circle logo](https://i.postimg.cc/MHVj2hGk/Capture12.jpg) 

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_comments(media_link="https://www.instagram.com/p/CVCXNoRKvId/?utm_source=ig_web_copy_link",save_comments=True,comment_count=10)
cli.close()
```
####
_________________________


### 9. get_stories()
Download stories and metadata for particular account.
```
get_stories(target_username,save_urls=False,save_to_device=False,story_count=50,media_type="both")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save images and videos to device | **True** or **False** | **False**      |
|story_count|Number of reels to scrape|**all** or **number**|**50**|
|media_type|Scrape only image or video or both |**image** or **video** or **both**|**both**|

### Response
```
{
    "image": [
            {
            "sid": string,            // Story id
            "username": string,       // Username of owner
            "user_id": int,           // Owner IG id
            "shortcode": string,      // Story identifier
            "url": string             // Story download url
        }
        ],
    "video": [
        {
            "sid": string,           // Video id
            "username": string,      // IG owner username
            "user_id": string,       // IG owner id
            "shortcode": string,     // Video identifier
            "thumbnail": string,     // Video thumbnail
            "url": string            // Video url
        }
    ]
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_stories(target_username="unnatiparab",save_urls=True,save_to_device=False,story_count=10)
cli.close()
```
####
_________________________


### 10. get_highlights()
Scrape account highlights media and metadata
```
get_highlights(target_username,save_urls=False,save_to_device=False,story_count=50,media_type="both")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|target_username    | Username of account to scrape     | --    | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save images and videos to device | **True** or **False** | **False**      |
|story_count|Number of reels to scrape|**all** or **number**|**50**|
|media_type|Scrape only image or video or both |**image** or **video** or **both**|**both**|

### Response
```
{
    "Highlight_name":{
    "image": [
            {
            "sid": string,            // Story id
            "username": string,       // Username of owner
            "user_id": int,           // Owner IG id
            "shortcode": string,      // Story identifier
            "url": string             // Story download url
        }
        ],
    "video": [
        {
            "sid": string,           // Video id
            "username": string,      // IG owner username
            "user_id": string,       // IG owner id
            "shortcode": string,     // Video identifier
            "thumbnail": string,     // Video thumbnail
            "url": string            // Video url
        }
    ]
}
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_highlights(target_username="rashmika_mandanna",save_urls=True,save_to_device=False,story_count=10)
cli.close()
```
####
_________________________


### 10. get_similar_reels()
Find reels with same music.
```
get_similar_reels(reel_source,save_urls=False,save_to_device=False,reel_count=10,save_music=False)
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|reel_source    | Enter reel **url** or **shortcode** or **music_id**     |     | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save videos to device | **True** or **False** | **False**      |
|reel_count|Number of reels to scrape|**all** or **number**|**10**|
|save_music|Save **.mp3** file to device|**True** or **False**|**False**|

#### Where to find link ⤵️

[![33.jpg](https://i.postimg.cc/3JgHCFN1/33.jpg)](https://postimg.cc/zVXMqWnH)
### Response
```
[
{
        "reel_id": string,                   // id of reel
        "username": string,                  // User of reel owner 
        "user_id": int,                      // User id of reel owner
        "shortcode": string,                 // reel identifier
        "reel_thumbnail": string,            // reel thumbnail
        "view_count": int,                   // view count of video
        "play_count": int,                   // play count of video
        "like_count": int,                   // like count of video
        "caption": string,                   // reel caption
        "music": {
            "music_id": string,              // Music id 
            "music_name": string,            // Music name
            "download_url": string,          // Download link for mp3 
            "artist_id": int,                // Music owner id
            "artist_username": string,       // Music owner username
            "artist_name": string,           // Music owner name
            "is_private": boolean,           // Music owner-is private account 
            "is_verified": boolean           // Music owner-is verified account
        }
    },
]
```

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_similar_reels(reel_source="https://www.instagram.com/reel/CX03x8vFPgk/?utm_source=ig_web_copy_link",save_urls=True,save_to_device=False,reel_count=10,save_music=True)
cli.close()
```
####
_________________________

### 11. get_similar_posts()
Find similar posts. Some posts may not be similar.
``` python
get_similar_posts(media_url,save_urls=False,save_to_device=False,post_count=10,media_type="both")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|media_url    | Enter post **url**|     | --    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save videos to device | **True** or **False** | **False**      |
|post_count|Number of posts to scrape|**all** or **number**|**10**|
|media_type|Scrape only image or video or both |**image** or **video** or **both**|**both**|

#### Where to find link ⤵️

![MarineGEO circle logo](https://i.postimg.cc/MHVj2hGk/Capture12.jpg) 

### Response
```
{
    "image": [
        {
            "image_id": string,      // image id
            "user_id": string,       // IG id of user
            "username": string,      // IG username of user 
            "url": string,           //  IG url of video
            "caption": string,       // image caption
            "shortcode": string      // Image identifier
        }
        ],
        "video": [
        {
            "video_id": string,     // Video id 
            "user_id": string,      // IG Id of user
            "username": string,     // IG username if user
            "thumbnail": string,    // video thumbnail
            "url": string,          // video url 
            "caption": string,      // video caption 
            "shortcode": string     // video shortcode
        }
        ]
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_similar_posts(media_url="https://www.instagram.com/p/CX6wlqBP_L_/?utm_source=ig_web_copy_link",save_urls=True,save_to_device=True,post_count=30,media_type="image")
cli.close()
```
####
_________________________


### 12. get_story_timeline()
Scrapes stories from the timeline. Scrapes only latest stories. Some stories may not be available.
``` python
get_story_timeline(save_urls=False,save_to_device=False,story_count=10,media_type="both")
```
| Parameter     | Description       | Values    | Default Value     |
|---    |---    |---    |---    |
|save_urls|Save response to json file|**True** or **False**|**False**|
|save_to_device     | Save media to device | **True** or **False** | **False**      |
|story_count|Number of posts to scrape|**all** or **number**|**10**|
|media_type|Scrape only image or video or both |**image** or **video** or **both**|**both**|

### Response
```
{
    "image": [
            {
            "sid": string,            // Story id
            "username": string,       // Username of owner
            "user_id": int,           // Owner IG id
            "shortcode": string,      // Story identifier
            "url": string             // Story download url
        }
        ],
    "video": [
        {
            "sid": string,           // Video id
            "username": string,      // IG owner username
            "user_id": string,       // IG owner id
            "shortcode": string,     // Video identifier
            "thumbnail": string,     // Video thumbnail
            "url": string            // Video url
        }
    ]
}
```
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_story_timeline(save_urls=False,save_to_device=False,story_count=10,media_type="both")
cli.close()
```
####
_________________________

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/suyashjawale/InstagramCLI/blob/main/LICENSE)