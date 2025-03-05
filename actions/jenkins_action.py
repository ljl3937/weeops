import jenkins
from metagpt.actions import Action

class JenkinsAction:
    def __init__(self, jenkins_url, username, password):
        self.server = jenkins.Jenkins(jenkins_url, username=username, password=password)

    def create_job(self, name, config_xml):
        """创建一个新的Jenkins Job"""
        self.server.create_job(name, config_xml)

    def build_job(self, name):
        """构建一个Jenkins Job"""
        self.server.build_job(name)

    def get_job_info(self, name):
        """获取Jenkins Job的信息"""
        return self.server.get_job_info(name)

    def stop_job(self, name, number):
        """停止一个正在运行的Jenkins Job"""
        self.server.stop_build(name, number)

    def delete_job(self, name):
        """删除一个Jenkins Job"""
        self.server.delete_job(name)

class CreateJenkinsJob(Action):
    def __init__(self, jenkins_action):
        self.jenkins_action = jenkins_action

    async def run(self, name, config_xml):
        """创建一个新的Jenkins Job"""
        self.jenkins_action.create_job(name, config_xml)

class BuildJenkinsJob(Action):
    def __init__(self, jenkins_action):
        self.jenkins_action = jenkins_action

    async def run(self, name):
        """构建一个Jenkins Job"""
        self.jenkins_action.build_job(name)

class GetJenkinsJobInfo(Action):
    def __init__(self, jenkins_action):
        self.jenkins_action = jenkins_action

    async def run(self, name):
        """获取Jenkins Job的信息"""
        return self.jenkins_action.get_job_info(name)

class StopJenkinsJob(Action):
    def __init__(self, jenkins_action):
        self.jenkins_action = jenkins_action

    async def run(self, name, number):
        """停止一个正在运行的Jenkins Job"""
        self.jenkins_action.stop_job(name, number)

class DeleteJenkinsJob(Action):
    def __init__(self, jenkins_action):
        self.jenkins_action = jenkins_action

    async def run(self, name):
        """删除一个Jenkins Job"""
        self.jenkins_action.delete_job(name)
