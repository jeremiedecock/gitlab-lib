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


    def make_issue(self, gitlab_project_id, title, labels, milestone_id, description):
        # https://docs.gitlab.com/ee/api/issues.html#new-issue

        title = urllib.parse.quote(title)              # urlencodé
        labels = urllib.parse.quote(labels)            # urlencodé
        description = urllib.parse.quote(description)  # urlencodé

        gitlab_request_url = f"{self.gitlab_host}/api/v4/projects/{gitlab_project_id}/issues?title={title}&labels={labels}&milestone_id={milestone_id}&description={description}"
        print(gitlab_request_url)

        resp = requests.post(gitlab_request_url, headers=self.request_header)

        if resp.status_code != 201:
            raise Exception("Error:" + resp.text)

        resp_dict = json.loads(resp.text)
        
        return resp_dict


    def update_issue(self, gitlab_project_id, gitlab_issue_iid, title=None, labels=None, milestone_id=None, description=None):
        # https://docs.gitlab.com/ee/api/issues.html#edit-issue

        request_params_list = []
        if title is not None:
            title = urllib.parse.quote(title)              # urlencodé
            request_params_list.append(f"title={title}")
        if labels is not None:
            labels = urllib.parse.quote(labels)            # urlencodé
            request_params_list.append(f"labels={labels}")
        if milestone_id is not None:
            request_params_list.append(f"milestone_id={milestone_id}")
        if description is not None:
            description = urllib.parse.quote(description)  # urlencodé
            request_params_list.append(f"description={description}")

        if len(request_params_list) > 0:
            request_params_str = "&".join(request_params_list)
            gitlab_request_url = f"{self.gitlab_host}/api/v4/projects/{gitlab_project_id}/issues/{gitlab_issue_iid}?{request_params_str}"
            print(gitlab_request_url)

            resp = requests.put(gitlab_request_url, headers=self.request_header)

            if resp.status_code != 200:
                raise Exception("Error:" + resp.text)

            resp_dict = json.loads(resp.text)

            return resp_dict

        else:
            raise ValueError("All parameters are set to None ; at least one parameter have to be set.")


    def update_issue_labels(self, gitlab_project_id, gitlab_issue_iid, remove_labels, add_labels):
        # https://docs.gitlab.com/ee/api/issues.html#edit-issue

        # REMOVE FORMER LABELS ##################

        request_params_str = f"remove_labels={urllib.parse.quote(remove_labels)}"            # urlencodé
        gitlab_request_url = f"{self.gitlab_host}/api/v4/projects/{gitlab_project_id}/issues/{gitlab_issue_iid}?{request_params_str}"
        print(gitlab_request_url)

        resp = requests.put(gitlab_request_url, headers=self.request_header)

        if resp.status_code != 200:
            raise Exception("Error:" + resp.text)

        resp_remove_dict = json.loads(resp.text)

        # ADD NEW LABELS ########################

        request_params_str = f"add_labels={urllib.parse.quote(add_labels)}"            # urlencodé
        gitlab_request_url = f"{self.gitlab_host}/api/v4/projects/{gitlab_project_id}/issues/{gitlab_issue_iid}?{request_params_str}"
        print(gitlab_request_url)

        resp = requests.put(gitlab_request_url, headers=self.request_header)

        if resp.status_code != 200:
            raise Exception("Error:" + resp.text)

        resp_add_dict = json.loads(resp.text)

        ###

        return resp_remove_dict, resp_add_dict

    
    def _gitlab_get_request(self, get_url):
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
        if resp.apparent_encoding.lower() not in ('utf-8', 'ascii'):
            raise Exception("Apparent_encoding error:", resp.apparent_encoding)

        #for issue_dict in json_list:
        #    if ("Ã©" in issue_dict["title"]) or ("â€™" in issue_dict["title"]) or ("Ã‰" in issue_dict["title"]) or ("Ã¢" in issue_dict["title"]): # Ã¨
        #        print("Encoding err:", issue_dict["id"], issue_dict["web_url"])

        return json_list, resp


    def gitlab_fetch_all_issues(self):
        issue_list = []

        url = f"{self.gitlab_host}/api/v4/issues?per_page=100&page=1&scope=all"

        json_list, resp = self._gitlab_get_request(url)
        issue_list.extend(json_list)

        num_pages = int(resp.headers['X-Total-Pages'])

        for page in range(2, num_pages+1):
            #print(".", end="", flush=True)
            print("page {}/{}".format(page, num_pages))

            url = f"{self.gitlab_host}/api/v4/issues?per_page=100&page={page}&scope=all"
            json_list, resp = self._gitlab_get_request(url)

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

            json_list, resp = self._gitlab_get_request(url)
            issue_list.extend(json_list)

            num_pages = int(resp.headers['X-Total-Pages'])

            for page in range(2, num_pages+1):
                print(f"page {page}/{num_pages}")

                url = f"{self.gitlab_host}/api/v4/projects/{project_id}/issues?per_page=100&page={page}&scope=all" + url_filters

                print(url)
                json_list, resp = self._gitlab_get_request(url)
                issue_list.extend(json_list)

        return issue_list