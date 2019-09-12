# enola

*Bombastic deployments!*

[enola](https://en.wikipedia.org/wiki/Enola_Gay) is a command line tool to execute smarter deployments in cloud environments (starting with GCP).


## Usage

```bash
enola <PRODUCT> <ACTION> [ACTION_ARGS]
```

e.g.,

```bash
enola composer build dev
```


## Architecture

### Cloud Configurations

The repository's root must have a package *gcp*, containing packages for each product. In example above, the package hierarchy must be similar to

```
- gcp
    |- [product_1]
        |- [env_1].json
        .
        .
        .
        |- [env_K].json
    .
    .
    .
    |- composer
        | - dev.json
    .
    .
    .
    |- product_N
        |- ...
```
