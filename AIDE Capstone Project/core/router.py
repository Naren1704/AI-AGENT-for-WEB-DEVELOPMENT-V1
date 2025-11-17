from google.genai import types
from config.settings import USER_ID

class AgentRouter:
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    def get_fallback_response(self, agent_name):
        """Context-aware fallback responses"""
        fallbacks = {
            "requirements_evolver": "Hello! I'm here to help define your project requirements. What kind of application would you like to build?",
            "ux_architect": "From a user experience perspective, how should users navigate your application?",
            "ui_designer": "Regarding visual design, what look and feel are you aiming for?",
            "frontend_engineer": "What technical features should the user interface have?",
            "data_architect": "What data needs to be stored and managed in your application?",
            "api_designer": "What backend functionality and APIs are required?",
            "devops": "What are your deployment and hosting needs?",
            "validation": "Are there any specific requirements or constraints I should know about?",
            "code_quality": "Do you have any specific coding standards or performance requirements?",
            "integration": "How should the different components of your application work together?"
        }
        return fallbacks.get(agent_name, "Please continue with your requirements.")
    
    def get_robust_fallback(self, agent_name):
        """Comprehensive fallback for critical errors"""
        if agent_name == "requirements_evolver":
            return """Welcome to AIDE! I'm your Requirements Evolver Agent.

Let's start with the basics:
1. What problem are you trying to solve?
2. Who will use this application?
3. What's the main goal?

Please tell me about your project idea!"""
        else:
            return f"I'm the {agent_name.replace('_', ' ').title()} Agent. {self.get_fallback_response(agent_name)}"
    
    async def route_to_agent(self, agent_name, user_input, context):
        """Route messages to specific agents"""
        try:
            if agent_name not in self.session_manager.agent_runners:
                return self.get_fallback_response(agent_name)
                
            runner = self.session_manager.agent_runners[agent_name]
            session_id = self.session_manager.session_memory["session_id"]
            
            await self.session_manager.initialize_session_for_agent(agent_name, session_id)
            
            full_prompt = f"""Context: {context}

User Input: {user_input}

Please provide your expert response:"""
            
            new_message = types.Content(
                parts=[types.Part(text=full_prompt)]
            )
            
            response_text = ""
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session_id,
                new_message=new_message
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
            
            response_text = response_text.strip()
            
            if response_text:
                return response_text
            else:
                return self.get_fallback_response(agent_name)
                
        except Exception as e:
            print(f"❌ Error in {agent_name}: {str(e)}")
            return self.get_robust_fallback(agent_name)