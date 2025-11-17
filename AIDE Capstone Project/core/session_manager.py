import time
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from config.settings import USER_ID

class SessionManager:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.agent_runners = {}
        self.session_memory = {
            "project_requirements": {},
            "current_phase": "initialization",
            "active_agent": "requirements_evolver",
            "user_responses": [],
            "evolution_cycles": 0,
            "session_id": f"aide_{int(time.time())}"
        }
    
    def initialize_runners(self, agent_registry):
        """Initialize runners for all agents"""
        print("🔄 Initializing agent runners...")
        for agent_name, agent in agent_registry.items():
            try:
                self.agent_runners[agent_name] = Runner(
                    app_name=f"aide_{agent_name}",
                    agent=agent,
                    session_service=self.session_service
                )
                print(f"   ✅ {agent_name} runner ready")
            except Exception as e:
                print(f"   ❌ {agent_name} runner failed: {e}")
        print("✅ All runners initialized!")
    
    async def initialize_session_for_agent(self, agent_name, session_id):
        """Initialize a session for a specific agent"""
        try:
            runner = self.agent_runners[agent_name]
            session = await self.session_service.create_session(
                app_name=runner.app_name,
                user_id=USER_ID,
                session_id=session_id
            )
            print(f"   ✅ Session created for {agent_name}")
            return session
        except Exception as e:
            try:
                session = await self.session_service.get_session(
                    app_name=runner.app_name,
                    user_id=USER_ID,
                    session_id=session_id
                )
                print(f"   ✅ Session retrieved for {agent_name}")
                return session
            except Exception as e2:
                print(f"   ❌ Failed to initialize session for {agent_name}: {e2}")
                return None
    
    def update_session_memory(self, user_input, agent_response):
        """Update session memory with interaction"""
        self.session_memory["user_responses"].append({
            "agent": self.session_memory["active_agent"],
            "user_input": user_input,
            "agent_response": agent_response,
            "timestamp": time.time()
        })
        
        if self.session_memory["active_agent"] == "requirements_evolver":
            self.session_memory["evolution_cycles"] += 1
    
    def get_session_context(self):
        """Get current session context"""
        recent_responses = self.session_memory["user_responses"][-3:] if self.session_memory["user_responses"] else []
        context_summary = "\n".join([
            f"- {resp['agent']}: User said '{resp['user_input'][:50]}...'" 
            for resp in recent_responses
        ])
        
        return f"""
Project Phase: {self.session_memory['current_phase']}
Active Agent: {self.session_memory['active_agent']}
Previous Interactions: {len(self.session_memory['user_responses'])}
Evolution Cycles: {self.session_memory['evolution_cycles']}
Recent Context:
{context_summary}
"""