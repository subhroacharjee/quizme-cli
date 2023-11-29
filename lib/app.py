
import argparse
import json
from pathlib import Path

from lang_chain_config import LLMChainConfig

parser = argparse.ArgumentParser()

parser.add_argument("--path") # path to pdf file
parser.add_argument("--url", default="neo4j://localhost:7687") # neo4j url
parser.add_argument("--password", default="password") # neo4j password
parser.add_argument("--username", default="neo4j") # neo4j username
parser.add_argument("-n", default=10)
parser.add_argument("--label", default="pdf")
parser.add_argument("-o", "--output", default="output.json")


def format_result(result):
  print("[Running]formatting")
  res = {}

  for elem in result:
    res[elem["question"]] = elem["answer"]
  
  list_of_questions = []
  for key in res:
    list_of_questions.append({
      "question": key,
      "answer": res[key],
    })
  return list_of_questions

if __name__ == '__main__':
  args = parser.parse_args()
  target_path = Path(args.path)
  if not target_path.exists():
    print("The target pdf does not exists")
    raise SystemExit(1)

  llmconfig = LLMChainConfig(config={
    "url": args.url,
    "password": args.password,
    "username": args.username,
  })

  print("[Running] main")
  result = llmconfig.run(target_path, args.label, args.n)
  
  
  with open(Path(args.output), "w") as js:
    json.dump(format_result(result), js, sort_keys=True, indent=4)
  print("[SUCCESS]")