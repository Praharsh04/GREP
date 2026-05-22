from bs4 import BeautifulSoup

with open("sample_q_tc_raw.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Find the first post. In phpBB (which GRE Prep Club seems to be based on), it's often .post
posts = soup.find_all("div", class_="post")
for i, post in enumerate(posts):
    print(f"--- Post {i} ---")
    content = post.find("div", class_="content")
    if content:
        print(content.text.strip())
    else:
        # Try finding postbody
        postbody = post.find("div", class_="postbody")
        if postbody:
            print(postbody.text.strip())
            
# If not found, look for any div that might contain the question
if not posts:
    print("No .post divs found, looking for .postbody")
    postbodies = soup.find_all("div", class_="postbody")
    for i, pb in enumerate(postbodies):
        print(f"--- Postbody {i} ---")
        print(pb.text.strip()[:500])
