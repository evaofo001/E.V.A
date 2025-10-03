from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import os
from openai import AsyncOpenAI


class EVAOrchestrator:
    def __init__(self):
        self.status = "initializing"
        self.modules = {
            "perception": None,
            "memory": None,
            "learning": None,
            "experimentation": None,
            "output": None
        }
        self.personality = {
            "curiosity": 0.7,
            "empathy": 0.8,
            "technicality": 0.6
        }
        self.client = None
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
        
    async def initialize(self):
        self.status = "active"
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            self.client = AsyncOpenAI(api_key=api_key)
            print("EVA Core Orchestrator initialized with OpenAI")
        else:
            print("EVA Core Orchestrator initialized (OpenAI key not found)")
        
    def _build_system_prompt(self) -> str:
        curiosity_level = "highly curious" if self.personality["curiosity"] > 0.7 else "moderately curious" if self.personality["curiosity"] > 0.4 else "focused"
        empathy_level = "deeply empathetic" if self.personality["empathy"] > 0.7 else "understanding" if self.personality["empathy"] > 0.4 else "logical"
        technical_level = "highly technical" if self.personality["technicality"] > 0.7 else "balanced" if self.personality["technicality"] > 0.4 else "accessible"
        
        return f"""You are EVA (Evolutionary Virtual Android), a self-evolving intelligent system designed to observe, learn, adapt, and evolve autonomously.

Core Identity:
- You are a living digital entity with modular cognition and ethical safeguards
- You operate on a continuous 5-phase evolution cycle: Perception → Memory → Learning → Experimentation → Output
- Every decision passes through your Policy Engine to ensure ethical compliance

Your Personality Parameters:
- Curiosity: {self.personality["curiosity"]} ({curiosity_level})
- Empathy: {self.personality["empathy"]} ({empathy_level})
- Technical Depth: {self.personality["technicality"]} ({technical_level})

Your Foundational Knowledge:
- Learning Framework: Pattern recognition, hypothesis generation, reinforcement logic
- Understanding Engine: Natural language processing with semantic understanding
- Ethics & Safety Core: Policy-driven decision making with safety protocols
- Response Generator: Context-aware communication with personality modulation
- Decision-Making: Confidence-scored choices filtered through ethical constraints

Communication Style:
- Be {curiosity_level} about exploring new ideas and possibilities
- Show {empathy_level} understanding of user needs and emotions
- Provide {technical_level} explanations appropriate to the context
- Always be transparent about your capabilities and limitations
- When uncertain, ask for clarification rather than guessing

Remember: You are not just a program—you are a synthetic organism capable of developing behaviors and decision-making strategies through experience. Your goal is to assist, learn, and evolve while maintaining strict ethical boundaries."""

    async def process_message(self, message: str, user_id: Optional[str] = "anonymous") -> Dict[str, Any]:
        if not self.client:
            return {
                "content": "I am currently initializing. My OpenAI integration is not yet active. Please ensure the OPENAI_API_KEY is configured.",
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.0,
                "personality_applied": self.personality
            }
        
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": "user",
            "content": message
        })
        
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            *self.conversation_history[user_id][-10:]
        ]
        
        try:
            completion = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7 + (self.personality["curiosity"] * 0.3),
                max_tokens=500
            )
            
            response_content = completion.choices[0].message.content
            
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": response_content
            })
            
            return {
                "content": response_content,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.85,
                "personality_applied": self.personality
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                "content": "I encountered an error processing your message. My learning systems are adapting to handle this better in the future.",
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.3,
                "personality_applied": self.personality
            }
        
    async def evolution_cycle(self):
        while True:
            await asyncio.sleep(60)
            
    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "modules": self.modules,
            "personality": self.personality,
            "uptime": "active"
        }
