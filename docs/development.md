# Working on the code

## Ground rules

- **The client is the spec.** We're building a server for the original client,
  not changing the client to suit the server. Only touch client code when
  there's no other way, and say why in the commit.
- **Write it the way the original developers would have.** Follow the naming,
  structure and comment style of the code around you: `d_`/`b_` senders,
  `notify` categories, FSMs, `self.air.writeServerEvent` for suspicious input.
- **No auto-formatters.** The code is formatted by hand; don't run autopep8,
  black or similar over it.
- **Don't strip "unused" code.** A lot of it is the original game's and is used
  somewhere you haven't found yet.
- **Never trust a `clsend` field.** Check the sender (`getAvatarIdFromSender`),
  the state they're in, and every argument before acting, and log anything
  impossible with `logPotentialHacker`.

## Adding a feature

1. Find the field in `astron/dclass/pirates.dc`, and find where the client sends
   or expects it (search the client class without a suffix).
2. Implement the server half in the `AI` or `UD` class, mirroring what the
   client does.
3. Add a test under `tests/`, laid out like the source tree
   (`tests/pirates/quest/...` for `pirates/quest/...`).
4. Run the game and try it.

### dclassesByName and suffixes

`self.air.dclassesByName` is keyed by the class name **as the process sees it**.
On the AI that's `'DistributedPlayerPirateAI'`, on the UberDOG
`'DistributedPlayerPirateUD'`. A class without a view for that process (for
example `DistributedDinghy/AI`, which has no UD class) is keyed by whichever
suffix was found, so `dclassesByName['DistributedDinghy']` is a `KeyError` on
the UberDOG. When you need a dc class to format a message, the reliable lookup
is `self.air.getDcFile().getClassByName('DistributedDinghy')`.

## Tests

```bash
python3 -m pip install pytest
```

```bash
python3 -m pytest -q
```

Run them from the repository root. The suite is fast (well under a minute) and
needs no running servers: tests build the objects they need with mocks and pack
fields against the real dc files, so a field that doesn't match the dc fails
there.

## Commits

Prefix the message with the area it touches, then say in lowercase what's true
now:

```
pirates/npc: darby drydock's closing dialog waits for the tutorial ship to be built
pirates/quest: the ship reward always gives the new ship token
astron/databases: ignore the code redemption bridge database
```

Keep one change per commit, and don't commit `config/personal.prc`, the
databases in `astron/databases/`, or logs.

## Branches

| Branch | Purpose |
|---|---|
| `master` | Stable. |
| `develop` | Active development and experiments. |
| `qa` | The internal test server. |
| `verify` | Client verification and bytecode matching. |

Open pull requests against `develop` unless you're asked otherwise. A pull
request is merged after two other contributors have reviewed it. Emergency and
security fixes need one review.

## Project layout

```
pirates-online-classic/
├── astron/
│   ├── config/        astrond.yml: ports, UberDOG objects, database backend
│   ├── dclass/        otp.dc, pirates.dc: every networked class and field
│   ├── databases/     Astron and UberDOG data (git-ignored)
│   ├── logs/          event logs
│   └── darwin/ linux/ win32/   server launch scripts
├── config/            .prc settings (see configuration.md)
├── darwin/ win32/     client launch scripts
├── docs/              these docs
├── libotp/ libpirates/  Python versions of the original C++ helpers (nametags, …)
├── otp/               the OTP framework: login, chat, friends, magic words
├── pirates/           the game, client and server code side by side
└── tests/             pytest suite, mirroring the source tree
```
