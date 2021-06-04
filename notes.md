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
