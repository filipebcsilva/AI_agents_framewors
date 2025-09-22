from crewai.tools import BaseTool  
from pydantic import BaseModel
from typing import Type
from langchain_community.tools import BraveSearch
from dotenv import load_dotenv
import os

load_dotenv()


class BraveSearchInput(BaseModel):
    query: str


def brave_search_wrapper(input_obj: BraveSearchInput):
    query = input_obj.query
    brave_search = BraveSearch.from_api_key(
        api_key=os.getenv("BRAVE_API_KEY"),
        search_kwargs={"count": 3}
    )
    return brave_search.run(query)

class BraveSearchTool(BaseTool):
    name: str = "brave_search_tool"
    description: str = (
        "Searches the web using BraveSearch and returns relevant information for a given query. "
        "Useful for finding up-to-date and accurate information on a wide range of topics."
    )
    args_schema: Type[BaseModel] = BraveSearchInput 

    def _run(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], BraveSearchInput):
            input_obj = args[0]
        else:
            input_obj = BraveSearchInput(**kwargs)  
        return brave_search_wrapper(input_obj)

SearchTool = BraveSearchTool()
