
from app.core.devops_models import *
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from app.core.utils import filter_dataframe

#For the interface
import streamlit as st

class SlProject(Project):
    """A class to represent a project in Streamlit.

    Args:
        Project (Project): The base class for projects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"SlProject({self.__dict__})"

    def display_in_streamlit(self):
        """
        Display the Project details in a Streamlit app with a clean and elegant layout.
        """
        st.markdown(f"### Project ID: {self.id}")
        st.markdown(f"**Name:** {self.name}")
        st.markdown(f"**State:** {self.state}")
        st.markdown(f"**Description:** {self.description}")
        st.markdown(f"**URL:** [Link to Project]({self.url})")
        st.markdown("---")

class SlWebApiTeams(WebApiTeam):
    """A class to represent a Web API team in Streamlit.

    Args:
        WebApiTeam (WebApiTeam): The base class for Web API teams.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"SlWebApiTeams({self.__dict__})"

    def display_in_streamlit(self):
        """
        Display the WebApiTeam details in a Streamlit app with a clean and elegant layout.
        """
        st.markdown(f"### Team ID: {self.id}")
        st.markdown(f"**Name:** {self.name}")
        st.markdown(f"**URL:** [Link to Team]({self.url})")
        st.markdown("---")

class SlIdentityRef(IdentityRef):
    """A class to represent an identity reference in Streamlit.

    Args:
        IdentityRef (IdentityRef): The base class for identity references.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"SlIdentityRef({self.__dict__})"

    def display_in_streamlit(self):
        """
        Display the IdentityRef details in a Streamlit app with a clean and elegant layout.
        """
        st.markdown(f"### Identity ID: {self.id}")
        st.markdown(f"**Name:** {self.displayName}")
        st.markdown(f"**URL:** [Link to Identity]({self.url})")
        st.markdown("---")

class SlWorkItem(WorkItem):
    """A class to represent a work item in Streamlit.

    Args:
        WorkItem (WorkItem): The base class for work items.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"SlWorkItem({self.__dict__})"

    def display_in_streamlit(self):
        """
        Display the WorkItem details in a Streamlit app with a clean and elegant layout.
        """
        st.markdown(f"### Work Item ID: {self.id}")
        st.markdown(f"**Title:** {self.title}")
        st.markdown(f"**State:** {self.state}")
        st.markdown(f"**Completed Hours:** {self.completedHours}")
        st.markdown(f"**URL:** [Link to Work Item]({self.url})")
        st.markdown("---")

class SlWorkItemQueryResult(WorkItemQueryResult):
    """A class to represent a work item query result in Streamlit.

    Args:
        WorkItemQueryResult (WorkItemQueryResult): The base class for work item query results.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"SlWorkItemQueryResult({self.__dict__})"
    
    def display_in_streamlit(self):
        """
        Display the WorkItemQueryResult in a Streamlit app with a clean and elegant layout.
        """
        st.markdown(f"### Total Work Items: {len(self.workItems)}")
        df = self.to_dataframe()
        
        if "assignedTo" in df.columns:
            df["assigned_to"] = df["assignedTo"].apply(lambda x: x.get("displayName") if isinstance(x, dict) else None)
            df["assignedTo_email"] = df["assignedTo"].apply(lambda x: x.get("uniqueName") if isinstance(x, dict) else None)

        columns_to_drop = {"commentVersionRef", "fields", "relations", "assignedTo","organization"}

        if "project" in df.columns:
            if df["project"].nunique() <= 1 or df["project"].isnull().all():
                columns_to_drop.add("project")

        df = df.drop(columns=columns_to_drop.intersection(df.columns))


        st.dataframe(filter_dataframe(df))
