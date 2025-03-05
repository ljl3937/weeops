from metagpt.roles.role import Role
from actions.jenkins_action import JenkinsAction, CreateJenkinsJob, BuildJenkinsJob, GetJenkinsJobInfo, StopJenkinsJob, DeleteJenkinsJob

class JenkinsRole(Role):
    def __init__(self, jenkins_url, username, password):
        super().__init__()
        self.jenkins_action = JenkinsAction(jenkins_url, username, password)
        self.actions = [
            CreateJenkinsJob(self.jenkins_action),
            BuildJenkinsJob(self.jenkins_action),
            GetJenkinsJobInfo(self.jenkins_action),
            StopJenkinsJob(self.jenkins_action),
            DeleteJenkinsJob(self.jenkins_action)
        ]
