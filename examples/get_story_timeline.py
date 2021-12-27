from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_story_timeline(save_urls=True,save_to_device=False,story_count=10,media_type="image")
print(data)
cli.close()