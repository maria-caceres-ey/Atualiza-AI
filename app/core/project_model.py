#project_model
import requests

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime
import pandas as pd

from devops_models import WorkItem, IdentityRef

class Project(BaseModel):
    #Tambien es un WorkItem pero es un epic 
    abbreviation: Optional[str]
    defaultTeamImageUrl: Optional[str]
    description: Optional[str]
    id: Optional[str]
    lastUpdateTime: Optional[datetime]
    name: Optional[str]
    revision: Optional[int]
    state: Optional[str]
    url: Optional[str]
    web: Optional[str]
    visibility: Optional[str]


    root: Optional[WorkItem] = Field(default_factory=WorkItem)#Guarda el workitem raiz del proyecto
    childs: Optional[List[WorkItem]] = Field(default_factory=list)#Guarda descendientes directos
    tasks: Optional[List[WorkItem]] = Field(default_factory=list)#Guarda las tasks de los niveles mas bajos
    teamMembers: Optional[Dict[str,IdentityRef]] = Field(default_factory=list)#Guarda los miembros del equipo
    #descendientes: Optional[List[WorkItem]] = Field(default_factory=list)#Guarda todos los descendientes

    def __repr__(self):
        return (
            f"Project(abbreviation={self.abbreviation}, defaultTeamImageUrl={self.defaultTeamImageUrl}, "
            f"description={self.description}, id={self.id}, lastUpdateTime={self.lastUpdateTime}, "
            f"name={self.name}, revision={self.revision}, state={self.state}, url={self.url}, "
            f"visibility={self.visibility})"
        )

    @classmethod
    def from_json(cls, json_data):
        lastUpdateTime = json_data.get("lastUpdateTime")
        try:
            lastUpdateTime = datetime.strptime(lastUpdateTime, "%Y-%m-%dT%H:%M:%S.%fZ") if '.' in lastUpdateTime else datetime.strptime(lastUpdateTime, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            lastUpdateTime = None
        else:
            lastUpdateTime = None

        return cls(
            abbreviation=json_data.get("abbreviation"),
            defaultTeamImageUrl=json_data.get("defaultTeamImageUrl"),
            description=json_data.get("description"),
            id=json_data.get("id"),
            lastUpdateTime=json_data.get("lastUpdateTime"),
            name=json_data.get("name"),
            revision=json_data.get("revision"),
            state=json_data.get("state"),
            url=json_data.get("url"),
            visibility=json_data.get("visibility"),
            web=json_data.get("web"),
        )
    
    @classmethod
    def project_from_workitem(cls, json_data):
        fields = json_data.get("fields", {})
        return cls(
            abbreviation=json_data.get("abbreviation"),
            defaultTeamImageUrl=json_data.get("defaultTeamImageUrl"),

            id=str(json_data.get("id")) if json_data.get("id") else None,
            name=fields.get("System.Title"),
            description=fields.get("System.Description"),
            lastUpdateTime=datetime.strptime(fields.get("System.ChangedDate"), "%Y-%m-%dT%H:%M:%S.%fZ") if fields.get("System.ChangedDate") and '.' in fields.get("System.ChangedDate") else datetime.strptime(fields.get("System.ChangedDate"), "%Y-%m-%dT%H:%M:%SZ") if fields.get("System.ChangedDate") else None,
            state=fields.get("System.State"),
            revision=json_data.get("rev"),
            url=json_data.get("url"),

            visibility=json_data.get("visibility"),
            web=json_data.get("web"),
        )
    
    def getTasks(self, headers, azure_path="https://dev.azure.com/FSO-DnA-Devops", azure_project_id="e4005fd0-7b95-4391-8486-c4b21c935b2e"):
        if len(self.tasks) > 0:#si ya se obtuvieron las tareas
            return self.tasks
        
        if not self.root or not len(self.root.childs):#si no fue por los niveles
            self.getRelationships(headers=headers,azure_path=azure_path,azure_project_id=azure_project_id)
        self.tasks = []

        #Recorre el arbol hasta las hojas
        def dfs(node):
            if node.childs:
                for child in node.childs:
                    dfs(child)
            else:
                self.tasks.append(node)#Don,t know if i´ll work
        dfs(self.root)
        return self.tasks
    
    def getTeamMembers(self, headers, azure_path="https://dev.azure.com/FSO-DnA-Devops", azure_project_id="e4005fd0-7b95-4391-8486-c4b21c935b2e"):
        if len(self.teamMembers) > 0:
            return self.teamMembers
        
        if not self.root or not len(self.root.childs):#si no fue por los niveles
            self.getRelationships(headers=headers,azure_path=azure_path,azure_project_id=azure_project_id)

        def dfs(node):
            if node.childs:
                for child in node.childs:
                    dfs(child)
            else:
                member = node.assignedTo
                self.teamMember[member.id] = member

        dfs(self.root)
        return List[self.teamMembers]

    def getRelationships(self, headers, azure_path="https://dev.azure.com/FSO-DnA-Devops", azure_project_id="e4005fd0-7b95-4391-8486-c4b21c935b2e"):
        if not self.root:
            self.root = WorkItem()
            self.root.id = self.id

            #Obtiene sus hijos y sus descendientes
            #there are no more than 5 levels but just in case
            self.root.getInfo(10,headers=headers,azure_path=azure_path,azure_project_id=azure_project_id)

    