from openapi_server.start_app import start_app
import argparse


if __name__ == '__main__':
    # read port from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", type=int, default=8080, help="The port where the tool's API will be exposed")
    args = parser.parse_args()
    start_app(base_path='/spacy', port=args.port)