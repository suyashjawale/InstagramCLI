from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_stories(target_username="cbum",save_urls=True,save_to_device=False,story_count="all",media_type="image")
print(data)
cli.close()
