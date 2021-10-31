from InstagramCLI import InstagramCLI
cli = InstagramCLI(username="", password="")
data= cli.get_comments(media_link="https://www.instagram.com/p/CVXI1Wfh9p3/?utm_source=ig_web_copy_link",save_comments=True,comment_count="all")
print(data)
cli.close()