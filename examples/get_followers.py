from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_followers(target_username="", save_to_file=True)
print(data)
cli.close()