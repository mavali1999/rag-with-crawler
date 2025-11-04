import os


def save_markdown(save_location, markdown):

    assert isinstance(markdown, str)

    save_location += ".md"
    os.makedirs(os.path.dirname(save_location), exist_ok=True)
    with open(save_location, "w", encoding='utf-8') as f:
        f.write(markdown)
