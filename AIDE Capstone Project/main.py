import asyncio
import time
from agents.specialized import agent_registry
from core.session_manager import SessionManager
from core.router import AgentRouter
from utils.helpers import display_system_status, display_requirements_header

async def start_requirements_evolution(session_manager, router):
    """Start the requirements gathering process"""
    display_requirements_header()
    
    session_manager.session_memory["current_phase"] = "requirements_evolution"
    session_manager.session_memory["active_agent"] = "requirements_evolver"
    
    print("🔄 Initializing session for Requirements Evolver...")
    await session_manager.initialize_session_for_agent(
        "requirements_evolver", 
        session_manager.session_memory["session_id"]
    )
    
    context = session_manager.get_session_context()
    initial_prompt = "Please start the conversation by greeting the user and asking about their project."
    
    response = await router.route_to_agent("requirements_evolver", initial_prompt, context)
    return response

async def process_user_response(session_manager, router, user_input):
    """Process user input through current active agent"""
    if user_input.lower() in ['exit', 'quit', 'stop', 'end']:
        return None
    
    current_agent = session_manager.session_memory["active_agent"]
    context = session_manager.get_session_context()
    
    try:
        response = await router.route_to_agent(current_agent, user_input, context)
        session_manager.update_session_memory(user_input, response)
        return response
    except Exception as e:
        error_msg = "System temporarily unavailable. Please try again."
        print(f"❌ Routing error: {str(e)}")
        return error_msg

async def main_interaction_loop():
    """Main interaction loop"""
    try:
        # Initialize system components
        session_manager = SessionManager()
        session_manager.initialize_runners(agent_registry)
        router = AgentRouter(session_manager)
        
        display_system_status(agent_registry, session_manager.session_memory)
        
        # Start the process
        initial_response = await start_requirements_evolution(session_manager, router)
        if initial_response:
            print(f"🤖 Requirements Evolver: {initial_response}")
        
        # Main loop
        while True:
            try:
                user_input = input("\n💬 Your response: ").strip()
                
                if not user_input:
                    print("Please enter a response to continue...")
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'stop', 'end']:
                    print("\n👋 Thank you for using AIDE! Session ended.")
                    break
                
                # Process response
                response = await process_user_response(session_manager, router, user_input)
                if response:
                    agent_display_name = session_manager.session_memory["active_agent"].replace('_', ' ').title()
                    print(f"🤖 {agent_display_name}: {response}")
                    
                    # Check for phase transition
                    if (session_manager.session_memory["evolution_cycles"] >= 3 and 
                        session_manager.session_memory["current_phase"] == "requirements_evolution"):
                        print("\n🎯 Requirements phase complete! Ready for specialist agents...")
                        
            except KeyboardInterrupt:
                print("\n\n🛑 Session interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                continue
                
    except Exception as e:
        print(f"🚨 Critical system error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main_interaction_loop())
    except Exception as e:
        print(f"🚨 Fatal error: {e}")
    finally:
        print("\n🔚 AIDE System shutdown complete.")