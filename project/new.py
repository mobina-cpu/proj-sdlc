from db import Files, session


def add(url, path=None):
    file_kwargs = dict(
        url=url,
    )
    if path is not None:
        file_kwargs['path'] = path

    file = Files(**file_kwargs)
    session.add(file)
    session.commit()


def get_params_from_client():
    url = input('Enter file url:')
    path = input('Enter file path (or leave it blank for default):')
    if not path.strip():
        path = None
    return url, path


if __name__ == '__main__':
    add(*get_params_from_client())

