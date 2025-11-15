from setuptools import setup, find_packages

def get_requirements() -> list[str]:
    """
    This function returns the list of requirements for the project.
    """
    requirements_lst:List[str] = []
    try : 
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!='-e .':
                    requirements_lst.append(requirement)
                
    except FileNotFoundError:
        message = f"The requirements.txt file is not found."
        raise FileNotFoundError(message)
    return requirements_lst

setup(
    name = "Groww-Trader",
    version = "0.0.1",
    author = "Rakshit Dabral",
    author_email = "rakshitdabral1@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements(),
    description = "This is a project for the CLI Based Groww Trading",
    long_description = "This is a project for the CLI Based Groww Trading",
    long_description_content_type = "text/markdown",
)