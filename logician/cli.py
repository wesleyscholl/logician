"""Simple CLI for logician"""
import argparse
from .rag import RagOrchestrator


def main():
    parser = argparse.ArgumentParser(prog="logician")
    parser.add_argument("query", help="Query to ask the assistant")
    args = parser.parse_args()

    orchestrator = RagOrchestrator()
    answer = orchestrator.answer(args.query)
    print(answer)


if __name__ == "__main__":
    main()
