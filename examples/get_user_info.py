from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_user_info(target_username="usnjsi77",save_to_device=True)
print(data)
cli.close()