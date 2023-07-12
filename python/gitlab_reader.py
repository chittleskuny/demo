# -*- coding: utf-8 -*-

import json
import logging
import requests


class DemoGitLabNamespace(object):
    def __init__(self, namespace):
        self.id = namespace['id']
        self.name = namespace['name']
        self.path = namespace['path']
        self.kind = namespace['kind']
        self.full_path = namespace['full_path']
        self.parent_id = namespace['parent_id']
        self.avatar_url = namespace['avatar_url']
        self.web_url = namespace['web_url']


    def __str__(self):
        return self.name 


class DemoGitLabGroup(object):
    def __init__(self, group):
        self.id = group['id']
        self.name = group['name']
        self.path = group['path']
        self.description = group['description']
        self.visibility = group['visibility']
        self.share_with_group_lock = group['share_with_group_lock']
        self.require_two_factor_authentication = group['require_two_factor_authentication']
        self.two_factor_grace_period = group['two_factor_grace_period']
        self.project_creation_level = group['project_creation_level']
        self.auto_devops_enabled = group['auto_devops_enabled']
        self.subgroup_creation_level = group['subgroup_creation_level']
        self.emails_disabled = group['emails_disabled']
        self.mentions_disabled = group['mentions_disabled']
        self.lfs_enabled = group['lfs_enabled']
        self.default_branch_protection = group['default_branch_protection']
        self.avatar_url = group['avatar_url']
        self.web_url = group['web_url']
        self.request_access_enabled = group['request_access_enabled']
        self.full_name = group['full_name']
        self.full_path = group['full_path']
        self.parent_id = group['parent_id']
        self.created_at = group['created_at']

        
    def __str__(self):
        return self.name


class DemoGitLabProject(object):
    def __init__(self, project):
        self.id = project['id']
        self.description = project['description']
        self.name = project['name']
        self.name_with_namespace = project['name_with_namespace']
        self.path = project['path']
        self.path_with_namespace = project['path_with_namespace']
        self.created_at = project['created_at']
        self.default_branch = project['default_branch']
        self.tag_list = project['tag_list']
        self.topics = project['topics']
        self.ssh_url_to_repo = project['ssh_url_to_repo']
        self.http_url_to_repo = project['http_url_to_repo']
        self.web_url = project['web_url']
        self.readme_url = project['readme_url']
        self.avatar_url = project['avatar_url']
        self.forks_count = project['forks_count']
        self.star_count = project['star_count']
        self.last_activity_at = project['last_activity_at']
        self.namespace = DemoGitLabNamespace(project['namespace'])


    def __str__(self):
        return self.name


class DemoGitLabCommit(object):
    def __init__(self, commit):
        self.author_email = commit['author_email']
        self.author_name = commit['author_name']
        self.authored_date = commit['authored_date']
        self.committed_date = commit['committed_date']
        self.committer_email = commit['committer_email']
        self.committer_name = commit['committer_name']
        self.id = commit['id']
        self.short_id = commit['short_id']
        self.title = commit['title']
        self.message = commit['message']
        self.parent_ids = commit['parent_ids']


    def __str__(self):
        return self.title


class DemoGitLabBranch(object):
    def __init__(self, branch):
        self.name = branch['name']
        self.merged = branch['merged']
        self.protected = branch['protected']
        self.developers_can_push = branch['developers_can_push']
        self.developers_can_merge = branch['developers_can_merge']
        self.can_push = branch['can_push']
        self.web_url = branch['web_url']
        self.commit = DemoGitLabCommit(branch['commit'])


    def __str__(self):
        return self.name


