from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_reels(target_username="aashnahegde",save_urls=True,save_to_device=True,reel_count=3)
print(data)
cli.close()