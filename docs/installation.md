# Installation

Aleph requires a couple of services in order to operate. To make it easier
for development and deployments it uses Docker containers. Below you will find
the installation steps on how to install Aleph locally for development and
production environment.

## Prerequisites

Before we continue, you will need to have Docker and `docker-compose`
installed. Please refer to their manual to learn how to set up
[Docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

You will also need to adapt a configuration to provide some credentials
for the external services. This includes the OAuth credentials to allow
Google users to login to Aleph and an email server credentials. Email
server support is optional for development purposes.

Inside the same repository you will find a file called `aleph.env.tmpl`.
This is a template of the configuration file. Make a copy of this file named
`aleph.env` and follow the steps below to edit it.

To get the OAuth credentials please visit the [Google Developers Console](https://console.developers.google.com/).
There you will need to [create an API key](https://support.google.com/googleapi/answer/6158862).
In the **Authorized redirect URIs** section, use this URL:

```
http://localhost:8080/api/1/sessions/callback/google
```

Save the client ID and the client secret as `ALEPH_OAUTH_*` values.

Finally you will need to provide a value for the `ALEPH_SECRET_KEY`. A good
example of a value is the output of `openssl rand -hex 24`.

## Development installation steps

Insider the Aleph repository you will find a `Dockerfile` and a
`docker-compose.dev.yml` files. These are used to build a container with the
application and start the relevant services.

For ElasticSearch, you need to run: 

```
sysctl -w vm.max_map_count=262144
```

Or to set this permanently, in `/etc/sysctl.conf` add:

```
vm.max_map_count=262144
```

Then, to proceed run:

 1. `make build` to start the application and relevant services. You can
    leave this open to have access to the development logs.
 2. `make upgrade` to run the latest database migrations and create/update
    any indexes.
 3. `make web` to run the web-based API server and the user interface.
 4. Open `http://localhost:8080/` in your browser to visit the application.

Your repository is mounted inside the docker container under the name
`aleph_app`. You can access these services anytime by running `make shell`.

### Building from a clean state

You can also build the Aleph images locally. This could be useful while working
on the Dockerfile changes and new dependency upgrades.

To build the image you can run `make build`, which will
build the `alephdata/aleph` image (this will generate a production ready image).

## Production deployment

Aleph runs on PostgreSQL and ElasticSearch along with a couple of system
tools like ImageMagik, Tesseract. For a full list of system dependencies
please review the [`aleph_base` Dockerfile](https://github.com/alephdata/aleph/blob/master/Dockerfile).

If you decide to not use Docker compose, you will have to provide all these
dependencies and services and change the configuration file accordingly.
An application only Docker image is also available at
[`alephdata/aleph`](https://hub.docker.com/r/alephdata/aleph/).

Finally, aleph is optimized to use certain Amazon Web Services: SQS and S3. To
enable AWS features, you will need to set the AWS key ID and access key in the
configuration file. Amazon SQS support is available for task queueing. Where
S3 is available for file uploads.

### Upgrading

Aleph does not provide automatic upgrades. You will have to download the new
version Docker images or checkout the latest version using Git first.

Once you have the latest version, you can run the command bellow to upgrade
the existing installation.

```
make upgrade
```

## Configuration

Most of the Aleph configuration is handled via a set of environment values, which are
read by Aleph inside of docker. They are set using the ``aleph.env`` file, and can be
edited locally.

## Users

For development purposes, you can quickly create a new user with the
`aleph createuser` command, inside a shell (`make shell`):

```
aleph createuser --email="user@example.com" --name="Alice" --is_admin=True userid123
```

If you pass an email address in the `ALEPH_ADMINS` environment variable (in your
`aleph.env` file) it will automatically be made admin.

The user's API key is returned.

## Running tests

To run the tests, assuming you already have the `docker-compose` up and ready,
run `make test`.

This will create a new database and run all the tests.

The test settings can also be configured by making a copy of the
`test_settings.py.tmpl` file to `test_settings.py` and editing it to
match your configuration. You must then set the environment
variable ``ALEPH_TEST_SETTINGS`` to point to the absolute path of that
settings file.
