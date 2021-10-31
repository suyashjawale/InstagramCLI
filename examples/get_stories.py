from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="",hidden=False)
data= cli.get_stories(target_username="cbum",save_urls=True,save_to_device=False,story_count="all")
print(data)
cli.close()