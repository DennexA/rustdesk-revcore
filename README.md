# RustDesk client — RevCore (`remote.r3v.ro`)

OSS build with ID server + public key baked into the binary (no Pro, no exe rename).

## Secrets (GitHub → Settings → Secrets → Actions)

- `RENDEZVOUS_SERVER` = `remote.r3v.ro`
- `RS_PUB_KEY` = public key from hbbs (`id_ed25519.pub`)

## Build

Actions → **Build custom client** → Run workflow → choose platform (default: Windows x64).

Artifacts land on the run page; publish to `https://remote.r3v.ro/downloads/`.
