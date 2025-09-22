from logician.rag import RagOrchestrator


def test_rag_smoke():
    r = RagOrchestrator()
    ans = r.answer("Why did my deployment fail?")
    assert isinstance(ans, str)
