# PTTT
Working area for the Protocol Transition Tiger Team



## Generating code from OpenAPI specification

This project uses the [OpenAPI Generator](https://openapi-generator.tech/) project to generate server/client code examples from the OpenAPI specifications. Configuration options for generating code can be found in the service's `/configs/` directory. Supported languages and frameworks can be found at [OpenAPI Generator#Generators](https://openapi-generator.tech/docs/generators).

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

The code output of OpenAPI Generator can be customized using mustache templates, stored in the `/templates/generators/` directory. See [TEMPLATES.md](/templates/TEMPLATES.md) for more information on how to use these templates.

