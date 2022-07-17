This repo has been forked from https://github.com/caseychu/spotify-backup
==============

spotify-backup
==============

A Python script that exports all of your Spotify playlists, useful for paranoid Spotify users like me, afraid that one day Spotify will go under and take all of our playlists with it!

1. [Get Access token](https://accounts.spotify.com/authorize?response_type=token&client_id=5c098bcc800e45d49e476265bc9b6934&scope=playlist-read-private+playlist-read-collaborative+user-library-read&redirect_uri=http%3A%2F%2F127.0.0.1%3A43019%2Fredirect)

2. Copy URL to which your browser has been redirected to clipboard

3. Paste URL as value for variable `SPOTIFY_REDIRECT_URL` in manual pipeline step in Gitlab

