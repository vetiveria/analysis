## Segments

Analysis of [spots'](https://github.com/vetiveria/spots) outputs.

<br>

### Development Environment

In preparation for Docker, etc.

#### Anaconda

Refer to [spots](https://github.com/vetiveria/spots#development-environment)

<br>

#### Requirements

In relation to requirements.txt

```markdown
    pip freeze -r docs/filter.txt > requirements.txt
```

<br>

#### Conventions

```markdown
    pylint --generate-rcfile > .pylintrc
```

<br>
<br>

### Notes

``generator = np.random.default_rng(seed=0)``