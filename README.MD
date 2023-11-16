# The liblab llama SDK challenge game!

![The liblab llama game with a llama navigating a maze of fences and trees]()

Welcome to the liblab llama SDK challenge game! Your goal is to lead the llama home, collecting as many berries on the way that you can.

The llama is controlled by an API, but as a developer who values great developer experience, your job is to create an SDK first, then use that to control the llama in whichever programming language you feel most comfortable in.

Your tasks:

1. [Launch the game so you can control it via the API using an SDK](#launch-the-llama-game)
1. [Generate the SDK using liblab](#create-the-sdk)
1. [Write the code to control the llama](#control-the-llama)

## Launch the llama game

The llama game is in 2 parts - a frontend application that shows the llama and the game map, and a back end API.

There are 3 ways to run this game - from a [devcontainer](#run-the-game-from-a-dev-container), [locally](#run-the-game-locally), and from a [docker container](#run-the-game-from-a-docker-container).

### Run the game from a dev container

If you open this repo in an IDE that supports dev containers (such as VS Code or GitHub codespaces), then once you open the container, everything will be installed and configured for you.

To start the frontend and API, run the following script:

```bash
./scripts/start-game.sh
```

Stop the game running using `ctrl+c`. This will terminate both the front and and API.

### Run the game locally

To run the game locally, you will need to install some Python packages and run the frontend via NPM.

1. Make sure you have NPM and Python installed locally. You will need a recent version of NPM and Python 3.8 or higher.
1. For the frontend, install the NPM packages:

    ```bash
    cd frontend
    npm install
    ```
1. For the API, you will need to install some Python packages. The recommended way is via a virtual environment:

    ```bash
    cd api
    python -m venv .venv
    source ./.venv/bin/activate
    ```

1. Once you have your virtual environment created and activated, install the packages:

    ```bash
    pip install -r requirements.txt
    ```

1. You can now run the game with the following helper script:

    ```bash
    ./scripts/start-game.sh
    ```

Stop the game running using `ctrl+c`. This will terminate both the front and and API.

### Run the game from a Docker container

You can also create a docker container that the game runs in. This container runs both the front end and the API.

To run the container, you need docker and docker compose installed. You can then build and start the container using:

```bash
docker compose up
```

## Create the SDK

Once the game is running, you will need to generate an SDK to play the game. To do this, you will be using [liblab](https://liblab.com). You can learn more about liblab and the steps to create an SDK in the [liblab documentation](https://developers.liblab.com).

liblab takes an API specification and uses that to build the SDK. This specification can be loaded from the API whilst it is running - you can see it at [localhost:8001/openapi.json](http://localhost:8001/openapi.json).

### Install the liblab CLI

You can install the liblab CLI using NPM:

```bash
npm install -g liblab
```

This will install the latest version of the liblab CLI. Next you will need to log in:

```bash
liblab login
```

If you don't have a liblab account yet, you will be able to create one as part of the login step.

### Create a liblab config file

liblab is configured using a JSON file called [`liblab.config.json`](https://developers.liblab.com/cli/config-file-overview/). This contains the configuration for the SDK you want to generate, such as the programming languages you want SDKs in, and the location of the API spec that the SDK is built from.

You can create this file using the following command:

```bash
liblab init
```

This will create the config file in the current folder, so run this from where you want the SDK to be generated.

The default config file has a lot of options you don't need here, so open it in a text editor and change the contents to the following:

```json
{
  "sdkName": "llama-game",
  "specFilePath": "http://localhost:8001/openapi.json",
  "languages": [
    "python"
  ],
  "createDocs": true
}
```

This will generate a Python SDK, and for the rest of this guide we will use Python. If you want to use a different programming language or multiple languages than python to control the game, you can update the `languages` section accordingly. See [the liblab config file docs](https://developers.liblab.com/reference/language-support/) for the available options. The code samples below should be simple enough to convert to the programming language of your choice.

To generate the SDK, run the following command:

```bash
liblab build
```

This will download the spec from the API, and send it to liblab along with the config file, then generate the SDK.

> The llama game API must be running for this command to work. If you get the following error: 
>
> ```bash
> Error: There was a problem fetching or finding the spec file
> ```
>
> Then the API is not running and needs to be started.

The SDK will be generated and downloaded to the `output` folder, in a subfolder for the SDK language(s) in the config file. You can then use this SDK to control the llama. Docs will also be created, and you can use these to help you control the llama using the SDK.

## Control the llama

The aim of the game is to write code to get the llama safely to the pen on the right hand side of the screen, collecting as many berries as possible on the way.

The steps you need to take are:

1. Create the llama game SDK client
1. Create a llama
1. Add steps that the llama should take to get to the pen
1. Run the steps to move the llama
1. Output the result

You can refer to the SDK docs that are generated to help you do this!

## Learn more

liblab generates high-quality, developer friendly SDKs in multiple languages. Learn more from the following:

- [Learn about liblab](https://liblab.com)
- [Read our documentation](https://developers.liblab.com)
- [Read our blog](https://blog.liblab.com)
- [Join our Discord](https://discord.gg/F8aECHbRkV)
- [Follow us on Twitter](https://twitter.com/liblaber)
- [Connect with us on LinkedIn](https://www.linkedin.com/company/liblaber)
- [Watch our videos on YouTube](https://youtube.com/@liblaber)
