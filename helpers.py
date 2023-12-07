from re import match
from typing import List, Dict, Any

def parseLine(line):
    temp = match(r"Rule\((\d+)\): IF \(([^)]+)\), THEN \(([^)]+)\)", line.decode("utf-8").strip())
    if temp:
        return {
            "number": int(temp.group(1)),
            "premises": [p.strip() for p in temp.group(2).split(',')],
            "actions": [a.strip() for a in temp.group(3).split(',')]
        }    
    return None

def filterRules(rules, facts):
    return [rule for rule in rules if not all(action in facts for action in rule["actions"])]

def getFirstVerifiedRuleIndex(facts, rules):
    for index, rule in enumerate(rules):
        if all(premise in facts for premise in rule["premises"]):
            return index
    return None

def forwardChaining(facts, rules, factToProve):
    fact_found: bool = factToProve in facts
    proof: List[Dict[str, Any]] = []
    while not fact_found:
      index: int = getFirstVerifiedRuleIndex(facts, rules)
      if index is None:
        break
      else:
        rule: Dict[str, Any] = rules[index]
        facts.extend(rule["actions"])
        proof.append({
          "rule" : rule,
          "facts": facts.copy()
        })
        rules.remove(rule)
        if(factToProve in rule["actions"]):
          fact_found = True

    return proof, fact_found

def backwardChaining(facts, rules: List[Dict[str, Any]], factToProve):
    if(factToProve in facts):
       return [], True
    done = False
    while not done:
      rule: Dict[str, Any] = getNextRule(factToProve, rules)
      if(rule is None):
        return [], False 
      proofs = [{
        "rule": rule,
      }]

      all_premises_proven = True
      rules.remove(rule)

      for premise in rule["premises"]:
        premise_proof, premise_proven = backwardChaining(facts, rules, premise)
        proofs.extend(premise_proof)
        if not premise_proven:
          all_premises_proven = False
          break

      if all_premises_proven:
        return proofs, all_premises_proven
    return [], False
      
        

def getNextRule(fact, rules):
    for _, rule in enumerate(rules):
        if fact in rule["actions"]:
            return rule
    return None

