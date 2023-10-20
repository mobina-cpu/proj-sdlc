def test_get_params_from_client(monkeypatch):

    url_input = "https://cs50x.ir/spring/assets/python-ai-spring-1402/week9/Final-Project.pdf"
    path_input = "home/happy"

    monkeypatch.setattr('builtins.input', lambda _: url_input)
    monkeypatch.setattr('builtins.input', lambda _: path_input)

    url, path = get_params_from_client()

    assert url == url_input
    assert path == path_input