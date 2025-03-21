def test_package_import():
    import remoter


def test_set_api_key():
    import remoter

    remoter.set_api_key("api_key")


def test_package_run():
    import remoter

    remoter.run(lambda x: x * 2, 10)


def test_mount_folder():
    import remoter

    remoter.mount_folder("path", "remote_path")
