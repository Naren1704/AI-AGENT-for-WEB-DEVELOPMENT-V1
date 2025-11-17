def display_system_status(agent_registry, session_memory):
    """Display system status"""
    print("\n" + "="*50)
    print("🎯 AIDE SYSTEM - READY FOR DEPLOYMENT")
    print(f"📊 Total Agents: {len(agent_registry)}")
    print(f"🆔 Session ID: {session_memory['session_id']}")
    print("="*50)

def display_requirements_header():
    """Display requirements evolution header"""
    print("\n" + "="*60)
    print("🚀 AIDE SYSTEM - REQUIREMENTS EVOLUTION INITIATED")
    print("="*60)
    print("I'll ask questions to understand your project requirements.")
    print("Please answer each question clearly. Type 'exit' to stop.\n")