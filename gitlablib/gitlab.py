#################################################################
# Install the Python requests library: pip install requests
# http://docs.python-requests.org/en/master/user/quickstart/
#################################################################

import requests
import json
import urllib


class GitLab:

    def __init__(self, api_token, gitlab_host):
        self.api_token = api_token
        self.gitlab_host = gitlab_host


    @property
    def request_header(self):
        header_dict = {
            "PRIVATE-TOKEN": self.api_token
        }
        return header_dict


    def make_issue(self, project_id, title, labels, milestone_id, description):
        # https://docs.gitlab.com/ee/api/issues.html#new-issue
        #
        # dict_keys(['id', 'iid', 'project_id', 'title', 'description', 'state', 'created_at', 'updated_at', 'closed_at', 'closed_by', 'labels', 'milestone', 'assignees', 'author', 'type', 'assignee', 'user_notes_count', 'merge_requests_count', 'upvotes', 'downvotes', 'due_date', 'confidential', 'discussion_locked', 'issue_type', 'web_url', 'time_stats', 'task_completion_status', 'blocking_issues_count', 'has_tasks', 'task_status', '_links', 'references', 'moved_to_id', 'service_desk_reply_to'])

        def post_request(post_url):
            resp = requests.post(post_url, headers=self.request_header)

            if resp.status_code != 201:
                raise Exception("Error:" + resp.text)

            json_dict = json.loads(resp.text)
            return json_dict

        title = urllib.parse.quote(title)              # urlencodé
        labels = urllib.parse.quote(labels)            # urlencodé
        description = urllib.parse.quote(description)  # urlencodé

        gitlab_request_url = f"{self.gitlab_host}/api/v4/projects/{project_id}/issues?title={title}&labels={labels}&milestone_id={milestone_id}&description={description}"
        print(gitlab_request_url)

        resp_dict = post_request(gitlab_request_url)
        
        return resp_dict


    def update_issue(self):
        pass

    
    def gitlab_get_request(self, get_url):
        """
        https://docs.gitlab.com/ee/api/issues.html

        Parameters
        ----------
        get_url : [type]
            [description]

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        Exception
            [description]
        Exception
            [description]
        Exception
            [description]
        """
        resp = requests.get(get_url, headers=self.request_header)

        json_list = json.loads(resp.text)
        if resp.status_code != 200:
            raise Exception("Error:" + resp.text)
        if resp.encoding is not None and resp.encoding.lower() != 'utf-8':
            raise Exception("Encoding error:", resp.encoding)
        if resp.apparent_encoding.lower() != 'utf-8':
            raise Exception("Apparent_encoding error:", resp.apparent_encoding)

        #for issue_dict in json_list:
        #    if ("Ã©" in issue_dict["title"]) or ("â€™" in issue_dict["title"]) or ("Ã‰" in issue_dict["title"]) or ("Ã¢" in issue_dict["title"]): # Ã¨
        #        print("Encoding err:", issue_dict["id"], issue_dict["web_url"])

        return json_list, resp


    def gitlab_fetch_all_issues(self):
        issue_list = []

        url = f"{self.gitlab_host}/api/v4/issues?per_page=100&page=1&scope=all"

        json_list, resp = self.gitlab_get_request(url)
        issue_list.extend(json_list)

        num_pages = int(resp.headers['X-Total-Pages'])

        for page in range(2, num_pages+1):
            #print(".", end="", flush=True)
            print("page {}/{}".format(page, num_pages))

            url = f"{self.gitlab_host}/api/v4/issues?per_page=100&page={page}&scope=all"
            json_list, resp = self.gitlab_get_request(url)

            issue_list.extend(json_list)

        return issue_list


    def gitlab_fetch_selected_issues(self, project_iid_list):
        iid_dict = {}
        for project_id, iid in project_iid_list:
            if project_id not in iid_dict:
                iid_dict[project_id] = []
            iid_dict[project_id].append(iid)

        issue_list = []

        # Group requests per project id
        for project_id, iid_list in iid_dict.items():
            url_filters = "".join([f"&iids[]={iid}" for iid in iid_list])
            url = f"{self.gitlab_host}/api/v4/projects/{project_id}/issues?per_page=100&page=1&scope=all" + url_filters

            json_list, resp = self.gitlab_get_request(url)
            issue_list.extend(json_list)

            num_pages = int(resp.headers['X-Total-Pages'])

            for page in range(2, num_pages+1):
                print(f"page {page}/{num_pages}")

                url = f"{self.gitlab_host}/api/v4/projects/{project_id}/issues?per_page=100&page={page}&scope=all" + url_filters

                print(url)
                json_list, resp = self.gitlab_get_request(url)
                issue_list.extend(json_list)

        return issue_list