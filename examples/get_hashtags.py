from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_hashtags(hashtag_name="bike",save_urls=True,save_to_device=True,tag_count=5,hashtag_type="top")
print(data)
data= cli.get_hashtags(hashtag_name="bike",save_urls=True,save_to_device=True,tag_count=5,hashtag_type="recent")
print(data)
cli.close()