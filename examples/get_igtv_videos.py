from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_igtv_videos(target_username="rvcjinsta",save_urls=True,save_to_device=True,igtv_count=2,mode="deep")
print(data)
cli.close()