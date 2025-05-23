#app/core/devops_models.py
import requests
import pprint
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

import os
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List
from datetime import datetime



class Project(BaseModel):
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
            lastUpdateTime = datetime.strptime(lastUpdateTime, "%Y-%m-%dT%H:%M:%SZ")
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
        if json_data is None:
            return cls(
                _links=None,
                descriptor="",
                directoryAlias="",
                displayName="",
                id="",
                imageUrl="",
                inactive=False,
                isAadIdentity=False,
                isContainer=False,
                isDeletedInOrigin=False,
                profileUrl="",
                uniqueName="",
                url=""
            )
        return cls(
            _links=json_data.get("_links", None),
            descriptor=json_data.get("descriptor", ""),
            directoryAlias=json_data.get("directoryAlias", ""),
            displayName=json_data.get("displayName", ""),
            id=json_data.get("id", ""),
            imageUrl=json_data.get("imageUrl", ""),
            inactive=json_data.get("inactive", False),
            isAadIdentity=json_data.get("isAadIdentity", False),
            isContainer=json_data.get("isContainer", False),
            isDeletedInOrigin=json_data.get("isDeletedInOrigin", False),
            profileUrl=json_data.get("profileUrl", ""),
            uniqueName=json_data.get("uniqueName", ""),
            url=json_data.get("url", ""),
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
    assignedTo: Optional[IdentityRef] = None
    target_date: Optional[datetime] = None

    

    def __init__(self, **data):
        super().__init__(**data)
        fields = data.get("fields", {})
        if fields != {}:
            self.parseFields(fields)

    def parseFields(self, fields):
        self.completedHours = fields.get("Microsoft.VSTS.Scheduling.CompletedWork", None)
        self.title = fields.get("System.Title", None)
        self.state = fields.get("System.State", None)
        self.assignedTo = IdentityRef.from_json(fields.get("System.AssignedTo", {})) if fields.get("System.AssignedTo") else None
        target_date_str = fields.get("Microsoft.VSTS.Scheduling.TargetDate", None)
        if target_date_str:
            try:
                self.target_date = datetime.strptime(target_date_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                self.target_date = None
        else:
            self.target_date = None

    def getDetails(self, headers):
        response = requests.get(self.url, headers=headers)
        fields = response.json().get("fields")
        self.parseFields(fields)

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

#st.dataframe(filter_dataframe(df))
class WorkItemQueryResult(BaseModel):
    workItems: List[WorkItem]
    def to_dataframe(self, column_order: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Store the work items as a pandas DataFrame with an optional column order.

        Args:
            column_order (Optional[List[str]]): List of column names in the desired order.

        Returns:
            pd.DataFrame: A DataFrame containing the work items.
        """
        if not column_order:
            column_order = [
                "title",#
                "id",#
                "state",#
                "completedHours",#
                "assignedTo",#
                "target_date",#
                "url"#
            ]
            #Falta rev
        df = pd.DataFrame([item.model_dump() for item in self.workItems])
        if column_order:
            df = df[[col for col in column_order if col in df.columns]]
        return df
    
    
    @classmethod
    def from_json_list(cls, json_list):
        """
        Create a WorkItemQueryResult instance from a list of JSON objects.
        """
        work_items = [WorkItem.from_json(item) for item in json_list]
        return cls(workItems=work_items)

    @classmethod
    def from_json(cls, json_data):
        return cls(
            workItems=[WorkItem.from_json(item) for item in json_data.get("workItems", [])],
        )

    def __repr__(self):
        return f"WorkItemQueryResult(count={len(self.workItems)}, workItems={self.workItems})"
    
