import requests
import pprint
import os
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List

class Project(BaseModel):
    abbreviation: Optional[str]
    defaultTeamImageUrl: Optional[str]
    description: Optional[str]
    id: Optional[str]
    lastUpdateTime: Optional[str]
    name: Optional[str]
    revision: Optional[int]
    state: Optional[str]
    url: Optional[str]
    web: Optional[str]
    visibility: Optional[str]

    def __repr__(self):
        return (
            f"Project(abbreviation={self.abbreviation}, defaultTeamImageUrl={self.defaultTeamImageUrl}, "
            f"description={self.description}, id={self.id}, lastUpdateTime={self.lastUpdateTime}, "
            f"name={self.name}, revision={self.revision}, state={self.state}, url={self.url}, "
            f"visibility={self.visibility})"
        )

    @classmethod
    def from_json(cls, json_data):
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
        
class WebApiTeam(BaseModel):
    '''
    ALL TEAMS 
    GET https://dev.azure.com/{organization}/_apis/teams?api-version=7.2-preview.3
    MY TEAMS
    GET https://dev.azure.com/{organization}/_apis/teams?api-version=7.2-preview.3

    '''
    description: Optional[str]
    id: Optional[str]
    identity: Optional[Any]
    identityUrl: Optional[str]
    name: Optional[str]
    projectId: Optional[str]
    projectName: Optional[str]
    url: Optional[str]

    def __repr__(self):
        return (
            f"WebApiTeam(description={self.description}, id={self.id}, identity={self.identity}, "
            f"identityUrl={self.identityUrl}, name={self.name}, projectId={self.projectId}, "
            f"projectName={self.projectName}, url={self.url})"
        )

    @classmethod
    def from_json(cls, json_data):
        return cls(
            description=json_data.get("description"),
            id=json_data.get("id"),
            identity=json_data.get("identity"),
            identityUrl=json_data.get("identityUrl"),
            name=json_data.get("name"),
            projectId=json_data.get("projectId"),
            projectName=json_data.get("projectName"),
            url=json_data.get("url"),
        )
    
#Team member
class IdentityRef(BaseModel):
    _links: Optional[Any]
    descriptor: Optional[str]
    directoryAlias: Optional[str]
    displayName: Optional[str]
    id: Optional[str]
    imageUrl: Optional[str]
    inactive: Optional[bool]
    isAadIdentity: Optional[bool]
    isContainer: Optional[bool]
    isDeletedInOrigin: Optional[bool]
    profileUrl: Optional[str]
    uniqueName: Optional[str]
    url: Optional[str]

    def to_dict(self):
        return {
            "id": self.id,
            "displayName": self.displayName,
            "imageUrl": self.imageUrl,
        }

    def __repr__(self):
        return (
            #f"IdentityRef(_links={self._links}, descriptor={self.descriptor}, directoryAlias={self.directoryAlias}, "
            f"displayName={self.displayName}, id={self.id}, imageUrl={self.imageUrl}, inactive={self.inactive}, "
            #f"isAadIdentity={self.isAadIdentity}, isContainer={self.isContainer}, isDeletedInOrigin={self.isDeletedInOrigin}, "
            f"profileUrl={self.profileUrl}, uniqueName={self.uniqueName}, url={self.url})"
        )

    @classmethod
    def from_json(cls, json_data):
        return cls(
            _links=json_data.get("_links"),
            descriptor=json_data.get("descriptor"),
            directoryAlias=json_data.get("directoryAlias"),
            displayName=json_data.get("displayName"),
            id=json_data.get("id"),
            imageUrl=json_data.get("imageUrl"),
            inactive=json_data.get("inactive"),
            isAadIdentity=json_data.get("isAadIdentity"),
            isContainer=json_data.get("isContainer"),
            isDeletedInOrigin=json_data.get("isDeletedInOrigin"),
            profileUrl=json_data.get("profileUrl"),
            uniqueName=json_data.get("uniqueName"),
            url=json_data.get("url"),
        )

class TeamMember(BaseModel):
    identity: Optional[IdentityRef]
    isTeamAdmin: Optional[bool]

    def to_dict(self):
        return {
            "isTeamAdmin": self.isTeamAdmin == True,
            "id": self.identity.id if self.identity else None,
            "displayName": self.identity.displayName if self.identity else None,
            "imageUrl": self.identity.imageUrl if self.identity else None,
        }

    def __repr__(self):
        return f"TeamMember(identity={self.identity}, isTeamAdmin={self.isTeamAdmin})"

    @classmethod
    def from_json(cls, json_data):
        return cls(
            identity=IdentityRef.from_json(json_data.get("identity")),
            isTeamAdmin=json_data.get("isTeamAdmin"),
        )
    
    def to_dict(self):
        return {
            "isTeamAdmin": self.isTeamAdmin == True,
            "id": self.identity.id,
            "displayName": self.identity.displayName,
            "imageUrl": self.identity.imageUrl,
        }

class WorkItem(BaseModel):
    _links: Optional[Any]
    commentVersionRef: Optional[Any]
    fields: Optional[Dict[str, Any]]
    id: Optional[int]
    relations: Optional[List[Any]]
    rev: Optional[int]
    url: Optional[str]
    organization: Optional[str] = None
    project: Optional[str] = None
    completedHours: Optional[float] = None
    title: Optional[str] = None
    state: Optional[str] = None

    def getDetails(self, headers):
        response = requests.get(self.url, headers=headers)
        fields = response.json().get("fields")
        self.completedHours = fields.get("Microsoft.VSTS.Scheduling.CompletedWork")
        self.title = fields.get("System.Title")
        self.state = fields.get("System.State")

    def __repr__(self):
        return (
            f"WorkItem(id={self.id}, url={self.url}, title={self.title}, state={self.state}, completedHours={self.completedHours})"
        )

    @classmethod
    def from_json(cls, json_data):
        return cls(
            _links=json_data.get("_links"),
            commentVersionRef=json_data.get("commentVersionRef"),
            fields=json_data.get("fields"),
            id=json_data.get("id"),
            relations=json_data.get("relations"),
            rev=json_data.get("rev"),
            url=json_data.get("url"),
        )