from flask import Flask, render_template, request
from helpers import parseLine, filterRules, forwardChaining, backwardChaining
from typing import List, Dict, Any

app: Flask = Flask(__name__)

@app.route("/")
def hello() -> str:
  return render_template('index.html')

@app.route("/process", methods=['POST'])
def process() -> None:
  factToProve: str = request.form.get("fact")
  chainingType: str = request.form.get("chaining_type")

  facts: List[str] = []
  with request.files.get("facts_file").stream as file:
    for line in file:
      facts.append(line.decode("utf-8").strip())
    
  rules: List[Dict[str, Any]] = []
  ui_rules = []
  with request.files.get("rules_file").stream as file:
    for line in file:
      ui_rules.append(line.decode("utf-8").strip())
      rules.append(parseLine(line))

  filteredRules: List[Dict[str, Any]] = filterRules(rules, facts)

  if(chainingType == 'forward'):
    proof, fact_found = forwardChaining(facts, filteredRules, factToProve)
    return render_template('forward.html', proof_list=proof, fact_found=fact_found, rules=ui_rules, facts=facts, factToProve=factToProve)
  else:
    proof, fact_found = backwardChaining(facts, filteredRules, factToProve)
    return render_template('backward.html', proof_list=proof, fact_found=fact_found, rules=ui_rules, facts=facts, factToProve=factToProve)


if __name__ == "__main__":
  app.run(debug=True)