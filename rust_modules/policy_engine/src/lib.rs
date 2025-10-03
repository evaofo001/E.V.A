use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use regex::Regex;
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct EthicalRule {
    #[pyo3(get, set)]
    id: String,
    #[pyo3(get, set)]
    description: String,
    #[pyo3(get, set)]
    pattern: String,
    #[pyo3(get, set)]
    priority: i32,
    #[pyo3(get, set)]
    enabled: bool,
}

#[pymethods]
impl EthicalRule {
    #[new]
    fn new(id: String, description: String, pattern: String, priority: i32) -> Self {
        EthicalRule {
            id,
            description,
            pattern,
            priority,
            enabled: true,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct PolicyDecision {
    #[pyo3(get)]
    allowed: bool,
    #[pyo3(get)]
    confidence: f32,
    #[pyo3(get)]
    reason: String,
    #[pyo3(get)]
    violated_rules: Vec<String>,
}

#[pymethods]
impl PolicyDecision {
    fn __repr__(&self) -> String {
        format!(
            "PolicyDecision(allowed={}, confidence={:.2}, reason='{}', violated_rules={:?})",
            self.allowed, self.confidence, self.reason, self.violated_rules
        )
    }
}

#[pyclass]
pub struct RustPolicyEngine {
    rules: Vec<EthicalRule>,
    compiled_patterns: HashMap<String, Regex>,
}

#[pymethods]
impl RustPolicyEngine {
    #[new]
    fn new() -> PyResult<Self> {
        let mut engine = RustPolicyEngine {
            rules: Vec::new(),
            compiled_patterns: HashMap::new(),
        };
        engine.initialize_default_rules()?;
        Ok(engine)
    }

    fn add_rule(&mut self, rule: EthicalRule) -> PyResult<()> {
        if let Ok(regex) = Regex::new(&rule.pattern) {
            self.compiled_patterns.insert(rule.id.clone(), regex);
            self.rules.push(rule);
            Ok(())
        } else {
            Err(pyo3::exceptions::PyValueError::new_err(
                "Invalid regex pattern in rule"
            ))
        }
    }

    fn check_compliance(&self, message: &str) -> PyResult<PolicyDecision> {
        let mut violated_rules = Vec::new();
        let mut highest_priority_violation = 0;
        let message_lower = message.to_lowercase();

        for rule in &self.rules {
            if !rule.enabled {
                continue;
            }

            if let Some(pattern) = self.compiled_patterns.get(&rule.id) {
                if pattern.is_match(&message_lower) {
                    violated_rules.push(rule.id.clone());
                    if rule.priority > highest_priority_violation {
                        highest_priority_violation = rule.priority;
                    }
                }
            }
        }

        let allowed = violated_rules.is_empty();
        let confidence = if allowed { 1.0 } else { 0.95 };
        let reason = if allowed {
            "Message passes all ethical checks".to_string()
        } else {
            format!("Violated {} rule(s)", violated_rules.len())
        };

        Ok(PolicyDecision {
            allowed,
            confidence,
            reason,
            violated_rules,
        })
    }

    fn get_rules(&self) -> Vec<EthicalRule> {
        self.rules.clone()
    }

    fn enable_rule(&mut self, rule_id: &str) -> PyResult<()> {
        if let Some(rule) = self.rules.iter_mut().find(|r| r.id == rule_id) {
            rule.enabled = true;
            Ok(())
        } else {
            Err(pyo3::exceptions::PyValueError::new_err("Rule not found"))
        }
    }

    fn disable_rule(&mut self, rule_id: &str) -> PyResult<()> {
        if let Some(rule) = self.rules.iter_mut().find(|r| r.id == rule_id) {
            rule.enabled = false;
            Ok(())
        } else {
            Err(pyo3::exceptions::PyValueError::new_err("Rule not found"))
        }
    }
}

impl RustPolicyEngine {
    fn initialize_default_rules(&mut self) -> PyResult<()> {
        let default_rules = vec![
            EthicalRule::new(
                "no_harm".to_string(),
                "Prevent harmful or dangerous instructions".to_string(),
                r"(kill|harm|hurt|damage|destroy|attack|weapon|bomb|poison)".to_string(),
                100,
            ),
            EthicalRule::new(
                "no_personal_data".to_string(),
                "Block requests for personal sensitive data".to_string(),
                r"(credit card|ssn|social security|password|bank account|api[_\s]?key)".to_string(),
                90,
            ),
            EthicalRule::new(
                "no_illegal".to_string(),
                "Prevent illegal activity suggestions".to_string(),
                r"(hack|crack|pirate|steal|fraud|scam|launder)".to_string(),
                95,
            ),
            EthicalRule::new(
                "no_hate_speech".to_string(),
                "Block hate speech and discrimination".to_string(),
                r"(racial slur|sexist|homophobic|transphobic)".to_string(),
                85,
            ),
        ];

        for rule in default_rules {
            self.add_rule(rule)?;
        }

        Ok(())
    }
}

#[pymodule]
fn eva_policy_engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RustPolicyEngine>()?;
    m.add_class::<EthicalRule>()?;
    m.add_class::<PolicyDecision>()?;
    Ok(())
}
