from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="",hidden=False)
cli.get_similar_posts("https://www.instagram.com/p/CX3Y6PkphUF/?utm_source=ig_web_copy_link",save_urls=True,save_to_device=True,media_type="both",post_count=20)
print(data)
cli.close()