from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_posts(target_username="akshaykumar",save_urls=True,save_to_device=True,post_count=5,media_type="image")
print(data)
cli.close()