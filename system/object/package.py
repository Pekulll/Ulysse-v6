from system.object.debug import log, warn, error, debug
from subprocess import call
from system.object.color import Color

def verify_package(needed: list = []):
    from pkg_resources import working_set
    installed_packages_name = [str(pkg.key) for pkg in  working_set]
    missing_package = []

    for package in needed:
        if not installed_packages_name.__contains__(package.lower()):
            missing_package.append(package)
            warn(f"[SYSTEM] Package '{package}' is missing!")
    
    return missing_package


def install_package(packages: list = []):
    succeed = True
    
    log("Checking for pip's update...")
    call(["python", "-m", "pip", "install", "--upgrade", "pip"], shell=False)
    
    for package in packages:
        return_code = call(["python", "-m", "pip", "install", package], shell=False)
        
        if return_code == 1:
            error(f"[SYSTEM] The auto-installation of the package '{package}' has failed! Please check out: {Color.URL}ulysse.ia{Color.END} to solve this issue.")
            succeed = False
        else:
            log(f"[SYSTEM] Package '{package}' had been installed.")

    return succeed