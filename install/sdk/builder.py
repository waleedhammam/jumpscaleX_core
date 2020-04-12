def start():
    """
    build the threebot container
    """
    jsx.tfgrid_simulator.callback(name)


def shell(name="simulator"):
    """
    Shell for simulator
    """
    jsx.container_shell.callback(name)


def kosmos(name="simulator"):
    """
    Start kosmos shell on simulator
    """
    jsx.kosmos.callback(name)


# def builder(push=False, base=False, delete=False, noclean=False, development=False):
#     """
#     create the 3bot and 3botdev images
#     """
#     if base:
#         basebuilder_(push=push)
#     dest = "threefoldtech/3bot2"
#
#     docker = e.DF.container_get(name="3botdev", delete=delete, image="threefoldtech/base2")
#
#     docker.install(update=delete, stop=delete)
#
#     # we know its a ubuntu 19.10 so we can install
#
#     installer = IT.JumpscaleInstaller()
#     installer.repos_get(pull=False)
#
#     docker.install_jumpscale(force=delete, pull=False, threebot=True, identity="build", reset=True)
#     # because identity==build the secret will be build
#     # the hex/hashed repr of the secret: 'b0da275520918e23dd615e2a747528f1'
#
#     docker._install_tcprouter()
#     docker.install_jupyter()
#     # docker.execute("rm  /sandbox/bin/micro;cd /tmp;curl https://getmic.ro | bash;mv micro /sandbox/bin")
#     docker.execute("apt install restic -y")
#     docker._install_package_dependencies()
#
#     docker.image = dest
#
#     if noclean:
#         docker.save(image=dest)
#         docker.delete()
#     else:
#         docker.save(development=development, image=dest, code_copy=True, clean=True)
#
#     if push:
#         docker.push()
#
#     print(" - *OK* threebot container has been built, as image & exported")
#     print(" - if you want to test the container do 'jsx container-shell -d'")
#     print(" - if you want to push you can do 'jsx container-save -p -cd' after playing with it.")
#
#
# def _build_phusion(push=False):
#     path = IT.Tools.text_replace("{DIR_BASE}/code/github/threefoldtech/baseimage-docker")
#     if not os.path.exists(path):
#         IT.Tools.code_github_get(url="https://github.com/threefoldtech/baseimage-docker", branch="master")
#     cmd = """
#         set -ex
#         cd {}/image
#         docker build . -t threefoldtech/phusion:latest
#     """.format(
#         path
#     )
#     IT.Tools.execute(cmd, interactive=True)
#     if push:
#         IT.Tools.execute("docker pushe threefoldtech/phusion/latest")
#
#
# def basebuilder_(dest=None, push=False, delete=True):
#     _build_phusion(push=push)
#     if not dest:
#         dest = "threefoldtech/base2"
#
#     # image = "threefoldtech/phusion:19.10"
#     image = "threefoldtech/phusion:latest"
#     docker = e.DF.container_get(name="base2", delete=delete, image=image)
#     docker.install(update=True, stop=delete)
#     cmd = "apt install python3-brotli python3-blosc cython3 cmake -y"
#     docker.dexec(cmd)
#     docker.save(image=dest, clean=True)
#     if push:
#         docker.push()
#         if delete:
#             docker.stop()
#     print("- *OK* base has been built, as image & exported")