Summary — Running spotify-backup.py headless in GitLab CI

Goal
- Run `spotify-backup.py` non-interactively in CI by providing a redirect URL that contains the authorization code (`?code=...`) and the original PKCE `code_verifier` so the script can exchange the code for an access token.

One-time (local) steps
1. Generate a PKCE pair (verifier + challenge) locally and save the verifier securely:

```bash
python3 - <<'PY'
import secrets, string, hashlib, base64
chars = string.ascii_letters + string.digits
verifier = ''.join(secrets.choice(chars) for _ in range(64))
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
print(verifier)   # save as code_verifier
print(challenge)  # use as code_challenge in auth URL
PY
```

2. Build and open the Spotify authorization URL in a browser (replace CLIENT_ID and CODE_CHALLENGE):

```
https://accounts.spotify.com/authorize?response_type=code&client_id=CLIENT_ID&scope=playlist-read-private+playlist-read-collaborative+user-library-read&redirect_uri=http%3A%2F%2F127.0.0.1%3A43019%2Fredirect&code_challenge_method=S256&code_challenge=CODE_CHALLENGE
```

3. After logging in Spotify will redirect to a URL like:

```
http://127.0.0.1:43019/redirect?code=AUTH_CODE&state=...
```

Copy that full redirect URL (it contains `?code=AUTH_CODE`).

CI setup (GitLab)
1. Add two CI/CD variables in your project (Settings → CI/CD → Variables):
- `SPOTIFY_REDIRECT_URL` — set to the full redirect URL copied above (e.g. `http://127.0.0.1:43019/redirect?code=...`).
- `PKCE_CODE_VERIFIER` — set to the `verifier` you generated earlier.

Mark `PKCE_CODE_VERIFIER` as Masked and Protected.

2. Ensure your `.gitlab-ci.yml` calls the script with `--redirect-url` as already configured. Example job snippet:

```yaml
get_data:
  stage: gather
  script:
    - python spotify-backup.py --format=json --dump=liked --redirect-url="$SPOTIFY_REDIRECT_URL" liked.json
    - python spotify-backup.py --format=json --dump=playlists --redirect-url="$SPOTIFY_REDIRECT_URL" playlists.json
```

The script will read `PKCE_CODE_VERIFIER` from the environment and perform the token exchange headlessly.

Local test
```bash
export PKCE_CODE_VERIFIER='the_verifier_from_step1'
python3 spotify-backup.py --redirect-url 'http://127.0.0.1:43019/redirect?code=THE_AUTH_CODE' --format=json --dump=liked liked.json
```

Notes & recommendations
- The manual authorization (opening the URL and copying the redirect) is a one-time step per refresh token lifecycle.
- Keep `PKCE_CODE_VERIFIER` secret; store as masked/protected variable in GitLab.
- If you want to avoid the hardcoded client id, add a `--client-id` script option and store the client id in CI variables.
- If you need a fully automated browserless flow, that requires additional tooling (headless browser or OAuth client automation) and is outside the scope here.

Troubleshooting
- If the job fails with "could not extract access_token or code", verify `SPOTIFY_REDIRECT_URL` contains `?code=` and that `PKCE_CODE_VERIFIER` is set.
- Use the local test command above to debug before committing.
