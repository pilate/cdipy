import requests

import logging



logger = logging.getLogger('chromer.generator')
logger.setLevel(10)
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s")


# EMPTY_CLASS_TPL = "class {name}({type}):"

HEADER = """from .decorators import proxy_target_command


"""

CLASS_TPL = """
class {name}({type}):
    description = \"\"\"
        {desc}
    \"\"\"

"""

COMMAND_TPL = """
    @proxy_target_command
    async def {name}({args}):
        \"\"\"
            {desc}
        \"\"\"

"""

DOMAIN_TPL = """
class {name}(object):

    def __init__(self, devtools):
        self.devtools = devtools

"""


def write_types(outfile, types):
    for _type in types:
        if _type["type"] ==  "string":
            outfile.write(CLASS_TPL.format(
                name=_type["id"],
                type="str",
                desc=_type.get("description", "None")))


def write_commands(outfile, commands):
    for command in commands:
        param_strs = ["self"]
        for param in command.get("parameters", []):
            param_str = param["name"]
            if param.get("optional"):
                param_str += "=None"
            param_strs.append(param_str)


        outfile.write(COMMAND_TPL.format(
            name=command["name"],
            args=", ".join(param_strs),
            desc=command.get("description", "None")))


def write_domain(outfile, domain):
        domain_name = domain["domain"]
        outfile.write(DOMAIN_TPL.format(
            name=domain_name))

        write_commands(outfile, domain.get("commands", []))



def main():
    protocol = requests.get("https://raw.githubusercontent.com/ChromeDevTools/devtools-protocol/master/json/browser_protocol.json").json()

    logger.debug("Generating objects for protocol version {0}.{1}".format(
        protocol["version"]["major"], protocol["version"]["minor"]))

    outfile = open("chromer.py", "w+b")
    for domain in protocol["domains"]:
        outfile = open("domains/{0}.py".format(domain["domain"]), "w+b")

        # write_types(outfile, domain.get("types", []))
        outfile.write(HEADER)
        write_domain(outfile, domain)



main() if __name__ == "__main__" else None