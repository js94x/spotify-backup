This repo has been forked from https://github.com/caseychu/spotify-backup

2025-12: 
* Spotify changed API authorization, changes from this [PR](https://github.com/caseychu/spotify-backup/pull/66) has been backported

==============

spotify-backup
==============

A Python script that exports all of your Spotify playlists, useful for paranoid Spotify users like me, afraid that one day Spotify will go under and take all of our playlists with it!

1. [Open link twice](https://accounts.spotify.com/authorize?response_type=code&client_id=5c098bcc800e45d49e476265bc9b6934&scope=playlist-read-private+playlist-read-collaborative+user-library-read&redirect_uri=http%3A%2F%2F127.0.0.1%3A43019%2Fredirect&code_challenge_method=S256&code_challenge=0Ng0kl3XTL9Bb8wsTgsX-YBODDldSYQyeHgL_7pUi6Q)

2. Copy & Paste URLs (different ones) as value for variable `SPOTIFY_REDIRECT_URL_LIKED` and `SPOTIFY_REDIRECT_URL_PLAYLISTS` in manual pipeline step in Gitlab

