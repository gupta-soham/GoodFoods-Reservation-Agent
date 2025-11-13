"""
Diagram Generation Code for GoodFoods Reservation Agent Architecture
All diagram generation code stored for future reference and modifications
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python
from diagrams.onprem.network import Internet, Nginx
from diagrams.programming.flowchart import PredefinedProcess, Database, Action, Decision, Document, InputOutput, StartEnd
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server
from diagrams.generic.os import Ubuntu

def generate_system_architecture():
    """Generate System Architecture diagram"""
    with Diagram("GoodFoods Reservation Agent - System Architecture", show=False, direction="LR"):
        # User Interface Layer
        with Cluster("Frontend Layer"):
            user = User("User")
            streamlit = Flask("Streamlit UI\napp.py")
        
        # Agent Layer
        with Cluster("Agent Layer"):
            agent = Python("Reservation Agent\nagent.py")
            cerebras = Internet("Cerebras Cloud\nLLM API")
        
        # MCP Protocol Layer
        with Cluster("MCP Protocol Layer"):
            mcp_server = Nginx("MCP Server\nserver.py")
            tools = PredefinedProcess("Tool Registry")
        
        # Database Layer
        with Cluster("Database Layer"):
            db = Redis("In-Memory DB\nrestaurant_db.py")
            models = Database("Data Models\nRestaurant\nReservation")
        
        # Data Flow
        user >> streamlit
        streamlit >> agent
        agent >> cerebras
        agent >> mcp_server
        mcp_server >> tools
        mcp_server >> db
        db >> models

def generate_tool_calling_flow():
    """Generate Tool Calling Flow diagram"""
    with Diagram("Tool Calling Flow - Restaurant Search & Reservation", show=False, direction="LR"):
        # User Input
        user_input = InputOutput("User Query\nFind Italian restaurants\nfor 4 people tonight")
        
        # Agent Processing
        with Cluster("Agent Processing"):
            agent = Python("Reservation\nAgent")
            llm_call = Internet("Cerebras LLM\nllama-3.3-70b")
            tool_decision = Decision("Tool Calling\nRequired?")
        
        # Tool Execution
        with Cluster("MCP Tool Execution"):
            search_tool = Action("search_restaurants")
            availability_tool = Action("get_availability")
            reservation_tool = Action("make_reservation")
            recommendation_tool = Action("get_recommendations")
            cancel_tool = Action("cancel_reservation")
        
        # Database Operations
        with Cluster("Database Operations"):
            restaurant_db = Redis("In-Memory DB")
            query_restaurants = Database("Query\nRestaurants")
            check_availability = Database("Check\nAvailability")
            create_reservation = Database("Create\nReservation")
        
        # Response Generation
        response_gen = Action("Generate\nResponse")
        user_response = InputOutput("Formatted Response\nwith Restaurant Details")
        
        # Flow
        user_input >> agent
        agent >> llm_call
        llm_call >> tool_decision
        
        # Tool routing
        tool_decision >> Edge(label="search") >> search_tool
        tool_decision >> Edge(label="availability") >> availability_tool
        tool_decision >> Edge(label="reservation") >> reservation_tool
        tool_decision >> Edge(label="recommend") >> recommendation_tool
        tool_decision >> Edge(label="cancel") >> cancel_tool
        
        # Database operations
        search_tool >> query_restaurants
        availability_tool >> check_availability
        reservation_tool >> create_reservation
        
        query_restaurants >> restaurant_db
        check_availability >> restaurant_db
        create_reservation >> restaurant_db
        
        # Response flow
        restaurant_db >> response_gen
        response_gen >> user_response

def generate_component_interaction():
    """Generate Component Interaction diagram"""
    with Diagram("Component Interaction & Data Flow", show=False, direction="LR"):
        # Frontend Components
        with Cluster("Streamlit Frontend (app.py)"):
            ui = Flask("Chat Interface")
            session = Document("Session State")
            config = Document("UI Config")
        
        # Agent Components
        with Cluster("Agent Layer"):
            with Cluster("agent/agent.py"):
                agent_core = Python("ReservationAgent")
                tool_schemas = Document("Tool Schemas")
                conversation = Document("Conversation\nContext")
            
            with Cluster("agent/cerebras_client.py"):
                cerebras_client = Python("CerebrasClient")
                api_config = Document("API Config")
        
        # External LLM
        llm_service = Internet("Cerebras Cloud\nllama-3.3-70b")
        
        # MCP Server Components
        with Cluster("MCP Server (mcp_server/server.py)"):
            mcp_server = Python("MCPServer")
            tool_registry = Action("Tool Registry")
            resource_registry = Action("Resource Registry")
        
        # Database Components
        with Cluster("Database Layer"):
            with Cluster("database/restaurant_db.py"):
                db_manager = Redis("In-Memory Database")
                
            with Cluster("database/models.py"):
                restaurant_model = Database("Restaurant Model")
                reservation_model = Database("Reservation Model")
                
            with Cluster("database/seed_data.py"):
                seed_data = Document("Sample Data")
        
        # User interaction flow
        user = User("User")
        user >> ui
        ui >> session
        ui >> agent_core
        
        # Agent processing flow
        agent_core >> tool_schemas
        agent_core >> conversation
        agent_core >> cerebras_client
        cerebras_client >> api_config
        cerebras_client >> llm_service
        
        # Tool calling flow
        agent_core >> mcp_server
        mcp_server >> tool_registry
        mcp_server >> resource_registry
        mcp_server >> db_manager
        
        # Database operations
        db_manager >> restaurant_model
        db_manager >> reservation_model
        seed_data >> db_manager
        
        # Response flow back
        db_manager >> mcp_server
        mcp_server >> agent_core
        llm_service >> cerebras_client
        cerebras_client >> agent_core
        agent_core >> ui

def generate_mcp_protocol_flow():
    """Generate MCP Protocol Flow diagram"""
    with Diagram("MCP Protocol Communication Flow", show=False, direction="TB"):
        # Agent Side
        with Cluster("Agent (Client)"):
            agent = Python("Reservation Agent")
            tool_call = Action("Tool Call Request")
            response_handler = Action("Response Handler")
        
        # MCP Protocol Layer
        with Cluster("MCP Protocol (JSON-RPC 2.0)"):
            request_format = Document("JSON-RPC Request\n{\n  'method': 'tools/call',\n  'params': {...}\n}")
            response_format = Document("JSON-RPC Response\n{\n  'result': {...}\n}")
        
        # MCP Server Side
        with Cluster("MCP Server"):
            server = Python("MCPServer")
            method_router = Decision("Route Method")
            
            # Available Tools
            with Cluster("Available Tools"):
                search_tool = Action("search_restaurants")
                availability_tool = Action("get_availability")
                reservation_tool = Action("make_reservation")
                cancel_tool = Action("cancel_reservation")
                recommend_tool = Action("get_recommendations")
            
            # Tool Execution
            tool_executor = Action("Execute Tool")
            result_formatter = Action("Format Result")
        
        # Database
        database = Action("Restaurant Database")
        
        # Flow
        agent >> tool_call
        tool_call >> request_format
        request_format >> server
        server >> method_router
        
        # Tool routing
        method_router >> Edge(label="search") >> search_tool
        method_router >> Edge(label="availability") >> availability_tool
        method_router >> Edge(label="reservation") >> reservation_tool
        method_router >> Edge(label="cancel") >> cancel_tool
        method_router >> Edge(label="recommend") >> recommend_tool
        
        # Execution flow
        search_tool >> tool_executor
        availability_tool >> tool_executor
        reservation_tool >> tool_executor
        cancel_tool >> tool_executor
        recommend_tool >> tool_executor
        
        tool_executor >> database
        database >> result_formatter
        result_formatter >> response_format
        response_format >> response_handler
        response_handler >> agent

def generate_conversation_flow():
    """Generate Conversation Flow diagram"""
    with Diagram("Complete Conversation Flow - Restaurant Reservation", show=False, direction="LR", graph_attr={"splines": "ortho", "nodesep": "1.5", "ranksep": "2.0"}):
        # Start
        start = StartEnd("Start")
        
        # User Input
        user_input = InputOutput("User Message\n\nBook Italian restaurant\nfor 4 people tonight")
        
        # Streamlit Processing
        with Cluster("Streamlit Processing"):
            ui_handler = Flask("UI Handler")
            session_update = Action("Update\nSession")
        
        # Agent Processing
        with Cluster("Agent Processing"):
            agent = Python("Reservation\nAgent")
            context_build = Action("Build\nContext")
            llm_request = Action("LLM\nRequest")
            cerebras = Internet("Cerebras\nLLM")
            tool_decision = Decision("Tool Call\nNeeded?")
        
        # Tool Execution Path
        with Cluster("Tool Execution"):
            parse_tools = Action("Parse\nTools")
            execute_tools = Action("Execute\nMCP Tools")
            format_results = Action("Format\nResults")
        
        # Response Generation
        with Cluster("Response Generation"):
            generate_response = Action("Generate\nResponse")
            stream_response = Action("Stream\nResponse")
        
        # User Output
        user_output = InputOutput("AI Response\n\nFound 3 restaurants\nBella Italia at 7:30pm\nBook it?")
        
        # End or Continue
        continue_decision = Decision("Continue\nConversation?")
        end = StartEnd("End")
        
        # Main Flow
        start >> user_input >> ui_handler >> session_update >> agent
        agent >> context_build >> llm_request >> cerebras >> tool_decision
        
        # Tool Execution Branch
        tool_decision >> Edge(label="Yes") >> parse_tools >> execute_tools >> format_results >> generate_response
        
        # Direct Response Branch
        tool_decision >> Edge(label="No") >> generate_response
        
        # Response Flow
        generate_response >> stream_response >> user_output >> continue_decision
        
        # Loop or End
        continue_decision >> Edge(label="Yes") >> user_input
        continue_decision >> Edge(label="No") >> end

def generate_tool_schema_database():
    """Generate Tool Schema & Database diagram"""
    with Diagram("Tool Schema & Database Operations", show=False, direction="LR"):
        # Tool Definitions
        with Cluster("Available Tools"):
            search_tool = Action("search_restaurants")
            availability_tool = Action("get_availability")
            reservation_tool = Action("make_reservation")
            cancel_tool = Action("cancel_reservation")
            recommend_tool = Action("get_recommendations")
        
        # Parameters
        with Cluster("Parameters"):
            search_params = Document("search_restaurants\ncuisine, location\nparty_size, date, time")
            availability_params = Document("get_availability\nrestaurant_id, date\ntime, party_size")
            reservation_params = Document("make_reservation\nrestaurant_id, date, time\nparty_size, customer_name")
            cancel_params = Document("cancel_reservation\nreservation_id")
            recommend_params = Document("get_recommendations\npreferences, location\nparty_size")
        
        # Database Operations
        with Cluster("In-Memory Database"):
            restaurant_db = Redis("Restaurant DB")
            
            restaurant_model = Database("Restaurant Model\nid, name, cuisine\nlocation, address\nseating_capacity\noperating_hours\nprice_range, rating")
            
            reservation_model = Database("Reservation Model\nid, restaurant_id\ndate, time\nparty_size\ncustomer_name\ncreated_at, status")
        
        # Tool to Database Mapping
        search_tool >> restaurant_db
        availability_tool >> restaurant_db
        reservation_tool >> restaurant_db
        cancel_tool >> restaurant_db
        recommend_tool >> restaurant_db
        
        restaurant_db >> restaurant_model
        restaurant_db >> reservation_model
        
        # Parameter connections
        search_params >> search_tool
        availability_params >> availability_tool
        reservation_params >> reservation_tool
        cancel_params >> cancel_tool
        recommend_params >> recommend_tool

def generate_deployment_architecture():
    """Generate Deployment Architecture diagram"""
    with Diagram("Deployment Architecture", show=False, direction="TB"):
        # User Layer
        users = User("Users")
        
        # Application Server
        with Cluster("Application Server"):
            server = Server("Local Server\n(localhost:8501)")
            
            with Cluster("Python Environment"):
                venv = Ubuntu("Virtual Environment")
                
                with Cluster("Application Components"):
                    streamlit_app = Flask("Streamlit App\n(app.py)")
                    agent_module = Python("Agent Module")
                    mcp_server_module = Python("MCP Server")
                    database_module = Redis("In-Memory DB")
            
            with Cluster("Configuration"):
                env_config = Document(".env\nCEREBRAS_API_KEY")
                streamlit_config = Document(".streamlit/config.toml")
        
        # External Services
        with Cluster("External Services"):
            cerebras_cloud = Internet("Cerebras Cloud\nAPI Endpoint")
        
        # Local Storage
        with Cluster("Local Storage"):
            app_files = Document("Application Files\n• Python modules\n• Static assets\n• Configuration")
            session_data = Document("Session Data\n• Conversation history\n• User state")
        
        # Network Flow
        users >> Edge(label="HTTP") >> server
        server >> streamlit_app
        streamlit_app >> agent_module
        agent_module >> mcp_server_module
        mcp_server_module >> database_module
        
        # Configuration
        env_config >> agent_module
        streamlit_config >> streamlit_app
        
        # External API
        agent_module >> Edge(label="HTTPS API") >> cerebras_cloud
        
        # Storage
        streamlit_app >> session_data
        server >> app_files

def generate_all_diagrams():
    """Generate all diagrams"""
    print("Generating all architecture diagrams...")
    
    generate_system_architecture()
    print("✓ System Architecture generated")
    
    generate_tool_calling_flow()
    print("✓ Tool Calling Flow generated")
    
    generate_component_interaction()
    print("✓ Component Interaction generated")
    
    generate_mcp_protocol_flow()
    print("✓ MCP Protocol Flow generated")
    
    generate_conversation_flow()
    print("✓ Conversation Flow generated")
    
    generate_tool_schema_database()
    print("✓ Tool Schema & Database generated")
    
    generate_deployment_architecture()
    print("✓ Deployment Architecture generated")
    
    print("All diagrams generated successfully!")

if __name__ == "__main__":
    generate_all_diagrams()
