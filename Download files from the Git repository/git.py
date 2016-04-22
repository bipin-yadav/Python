from github import Github
import getpass
import base64

def get_sha_for_tag(repository, tag):
    """
    Returns a commit object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha


def download_directory(repository, sha, server_path):
    """
    Download all contents at server_path with commit tag sha in 
    the repository.
    """
    contents = repository.get_dir_contents(server_path, ref=sha)

    for content in contents:
        print "Processing %s" % content.path
        if content.type == 'dir':
            download_directory(repository, sha, content.path)
        else:
            try:
                path = content.path
                print path
                file_content = repository.get_contents(path, ref=sha)
                file_data = base64.b64decode(file_content.content)
                file_out = open(content.name, "wb")
                file_out.write(file_data)
                file_out.close()
            except (Exception, IOError) as exc:
                print Exception
                print exc

github = Github("bipin-yadav", "gh6293@Wipro")
user = github.get_user()
print user
repository = user.get_repo('bipin-yadav.github.io')
print repository

branch_or_tag_to_download = raw_input("Branch or tag to download: ")
sha = get_sha_for_tag(repository, branch_or_tag_to_download)

directory_to_download = raw_input("Directory to download: ")
download_directory(repository, sha, directory_to_download)
