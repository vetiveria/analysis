<br>

Analysis of [spots'](https://github.com/vetiveria/spots) outputs.

<br>

* [Development Environment](#development-environment)
* [Notes](#notes)

<br>

## Development Environment

Locally, it uses the development environment `environment`; the environment is detailed within [spots](https://github.
com/vetiveria/spots#development-environment).  The `requirements.txt` file is created via

```shell
    pip freeze -r docs/filter.txt > requirements.txt
```

And, `.pylintrc` is created via command

```shell
    pylint --generate-rcfile > .pylintrc
```

<br>
<br>

## Notes

``generator = np.random.default_rng(seed=0)``