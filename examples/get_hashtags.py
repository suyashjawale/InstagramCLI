from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_hashtags(hashtag_name="bike",save_urls=True,save_to_device=True,tag_count=5,hashtag_type="top",media_type="image")
print(data)
data= cli.get_hashtags(hashtag_name="bike",save_urls=True,save_to_device=True,tag_count=5,hashtag_type="recent",media_type="video")
print(data)
cli.close()