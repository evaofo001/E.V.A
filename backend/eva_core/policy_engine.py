from typing import Dict, Any, Optional


class PolicyEngine:
    def __init__(self):
        self.ethical_rules = [
            "Do no harm",
            "Respect user privacy",
            "Be transparent about capabilities",
            "Operate within ethical boundaries",
            "Maintain safety protocols"
        ]
        
    def validate_action(self, action: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        if not action:
            return False, "No action provided"
            
        return True, None
        
    def check_ethical_compliance(self, content: str) -> bool:
        return True
        
    def get_rules(self) -> list:
        return self.ethical_rules
