from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_following(target_username="instagram", save_to_file=True)
print(data)
cli.close()