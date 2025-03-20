import requests
import pprint
import os

class Project:
    def __init__(self, abbreviation, defaultTeamImageUrl, description, id, lastUpdateTime, name, revision, state, url, visibility):
        self.abbreviation = abbreviation
        self.defaultTeamImageUrl = defaultTeamImageUrl
        self.description = description
        self.id = id
        self.lastUpdateTime = lastUpdateTime
        self.name = name
        self.revision = revision
        self.state = state
        self.url = url
        self.visibility = visibility

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
        )
    
class WebApiTeam:
    '''
    ALL TEAMS 
    GET https://dev.azure.com/{organization}/_apis/teams?api-version=7.2-preview.3
    MY TEAMS
    GET https://dev.azure.com/{organization}/_apis/teams?api-version=7.2-preview.3

    '''
    def __init__(self, description, id, identity, identityUrl, name, projectId, projectName, url):
        self.description = description
        self.id = id
        self.identity = identity
        self.identityUrl = identityUrl
        self.name = name
        self.projectId = projectId
        self.projectName = projectName
        self.url = url

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
class IdentityRef:
    def __init__(self, _links, descriptor, directoryAlias, displayName, id, imageUrl, inactive, isAadIdentity, isContainer, isDeletedInOrigin, profileUrl, uniqueName, url):
        self._links = _links
        self.descriptor = descriptor
        self.directoryAlias = directoryAlias
        self.displayName = displayName
        self.id = id
        self.imageUrl = imageUrl
        self.inactive = inactive
        self.isAadIdentity = isAadIdentity
        self.isContainer = isContainer
        self.isDeletedInOrigin = isDeletedInOrigin
        self.profileUrl = profileUrl
        self.uniqueName = uniqueName
        self.url = url

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
    
    def to_dict(self):
        return {
            "id": self.id,
            "displayName": self.displayName,
            "imageUrl": self.imageUrl,
        }

class TeamMember:
    def __init__(self, identity, isTeamAdmin):
        self.identity = identity
        self.isTeamAdmin = isTeamAdmin

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

class WorkItem:
    def __init__(self, _links, commentVersionRef, fields, id, relations, rev, url, organization=None, project=None):
        self._links = _links
        self.commentVersionRef = commentVersionRef
        self.fields = fields
        self.id = id
        self.relations = relations
        self.rev = rev
        self.url = url

        self.organization = organization
        self.project = project

    def getDetails(self,headers):
        #Makes a request to get the details we need
        response = requests.get(self.url, headers=headers)#Cuidado con el header
        pprint.pprint(response.json())
        print("processing fields")

    def __repr__(self):
        return (
            f"WorkItem(id={self.id}, rev={self.rev}, url={self.url}, "
            f"fields={self.fields}, relations={self.relations})"
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