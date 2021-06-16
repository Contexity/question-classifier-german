
(Part of the [Question Classifier for German](https://github.com/Contexity/question-classifier-german) project).


# Sentence Analysis Service

Simple implementation of a service that analyzes text and returns information on whether it contains German question words, or phrases the syntax of which is indicative of a question formulation.

## Prerequisites

This implementation requires an additional, external service that performs the analysis of the text and returns a CoNLL-U table for each of the sentences contained in the text. It is expected that the returned table(s) conform to the labeling scheme used for spacy's German models (https://spacy.io/models/de ).

Please see the sample spacy-based implementation for such a service, provided elsewhere in this distribution.

## Building and running

To build and run this service you need to have Java (at least a recent version of 1.8) installed on your system. 

Building:

* Linux / Mac:

	```
	./mvnw clean package
	```
	
* Windows:

	```
	.\mvnw.cmd clean package
	```
	
Running:

* Linux / Mac:

	```
	java -jar target/sentence-analyzer-**<version>**.jar
	```
	
* Windows:

	```
	java -jar target\sentence-analyzer-**<version>**.jar
	```
	
Note that **<version>** in the above example may vary over time, please check what the generated `.jar` file in the `target` directory is named after compilation.
	

## Configuration

The main configuration parameters supported at the moment can be found in `src/main/resources/properties/application.properties` and include:

* `server.port`: the port on which this service will be running
* `services.conllu.url`: the URL at which the text analysis service that return CoNLL-U can be reached

