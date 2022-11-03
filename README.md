# InstagramCLI 
CLI tool made by reverse engineering Instagram API calls.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) 
#####
[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)   [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)   [![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-380/) [![Python 3.9](https://img.shields.io/badge/python-3.9-violet.svg)](https://www.python.org/downloads/release/python-390/) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-390/)
#### Checkout repo 
[![forthebadge made-with-python](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/suyashjawale/InstagramCLI) 

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install InstagramCLI.
```bash
pip install InstagramCLI
```

## Documentation and Usage
### 1. get_followers()
Get followers of particluar account.
```python
get_followers(username, save, optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|username |  string | Username of account to scrape     | --    | --    |
|save   | boolean | Save followers list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|count|**int** or **string**|Number of followers|**number** or **all**|**all**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**followers**|
|filename|**string**|Custom file name|Anything you want|**username_followers**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Example 
```python
from InstagramCLI import InstagramCLI
optimizations = {
    "count" : 24, // Must be a multiple of 12,
    "folder" : "custom_readme_demo", 
    "sub_folder" : "custom_sub_folder",
    "filename" : "anything_i_want",
    "timestamp_folder" : True,
    "timestamp_file" : True
}
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_followers(username="suyash.jawale", optimizations=optimizations)
```
####
_________________________

### 2. get_following()
Get following of particluar account.
```python
get_following(username, save, optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|username |  string | Username of account to scrape     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|count|**int** or **string**|Number of following|**number** or **all**|**all**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**following**|
|filename|**string**|Custom file name|Anything you want|**username_following**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Example 
```python
from InstagramCLI import InstagramCLI
optimizations = {
    "count" : 24, // Must be a multiple of 12,
    "folder" : "custom_readme_demo", 
    "sub_folder" : "custom_sub_folder",
    "filename" : "anything_i_want",
    "timestamp_folder" : True,
    "timestamp_file" : True
}
cli = InstagramCLI(username="your_username", password="your_password")
data= cli.get_following(username="suyash.jawale", optimizations=optimizations)
```
####
_________________________

### 3. get_posts()
Fetch post media and post metadata.
```python
get_posts(username,save,optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|username |  string | Username of account to scrape     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|raw_response|**boolean**|Response received from instagram|**True** or **False**|**False**|
|count|**int**|Count of posts|**number** or **all**|**24**|
|media_type|**string**|What to scrape photo or video|**photo** or **video** or **both**|**both**|
|save_photo|**boolean**|Save photo post|**True** or **False**|**False**|
|save_video|**boolean**|Save video post|**True** or **False**|**False**|
|save_video_thumbnail|**boolean**|Save thumbnail of video|**True** or **False**|**False**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**posts**|
|filename|**string**|Custom file name|Anything you want|**username_posts**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
optimizations = {
    "count" : 36, // Multiple of 12
    "save_photo" : True,
    "save_video" : True,
    "timestamp_folder" : True
}
data= cli.get_posts(username="instagram",optimizations=optimizations)
```
####
_________________________


### 4. get_reels()
Fetch reel videos and metadata.
```python
get_reels(username,save,optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|username |  string | Username of account to scrape     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|raw_response|**boolean**|Response received from instagram|**True** or **False**|**False**|
|count|**int**|Count of reels|**number** or **all**|**18**|
|save_video|**boolean**|Save video post|**True** or **False**|**False**|
|save_video_thumbnail|**boolean**|Save thumbnail of video|**True** or **False**|**False**|
|save_music|**boolean**|Save reel music|**True** or **False**|**False**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**reels**|
|filename|**string**|Custom file name|Anything you want|**username_reels**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
optimized = {
            "count": optimizations.get("count", 18),
            "save_video": optimizations.get("save_video", False),
            "save_video_thumbnail": optimizations.get("save_video_thumbnail", False),
            "save_music": optimizations.get("save_music", False),
            "timestamp_folder" : optimizations.get("timestamp_folder",False),
            "timestamp_file" : optimizations.get("timestamp_file",False)
    }
data= cli.get_reels(username="instagram",optimizations=optimized)
```
####
_________________________

### 5. get_comments()
Scrape comments for any media.
```
get_comments(shortcode,save,optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|shortcode |  string | Post id     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|raw_response|**boolean**|Response received from instagram|**True** or **False**|**False**|
|count|**int**|Count of posts|**number** or **all**|**60**|
|child_comments|**string**|Comments of a comment|**True** or **False**|**False**|
|folder|**string**|Custom folder name|Anything you want|**shortcode**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**comments**|
|filename|**string**|Custom file name|Anything you want|**shortcode_comments**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to file|**True** or **False**|**False**|


#### Where to find shortcode ⤵️
[![Screenshot-22.jpg](https://i.postimg.cc/jjKmXC2v/Screenshot-22.jpg)](https://postimg.cc/cv9F1xQ8)

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
optimizations = {
    "count" : 25,
    "child_comments" : True, // This operations requires requesting to server. 
    "timestamp_folder" : True
}
data= cli.get_comments(shortcode="CkP5nARPxSg",optimizations=optimizations)
```
####
_________________________


### 6. get_story()
Download stories and metadata for particular account.
```
get_story(username,save,optimizations )
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|username |  string | Username of account to scrape     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|raw_response|**boolean**|Response received from instagram|**True** or **False**|**False**|
|media_type|**string**|What to scrape photo or video|**photo** or **video** or **both**|**both**|
|save_photo|**boolean**|Save photo post|**True** or **False**|**False**|
|save_video|**boolean**|Save video post|**True** or **False**|**False**|
|save_video_thumbnail|**boolean**|Save thumbnail of video|**True** or **False**|**False**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**story**|
|filename|**string**|Custom file name|Anything you want|**username_story**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
optimizations = {
    "raw_response":True,
    "media_type" : "video",
    "save_photo" : True,
    "save_video": True
}
data= cli.get_story(username="sakshimalikk",optimizations=optimizations)
```
####
_________________________


### 7. get_highlights()
Scrape account highlights media and metadata
```
get_highlights(username,save,optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|username |  string | Username of account to scrape     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|raw_response|**boolean**|Response received from instagram|**True** or **False**|**False**|
|media_type|**string**|What to scrape photo or video|**photo** or **video** or **both**|**both**|
|highlight_count|**string** or **number**|Count of highlights|**all** or **number**|**4**|
|story_count|**string** or **number**|Count of story|**all** or **number**|**10**|
|save_photo|**boolean**|Save photo post|**True** or **False**|**False**|
|save_video|**boolean**|Save video post|**True** or **False**|**False**|
|save_video_thumbnail|**boolean**|Save thumbnail of video|**True** or **False**|**False**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**highlights**|
|filename|**string**|Custom file name|Anything you want|**username_highlights**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="your_username", password="your_password")
optimizations = {
    "save_photo" : True,
    "save_video" : True,
    "highlight_count" : 5,
    "story_count" : 20,
}
data= cli.get_highlights(username="rashmika_mandanna",optimizations=optimizations)

```
####
_________________________


### 8. get_music_reels()
Find reels with same music.
```
get_music_reels(music_id,save,optimizations)
```
| Parameter |   Type | Description       | Values    | Default Value     |
|---    |--- |---   |---    |---    |
|music_id |  string | Id of music     | --    | --    |
|save   | boolean | Save following list to json file | **True** or **False** | **True**|
|**optimizations**   | dictionary | Additional params for nerds | shown below | |

##### Optimizations
#
|Param|Type|Description|Value|Default|
|--- |--- |--- |--- |--- |
|raw_response|**boolean**|Response received from instagram|**True** or **False**|**False**|
|count|**int**|Count of reels|**number** or **all**|**18**|
|save_video|**boolean**|Save video post|**True** or **False**|**False**|
|save_video_thumbnail|**boolean**|Save thumbnail of video|**True** or **False**|**False**|
|save_music|**boolean**|Save reel music|**True** or **False**|**False**|
|folder|**string**|Custom folder name|Anything you want|**username**|
|sub_folder|**string**|Custom sub folder name|Anything you want|**reels**|
|filename|**string**|Custom file name|Anything you want|**username_reels**|
|timestamp_folder|**boolean**|Append current date & time to folder|**True** or **False**|**False**|
|timestamp_file|**boolean**|Append current date & time to folder|**True** or **False**|**False**|

#### Where to find music_id ⤵️
Step 1 - Clik on mysic name of reel
[![step1.jpg](https://i.postimg.cc/Hxf25VVW/step1.jpg)](https://postimg.cc/PpQYnfW0)
Step 2 - Copy the music id
[![step2.jpg](https://i.postimg.cc/dQ8j7Qm6/step2.jpg)](https://postimg.cc/kDgbzmHR)
#### Example 
```python
from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
optimizations = {
    "count" : 40,
    "save_video" : True
}
data= cli.get_similar_reels(music_id="1184871695410444",optimizations=optimizations)
```
####
_________________________

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/suyashjawale/InstagramCLI/blob/main/LICENSE)