class DemoGitLabReader(object):
    def __init__(self, url, private_token):
        self.url = url
        self.private_token = private_token
        
        self.session = requests.Session()
        self.session.get(url)


    def close(self):
        self.session.close()


    def get_groups(self):
        groups = []
        
        url = self.url + '''
            /api/v4/groups
            ?private_token=%s
            &order_by=name
            &sort=asc
            &per_page=30
        '''.replace('\n', '').replace(' ', '') % (
            self.private_token,
        )
        headers = self.session.head(url).headers
        total = int(headers['X-Total'])
        total_pages = int(headers['X-Total-Pages'])

        # 逐页请求
        for page in range(1, total_pages + 1):
            
            cur_url = url + '&page=%d' % page
            cur_groups_text = self.session.get(cur_url).text
            cur_groups_json = json.loads(cur_groups_text)
            
            for cur_group_json in cur_groups_json:
                cur_group = DemoGitLabGroup(cur_group_json)
                groups.append(cur_group)
        
        return groups


    def get_group_by_name(self, group_name):
        groups = self.get_groups()
        for group in groups:
            if group.name == group_name:
                return group
        
        return None


    def get_projects(self):
        projects = []
        
        url = self.url + '''
            /api/v4/projects
            ?private_token=%s
            &order_by=name
            &sort=asc
            &per_page=30
        '''.replace('\n', '').replace(' ', '') % (
            self.private_token,
        )
        headers = self.session.head(url).headers
        total = int(headers['X-Total'])
        total_pages = int(headers['X-Total-Pages'])

        # 逐页请求
        for page in range(1, total_pages + 1):
            
            cur_url = url + '&page=%d' % page
            cur_projects_text = self.session.get(cur_url).text
            cur_projects_json = json.loads(cur_projects_text)
            
            for cur_project_json in cur_projects_json:
                cur_project = DemoGitLabProject(cur_project_json)
                projects.append(cur_project)
            
        return projects

    
    def get_project_by_name(self, project_name):
        projects = self.get_projects()
        for project in projects:
            if project.name == project_name:
                return project

        return None
    
    
    def get_group_projects(self, group):
        projects = []
        
        url = self.url + '''
            /api/v4/groups/%d/projects
            ?private_token=%s
            &order_by=name
            &sort=asc
            &per_page=30
        '''.replace('\n', '').replace(' ', '') % (
            group.id,
            self.private_token,
        )
        headers = self.session.head(url).headers
        total = int(headers['X-Total'])
        total_pages = int(headers['X-Total-Pages'])

        # 逐页请求
        for page in range(1, total_pages + 1):
            
            cur_url = url + '&page=%d' % page
            cur_projects_text = self.session.get(cur_url).text
            cur_projects_json = json.loads(cur_projects_text)
            
            for cur_project_json in cur_projects_json:
                cur_project = DemoGitLabProject(cur_project_json)
                projects.append(cur_project)
            
        return projects


    def get_group_project_by_name(self, group_name, project_name):
        group = self.get_group_by_name(group_name)
        
        if group is not None:
            projects = self.get_group_projects(group)
            
            for project in projects:
                if project.name == project_name:
                    return (group, project)
            
            return (group, None)    
    
        return (None, None)
    
    
    def get_project_branch_by_name(self, project_name, branch_name):
        project = self.get_project_by_name(project_name)
        
        if project is not None:
            
            url = self.url + '''
                /api/v4/projects/%d/repository/branches/%s
                ?private_token=%s
            '''.replace('\n', '').replace(' ', '') % (
                project.id,
                branch_name,
                self.private_token,
            )
            branch_text = self.session.get(url).text
            branch_json = json.loads(branch_text)
            if 'message' in branch_json and branch_json['message'] == '404 Branch Not Found':
                return None

            branch = DemoGitLabBranch(branch_json)

            return branch
        
        return None


    def get_group_project_branch_by_name(self, group_name, project_name, branch_name):
        (group, project) = self.get_group_project_by_name(group_name, project_name)
        
        if (group is not None) and (project is not None):
        
            url = self.url + '''
                /api/v4/projects/%d/repository/branches/%s
                ?private_token=%s
            '''.replace('\n', '').replace(' ', '') % (
                project.id,
                branch_name,
                self.private_token,
            )
            branch_text = self.session.get(url).text
            branch_json = json.loads(branch_text)
            if 'message' in branch_json and branch_json['message'] == '404 Branch Not Found':
                return None
            
            branch = DemoGitLabBranch(branch_json)

            return branch
        
        return None

    
if __name__ == '__main__':
    gitlab_reader = DemoGitLabReader('http://127.0.0.1', 'chittleskuny')
    gitlab_reader.close()
