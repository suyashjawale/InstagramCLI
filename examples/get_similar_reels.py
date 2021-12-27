from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_similar_reels(reel_source="https://www.instagram.com/reel/CX03x8vFPgk/?utm_source=ig_web_copy_link",save_urls=True,save_to_device=False,reel_count=500,save_music=True)
print(data)
cli.close()