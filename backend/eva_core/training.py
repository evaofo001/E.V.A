from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import asyncio
from collections import defaultdict
import re


class LearnedPattern:
    def __init__(self, pattern_id: str, description: str, keywords: List[str], confidence: float = 0.5):
        self.pattern_id = pattern_id
        self.description = description
        self.keywords = keywords
        self.confidence = confidence
        self.learned_at = datetime.now()
        self.usage_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "description": self.description,
            "keywords": self.keywords,
            "confidence": self.confidence,
            "learned_at": self.learned_at.isoformat(),
            "usage_count": self.usage_count
        }


class TrainingPipeline:
    def __init__(self):
        self.conversation_data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.learned_patterns: List[LearnedPattern] = []
        self.topic_frequency: Dict[str, int] = defaultdict(int)
        self.quality_threshold = 0.7
        
    async def record_interaction(self, user_id: str, user_message: str, eva_response: str, confidence: float):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "eva_response": eva_response,
            "confidence": confidence
        }
        self.conversation_data[user_id].append(interaction)
        
        await self._extract_patterns(user_message, eva_response)
        
    async def _extract_patterns(self, user_message: str, eva_response: str):
        words = re.findall(r'\b\w+\b', user_message.lower())
        topics = [w for w in words if len(w) > 4]
        
        for topic in topics:
            self.topic_frequency[topic] += 1
            
            if self.topic_frequency[topic] >= 3 and topic not in [p.pattern_id for p in self.learned_patterns]:
                pattern = LearnedPattern(
                    pattern_id=f"topic_{topic}",
                    description=f"Recognized topic: {topic}",
                    keywords=[topic],
                    confidence=min(0.5 + (self.topic_frequency[topic] * 0.1), 0.95)
                )
                self.learned_patterns.append(pattern)
                print(f"🧠 EVA learned new pattern: {topic} (confidence: {pattern.confidence:.2f})")
    
    def get_learned_patterns(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.learned_patterns]
    
    def get_conversation_insights(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.conversation_data:
            return {"message": "No data available for this user"}
        
        conversations = self.conversation_data[user_id]
        total_interactions = len(conversations)
        avg_confidence = sum(c["confidence"] for c in conversations) / total_interactions if total_interactions > 0 else 0
        
        recent_topics = []
        for conv in conversations[-5:]:
            words = re.findall(r'\b\w+\b', conv["user_message"].lower())
            recent_topics.extend([w for w in words if len(w) > 4])
        
        return {
            "total_interactions": total_interactions,
            "average_confidence": round(avg_confidence, 2),
            "recent_topics": list(set(recent_topics))[:10],
            "learned_patterns_count": len(self.learned_patterns)
        }
    
    async def improve_response_quality(self, message: str) -> Optional[str]:
        for pattern in self.learned_patterns:
            if any(keyword in message.lower() for keyword in pattern.keywords):
                pattern.usage_count += 1
                return f"[Learned Pattern: {pattern.description}] "
        return None
    
    def export_training_data(self, filepath: str):
        data = {
            "patterns": self.get_learned_patterns(),
            "topic_frequency": dict(self.topic_frequency),
            "total_conversations": sum(len(convs) for convs in self.conversation_data.values()),
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📊 Training data exported to {filepath}")
    
    def import_training_data(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for pattern_data in data.get("patterns", []):
                pattern = LearnedPattern(
                    pattern_id=pattern_data["pattern_id"],
                    description=pattern_data["description"],
                    keywords=pattern_data["keywords"],
                    confidence=pattern_data["confidence"]
                )
                pattern.usage_count = pattern_data.get("usage_count", 0)
                self.learned_patterns.append(pattern)
            
            self.topic_frequency.update(data.get("topic_frequency", {}))
            print(f"📥 Training data imported from {filepath}")
            
        except FileNotFoundError:
            print(f"⚠️ Training data file not found: {filepath}")
