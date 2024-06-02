# PTTT
Working area for the Protocol Transition Tiger Team

## Adding a new protocol

For convenience, a [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/README.html) template is provided to help creating a new protocol. cookiecutter is a command-line utility that creates projects from project templates. The template can be found in the `templates/protocol_template` directory.

### Installation

See the [cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/README.html) for installation instructions.

### Usage

Once installed, to create a new protocol from the template, run the following command:

```bash
cookiecutter templates/protocol_template
```

The template will prompt for the following information:
    - The name of the protocol, usually abbreviated (e.g. `UWS`)
    - The directory where the protocol will be generated
    - The full title of the protocol (e.g. `Universal Worker Service (UWS)`)
    - A brief description of the protocol
    - The version of the protocol
    - Contact information for the protocol's working group

Once finished, the template will generate a new directory with the protocol's name in the specified output directory. The directory will contain the following files:
    - `openapi.yaml`: The OpenAPI specification for the protocol, with example paths and responses
    - `README.md`: A README file for the protocol
    - `configs/`: A directory containing example configuration files for generating code from the OpenAPI specification

Additionally, the new OpenAPI specification will be added to the redocly linting configuration file, `.redocly.yaml`.

## Generating code from OpenAPI specification

This project uses the [OpenAPI Generator](https://openapi-generator.tech/) project to generate server/client code examples from the OpenAPI specifications. Configuration options for generating code can be found in the protocol's `/configs/` directory. Supported languages and frameworks can be found at [OpenAPI Generator#Generators](https://openapi-generator.tech/docs/generators).

### Installation

To install the OpenAPI Generator, follow the instructions at [OpenAPI Generator#Installation](https://openapi-generator.tech/docs/installation).

### Generating code

To generate a new code sample from the OpenAPI specification, use the following commands:

If not using the a configuration file, use the following command:
```bash
openapi-generator-cli generate -i <path-to-openapi-spec> -g <generator-name> -o <output-directory>
```

If using a configuration file, use the following command:
```bash
openapi-generator-cli generate -c <path-to-config-file>
```

*Output behavior is specific to the generator used, but generally will overwrite existing files in the output directory.
Use the command line option --skip-overwrite to skip existing files.*

In order to update only files that have been affected by template or OpenAPI specification changes, use the `--minimal-updates` argument:
```bash
output-generator-cli generate -c <path-to-config-file> --minimal-updates
```

#### Customizing code generation

The code output of OpenAPI Generator can be customized using mustache templates, stored in the `/templates/code_generation/` directory. See [TEMPLATES.md](/templates/TEMPLATES.md) for more information on how to use these templates.

