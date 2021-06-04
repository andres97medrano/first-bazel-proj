# First Bazel Project
Following the O'Reilly tutorial found [here](https://learning.oreilly.com/library/view/beginning-bazel-building/9781484251942/A481224_1_En_3_Chapter.html).


## Add `WORKSPACE` file
- This file should be placed at the root of the Bazel project
- All paths specified will be relative to this file

The `WORKSPACE` file allows you to:
- Add remote code from repositories to your workspace
- Add new rules for compiling in different languages