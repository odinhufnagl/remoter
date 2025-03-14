def test_package_import():
    import remoter


def test_package_run():
    import remoter

    remoter.run(lambda x: x * 2, 10)


def test_mount_folder():
    import remoter

    remoter.mount_folder("path", "remote_path")


def test_remoter_function_return_file():
    import remoter

    remoter.remote_functions.return_file("file_path")
