# Multi-Agent State-Driven Chatbot

A chatbot framework that utilizes a state graph to manage interactions with tools and external APIs. This system combines machine learning language models with tools and integrates them into a flexible state graph architecture for managing conversational flow.

## Features
- **State Graph Architecture**: Utilizes a directed acyclic graph (DAG) to manage the flow of messages and integrate tools.
- **Dynamic Interaction**: Dynamically binds tools with a language model (LLM) to generate contextually appropriate responses.
- **Condition-based Flow Control**: The flow between chatbot states can be influenced by conditional logic, allowing for complex conversational structures.
- **Visualization**: The architecture is visualized using Mermaid, making it easier to understand the flow of the chatbot.

## Technologies Used
- **Python**: Core programming language.
- **Langgraph**: Framework for building and managing state graphs.
- **Mermaid**: Visualization tool for generating flow diagrams.
- **LLM (Large Language Models)**: Pre-trained language models (like GPT or others) for conversational AI.
- **IPython**: Used for displaying visual outputs within Jupyter Notebooks.

## Prerequisites

Before you start, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)

### Dependencies:
You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

#### Required Libraries:
- `langgraph`
- `IPython`
- `mermaid`
- `threading`
- `typing`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/multi-agent-state-driven-chatbot.git
   cd multi-agent-state-driven-chatbot
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Define State**: The chatbot utilizes a `State` that contains the list of messages. This state is used by the chatbot to store and manage conversation history.

   ```python
   class State(TypedDict):
       messages: Annotated[list, add_messages]
   ```

2. **Bind Tools with LLM**: The `llm_with_tools` object binds the tools (external functionalities or APIs) with the language model to enhance the chatbot's abilities.

   ```python
   llm_with_tools = llm.bind_tools(tools=[tools])
   ```

3. **Create Chatbot Function**: This function takes the state as input and returns a chatbot response after invoking the LLM with the tools.

   ```python
   def chatbot(State: State):
       return {"messages": llm_with_tools.invoke(State["messages"])}
   ```

4. **Build State Graph**: The graph manages the nodes, edges, and the flow of the chatbot. The chatbot node interacts with the tools node, which can be conditional.

   ```python
   graph_builder = StateGraph(State)
   graph_builder.add_node("chatbot", chatbot)
   graph_builder.add_edge(START, "chatbot")
   ```

5. **Tool Node and Flow Setup**: The flow is controlled using conditional edges between the nodes. The tools node allows the chatbot to access various tools when required.

   ```python
   tools_node = ToolNode(tools=[tools])
   graph_builder.add_node("Tools", tools_node)
   graph_builder.add_conditional_edges("chatbot", tools_condition)
   graph_builder.add_edge("Tools", "chatbot")
   graph_builder.add_edge("chatbot", END)
   ```

6. **Compile the Graph**: Once the nodes and edges are set up, the graph is compiled into a functional state machine.

   ```python
   graph = graph_builder.compile()
   ```

## Visualization

The graph is visualized using Mermaid, and the compiled graph can be displayed in a Jupyter Notebook.

```python
from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    raiseExceptions("Mermaid not properly configured.")
```

## Usage

### Running the Chatbot

To run the chatbot, follow these steps:

1. Start by initializing the state and tools, then run the graph-building steps as described.
2. Use the `chatbot()` function to get responses.

Example:

```python
state = State(messages=["Hello, chatbot!"])
response = chatbot(state)
print(response)
```

This will invoke the chatbot with the given state, process the conversation flow using the state graph, and return the appropriate response.

### Error Handling

The graph compilation and visualization are protected with proper error handling. If Mermaid is not properly configured, an exception is raised:

```python
except Exception:
    raiseExceptions("Mermaid not properly configured.")
```

This ensures that the system gracefully handles any errors related to Mermaid visualization.

### Customizing the Flow

You can modify the flow by adding new nodes, tools, or conditions to the state graph:

1. **Add New Tools**: Add additional tools to the `tools_node` to extend the chatbot's functionality.
2. **Modify Conditions**: Change the conditions for when the chatbot should interact with the tools node.
3. **Extend the State**: Add more fields to the `State` TypedDict to support additional data or functionality.

## Example Graph

Here’s a simple example of how the graph might be visualized:

- `START` → `chatbot` → `Tools` → `chatbot` → `END`

This flow illustrates the chatbot interacting with tools and continuing the conversation until completion.

## Contributing

1. Fork the repository.
2. Create your branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Please make sure your code passes all tests and adheres to the project's coding guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Langgraph** for the state graph framework.
- **Mermaid** for visualization.
- **IPython** for easy integration with Jupyter Notebooks.

---
