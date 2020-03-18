# rpReport

Given a collection or a single rpSBML file generate a CSV output with all the BRS information in it

## Getting Started

This is a docker galaxy tools, and thus, the docker needs to be built locally where Galaxy is installed. 

## Input

Required information:
* **-input**: (string) Path to either tar.xz input collection of rpSBML files or a single rpSBML file.
* **-input_format**: (string) Format of the input (tar or sbml)

Advanced options:
* **-pathway_id**: (string, default: rp_pathway) The SBML groups ID that points to the heterologous reactions and chemical species.

## Output

* **output**: (string) Path to the output CSV file

## Dependencies

* Base Docker Image: [brsynth/rpbase](https://hub.docker.com/r/brsynth/rpbase)

## Installing

To build the image using the Dockerfile, use the following command:

```
docker build -t brsynth/rpreport-standalone .
```

### Running the tests

To run the test, untar the test.tar.xz file and run the following command:

```
python run.py -input test/test_in.tar -input_format tar -output test/test_output.tar
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

v0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thomas Duigou
* Joan Hérisson

### How to cite rpReport?
