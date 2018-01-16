# Dependencies

The sunfounder libraries are added as a submodule, you may either directly clone the whole project
```
git clone --recurse-submodules <url>
```
or you may first clone the project without submodules and later get the submodules
```
git clone <url>
...
git submodule init
git submodule update
```


# Run

Nothing yet

# Git policy

Always obey the following rule :

**Do not touch master ! Master should be the branch that should always work. Merge with it only, if everything is working.**

When initiating a new feature, create a branch named **<member name>-<feature name>** starting from master. Merge only once you have validated the feature with tests. If you need subbranches name the branch **<member name>-<feature name>-<subfeature name>**.


