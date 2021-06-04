# First Bazel Project
Following the O'Reilly tutorial found [here](https://learning.oreilly.com/library/view/beginning-bazel-building/9781484251942/A481224_1_En_3_Chapter.html).


## Add `WORKSPACE` file
- This file should be placed at the root of the Bazel project
- All paths specified will be relative to this file
- Bazel will create new sub-directories in the same location as the `WORKSPACE` directory

The `WORKSPACE` file allows you to:
- Add remote code from repositories to your workspace
- Add new rules for compiling in different languages

---

## Add source code
- Created a `HelloWorld.java` file under `src/` dir
- Define the `HelloWorld` build target inside the `src/BUILD.bazel` file
```python
java_binary(
      name = "HelloWorld",
      srcs = ["HelloWorld.java"],
)
```

Now, when running `bazel build src:HelloWorld`, we get the output:
```
INFO: Analyzed target //src:HelloWorld (23 packages loaded, 667 targets configured).
INFO: Found 1 target...
Target //src:HelloWorld up-to-date:
  bazel-bin/src/HelloWorld.jar
  bazel-bin/src/HelloWorld
INFO: Elapsed time: 17.314s, Critical Path: 4.11s
INFO: 7 processes: 4 internal, 2 darwin-sandbox, 1 worker.
INFO: Build completed successfully, 7 total actions
```

And now, in our project root, we see the bazel generated directories:
```
WORKSPACE               bazel-bin               bazel-first_bazel_proj  bazel-out               bazel-testlogs          notes.md                src/
```

Note: Creating a single binary is fine, but not practical for development. We want to seperate our programs into finer grain components due to the following advantages:
- more shareable
- easier to test
- faster to build
- easier to optimize the build

Now, we create a file `IntMultiplier.java` and attempt to use it within `HelloWorld.java`. 
When we run:
```
bazel run src:HelloWorld
```
we get:
```
INFO: Analyzed target //src:HelloWorld (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
ERROR: /Users/amedrano/playground/first_bazel_proj/src/BUILD.bazel:1:12: Building src/HelloWorld.jar (1 source file) failed: (Exit 1): java failed: error executing command external/remotejdk11_macos/bin/java -XX:+UseParallelOldGC -XX:-CompactStrings '--patch-module=java.compiler=external/remote_java_tools_darwin/java_tools/java_compiler.jar' ... (remaining 15 argument(s) skipped)
src/HelloWorld.java:4: error: cannot find symbol
        IntMultiplier im = new IntMultiplier(3, 4);
        ^
  symbol:   class IntMultiplier
  location: class HelloWorld
src/HelloWorld.java:4: error: cannot find symbol
        IntMultiplier im = new IntMultiplier(3, 4);
                               ^
  symbol:   class IntMultiplier
  location: class HelloWorld
Target //src:HelloWorld failed to build
Use --verbose_failures to see the command lines of failed build steps.
INFO: Elapsed time: 0.349s, Critical Path: 0.19s
INFO: 2 processes: 2 internal.
FAILED: Build did NOT complete successfully
FAILED: Build did NOT complete successfully
```
The error is: 
```
error: cannot find symbol IntMultiplier im = new IntMultiplier(3, 4);
```

Bazel will not find everything automatically. There is nothing implicit. You have to explicitly specify everything. We can do this in two ways:
- Add `IntMultiplier` into the list of `srcs` for the build target
- Create a new library and add the `IntMultiplier` to it. Then make the build target (`java_binary`) depend on it. 

For the first case, we do:
```
java_binary(
      name = "HelloWorld",
      srcs = [
           "HelloWorld.java",
           "IntMultiplier.java",
      ],
)
```

Although this works, it is sub-optimal since `IntMultiplier` it is not specific to the `HelloWorld` binary and it can easily be reused in other places. It is locked into the `HelloWorld` binary as of now.

If other targets want to use `IntMultiplier`, then they'll also have to add it as a source which wouldn't look clean. It makes more sense to add it into a general library.  

For the second case, we will create a separate dependency. We will introduce a new type of build target, `java_library`. This target is meant to contain some shared collection of Java functionality. With the `java_library`, other build targets will be able to depend on it. 

Let's define the library:
```
java_library(
       name = "LibraryExample",
       srcs = ["IntMultiplier.java"],
)
```

Now, we can make the `HelloWorld` binary target depend on the `LibraryExample` library target we created:
```
java_binary(
      name = "HelloWorld",
      srcs = [
           "HelloWorld.java",
      ],
      deps = [
          ":LibraryExample",
      ]
)
```