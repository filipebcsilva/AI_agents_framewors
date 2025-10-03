import os
from PIL import Image
from dotenv import load_dotenv
from reasoning_plot import check_reasoning_and_plot
from plane_time import calculate_cargo_travel_time
from smolagents import CodeAgent,VisitWebpageTool,LiteLLMModel,GoogleSearchTool

load_dotenv()

model = LiteLLMModel(model_id="gemini/gemini-2.5-flash",
                     api_key=os.getenv("GEMINI_API_KEY"))

web_agent = CodeAgent(
    model=model,
    tools=[GoogleSearchTool(provider = "serper"), VisitWebpageTool(), calculate_cargo_travel_time],
    name = "web_agent",
    description = "Browses the web to find information",
    verbosity_level = 0,
    max_steps = 10
)

web_agent.planning_interval = 4

manager_agent = CodeAgent(
    model=model,
    tools=[calculate_cargo_travel_time],
    managed_agents=[web_agent],
    additional_authorized_imports=[
        "geopandas",
        "plotly",
        "shapely",
        "json",
        "pandas",
        "numpy",
        "plotly.express",
        "plotly.graph_objects"
    ],
    planning_interval=5,
    verbosity_level=2,
    final_answer_checks=[check_reasoning_and_plot],
    max_steps=15,
)

manager_agent.visualize()

manager_agent.run("""
Find all Batman filming locations in the world, calculate the time to transfer via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W).
Also give me some supercar factories with the same cargo plane transfer time. You need at least 6 points in total.
Represent this as spatial map of the world, with the locations represented as scatter points with a color that depends on the travel time, and save it to saved_map.png!

Here's an example of how to plot and return a map:
import plotly.express as px
df = px.data.carshare()
fig = px.scatter_map(df, lat="centroid_lat", lon="centroid_lon", text="name", color="peak_hour", size=100,
     color_continuous_scale=px.colors.sequential.Magma, size_max=15, zoom=1)
fig.show()
fig.write_image("saved_image.png")
final_answer(fig)

Never try to process strings using code: when you have a string to read, just print it and you'll see it.
""")

manager_agent.python_executor.state["fig"]