from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_highlights(target_username="therock",save_urls=True,save_to_device=True,story_count=2,media_type="video")
print(data)
cli.close()