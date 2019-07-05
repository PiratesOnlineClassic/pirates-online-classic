<img src=".github/logo.png" align="center">

# Pirates Online Classic
This is the game development repository for Pirates Online Classic, a fan-made recreation of Disney's now-defunct MMORPG; Pirates of the Caribbean Online.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-git.svg)](https://git-scm.com/) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Merging
All merges should go through a three-step process:

    1. PR goes up by creator when the changes are ready
    2. PR is reviewed by another person
    3. PR is reviewed and merged by a third person

For emergency/security merges, only steps 1/2 are required if time is an issue.

## Verification Guidelines

Eventually we'll begin working on the verification codebase; when this happens we need to follow a set of regulations:

- Don't update deprecations, the goal(currently) is to make it as close to the original as possible.

- If you find code on the client you deem "Unnecessary" don't remove it, don't touch it; If it isn't broken, don't fix it.

- Custom client features that poc previously had(e.g Rich Presence, Various discord integrations, Userfunnel modifications, etc, etc) should not be added back until the codebase is nearing beta release ready.

- Retain originality. In the process of developing on this branch, we may need to alter things to support astron and the csm, we should try to retain as much originality as possible and not modify it out of the scope it needs to make certain things function.

- Do not run autopep formatters or any kind of formatters on the codebase, it's been manually formatted.

If you have anymore questions, ask me.

## Branches

### Master

Master is a branch that's stable, you're not to commit directly to master.

### Develop

Develop is a branch that is used for development purposes, namely it's purpose is for experimental changes and new features, which then get branched off to the QA branch for internal testing. Most temporary developmental branches should be based off this branch.

### QA

QA is a branch that the internal testing server resides on, it's used to push W.I.P features/functionalities and have internal testers test them.

### Verify

The verify branch houses the W.I.P client verification, which to put it in layman terms is a W.I.P complete redecompilation of the client intending to correct every mismatch from the original bytecode to our decompiled source code.

## Commit Guidelines

* Do **NOT** modify the client to benefit the server,  we're creating a server for the client, not a client for the server.

* Please keep your code clean, do not leave extraneous whitespace and use spaces not tabs.

* Give information on your commits, such as `pirates/piratesbase: fix a grammar issue with the localizer`.

* Give commit descriptions when plausible.

* If you're writing a new feature or doing any substantial change, please push it to a seperate branch and make a pull request when you believe it's ready. Refer to the Merging and Branches section for more.

## Requirements
* [Python](https://www.python.org)
* [Panda3D](https://github.com/panda3d/panda3d)
* [Resources](https://gitlab.com/pirates-online-classic/resources)

## Other
* [Bytecode](https://anythingtechpro.github.io/github-pages/classic/dev/2008bytecode.zip)

## License

Pirates Online Classic is licensed under the "BSD 3-Clause" for more information, refer to [LICENSE](LICENSE) file.
