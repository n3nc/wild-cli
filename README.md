# Wildebeest CLI

Official CLI for Wildebeest for N3NCLOUD, accessible using a command line tool implemented in Python 3.

Wildbeest is a CKAN-based solution for building data portals that share public data by DCAT standards. Wildbeest provides the most efficient disclosure of registered datasets and standard protocols for sharing data with other data catalog systems. Wildbeest uses the most compatible standard format and is the best solution for global data sharing. You can get more information on the [Wildebeest Documents](http://d3.n3ncloud.co.kr/wildebeest/1.0) and [N3NCLOUD](https://www.n3ncloud.co.kr/).
## Installation

Ensure you have Python 3 and the package manager `pip` installed.

Run the following command to access the Wildebeest CLI using the command line:

We are using **'wild'** for this cli package name.

`pip install wild` (You may need to do `pip install --user wild` on Mac/Linux.  This is recommended if problems come up during the installation process.) Installations done through the root user (i.e. `sudo pip install wild`) will not work correctly unless you understand what you're doing.  Even then, they still might not work.  User installs are strongly recommended in the case of permissions errors.

You can now use the `wild` command as shown in the examples below.

If you run into a `wild: command not found` error, ensure that your python binaries are on your path.  You can see where `wild` is installed by doing `pip uninstall wild` and seeing where the binary is.  For a local user install on Linux, the default location is `~/.local/bin`.  On Windows, the default location is `$PYTHON_HOME/Scripts`.

IMPORTANT: We do not offer Python 2 support.  Please ensure that you are using Python 3 before reporting any issues.

## API credentials

To use the Wildebeest CLI, sign up for a Wildbeest account at your site. Then go to your user profile (`https://[site url]/user/<username>`) and select 'Manage' and click 'Regenerate API Key'. This will regenerate your API Key and bring you back to account page then you can find your API Key bottom-left corner of the page. Then you have to export your Wildbeest Server URL and API key to the environment.

Environment:
```bash
export WB_SERVER_URL=http://[your-site-url]
export WB_API_KEY=[your-api-key-string]
```
Example:

```bash
export WB_SERVER_URL=http://127.0.0.1
export WB_API_KEY=e2806328-af09-41b2-b389-3fd78645fdcb
```

## Commands

The command line tool supports the following commands:

```
$ wild organizations {list | show | datasets}
$ wild datasets {list | show | search | resources | download}
$ wild resource {show | download}
```

See more details below for using each of these commands.

### Organizations

The Command supports the following commands for Wildebeest Organizations.

```
usage: wild organizations [OPTIONS] COMMAND

optional arguments:
  -h, --help            show this help message and exit

commands:
  list                  List available organizations
  show                  Show the detail of a organization
  datasets              List datasets of a organization
```

##### List organizations

```
usage: wild organizations list [-h]

optional arguments:
  -h, --help            show this help message and exit
```

Example: 

```bash
$ wild organizations list
$ wild o l
```
##### Show organization detail

```
usage: wild organizations show [-h] [organization-name]

optional arguments:
  -h, --help            show this help message and exit
  organization-name     Organizations Name (use "wild organizations list" to show options)
```

Example:

```bash
$ wild organization show n3ncloud
$ wild o s n3ncloud
```

##### List datasets

```
usage: wild organizations datasets [-h] [organization-name]

optional arguments:
  -h, --help            show this help message and exit
  organization-name     Organizations Name (use "wild organizations list" to show options)
  -p, --page            Page number for results paging. Page size is 20 by default
```

Examples:

```bash
$ wild organizations datasets n3ncloud --page 2
$ wild o d n3ncloud -p 2
```
### Datasets

The Command supports the following commands for Wildebeest Datasets.

```
usage: wild datasets  [OPTIONS] COMMAND

optional arguments:
  -h, --help            show this help message and exit

commands:
  list                  List available datasets
  show                  Show the detail of a dataset
  search                Search datasets by query or keyword
  resources             List the resources of a dataset
  download              Download resource files of a dataset
```

##### List datasets

```
usage: wild datasets list [-h] [-p PAGE]

optional arguments:
  -h, --help            show this help message and exit
  -p PAGE, --page PAGE  Page number for results paging. Page size is 20 by default
```

Example:

```bash
$ wild datasets list
$ wild d l -p 2
```

##### Show dataset detail

```
usage: wild datasets show [-h] [dataset]

optional arguments:
  -h, --help            show this help message and exit
  dataset               Dataset Id (use "wild datasets list" to show options)
```

Example:

```bash
$ wild datasets show 01631b54-16a3-4a84-8dac-3e8d142e12b9
$ wild d sh 01631b54-16a3-4a84-8dac-3e8d142e12b9
```

##### Search specific datasets

```
usage: wild datasets search [-h] [-p PAGE] [query]

optional arguments:
  -h, --help            show this help message and exit
  -p PAGE, --page PAGE  Page number for results paging. Page size is 20 by default
  query                 Query string what you want to find in datasets
```

Example:

```bash
$ wild datasets search 'cloud platfrom'
$ wild d s 'cloud platform' -p 2
```

##### List dataset resources

```
usage: wild datasets resources [-h] [dataset]

optional arguments:
  -h, --help            show this help message and exit
  dataset               Dataset Id (use "wild datasets list" to show options)
```

Example:

```bash
$ wild datasets resources 01631b54-16a3-4a84-8dac-3e8d142e12b9
$ wild d r 01631b54-16a3-4a84-8dac-3e8d142e12b9
```

##### Download dataset resources

```
usage: wild datasets download [-h] [-f FILE_NAME] [-p PATH] [-w] [--unzip]
                                [-o] [-q]
                                [dataset]

optional arguments:
  -h, --help            show this help message and exit
  dataset               Dataset Id (use "wild datasets list" to show options)
```


Examples:

```bash
$ wild datasets download 01631b54-16a3-4a84-8dac-3e8d142e12b9
$ wild d d 01631b54-16a3-4a84-8dac-3e8d142e12b9
```

### Resource

The Command supports the following commands for Wildebeest Resource.

```
usage: wild resource  [OPTIONS] COMMAND

optional arguments:
  -h, --help            show this help message and exit

commands:
  show                  List available kernels
  download              Initialize metadata file for a kernel
```

##### Show resource detail

```
usage: wild resource show [-h] [resource]

optional arguments:
  -h, --help            show this help message and exit
  resource              Resource Id (use "wild datasets resources" to show options)

```

Example:

```bash
$ wild resource show 13325edd-3d64-4e2a-a7e3-30e84ae017ab
$ wild r s 13325edd-3d64-4e2a-a7e3-30e84ae017ab
```

##### Download a resource

```
usage: wild resource download [resource]

optional arguments:
  -h, --help            show this help message and exit
  resource              Resource Id (use "wild datasets resources" to show options)
```

Example:

```bash
$ wild resource download 13325edd-3d64-4e2a-a7e3-30e84ae017ab
$ wild r d 13325edd-3d64-4e2a-a7e3-30e84ae017ab
```

## License

The wild(Wildebeest) CLI is released under the [Apache 2.0 license](LICENSE).