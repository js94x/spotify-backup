import argparse, json, logging, sys, urllib.parse, os

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')


def _artist_link(name):
    return f"{name}"
    # return f"[{name}](./artists/{urllib.parse.quote(name.replace('/', '_'))}.md)"

def _write_playlist(f, playlist, header):
    f.write(f"{header} {playlist.get('name', 'playlist')}\n\n")
    f.write('|Titel|Artist(s)|Album|\n|---|---|---|\n')
    for item in playlist.get('tracks', []):
        tr = item.get('track') if isinstance(item, dict) else None
        if not tr:
            continue
        artists = ', '.join(_artist_link(a['name']) for a in tr.get('artists', []))
        f.write('|{name}|{artists}|{album}|\n'.format(
            name=tr.get('name', ''),
            artists=artists,
            album=tr.get('album', {}).get('name', '')
        ))
    f.write('\n')

def main():
    # Parse arguments.
    parser = argparse.ArgumentParser(description='Convert json from spotify-backup to a markdown we want')
    parser.add_argument('-i', '--input', dest='input',
                        help='input JSON file (default: output.json, use "-" for stdin)',
                        default='output.json')
    parser.add_argument('-o', '--output', dest='file',
                        help='output filename (required)',
                        default='output.md',
                        required=True)
    parser.add_argument('-s', '--per-playlist', dest='per_playlist', action='store_true',
                        help='write each playlist to its own file named after the playlist (default: false)')
    args = parser.parse_args()
    # Load input JSON. Support '-' for stdin.
    try:
        if args.input == '-':
            data = json.load(sys.stdin)
        else:
            with open(args.input, 'r', encoding='utf-8') as inf:
                data = json.load(inf)
    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input}")
        sys.exit(2)
    except json.JSONDecodeError as e:
        logging.error(f"Could not parse JSON from {args.input}: {e}")
        sys.exit(3)

    # Expect the input JSON to contain 'playlists' and optionally 'albums' or 'liked_albums'
    playlists = data.get('playlists', [])
    liked_albums = data.get('albums', data.get('liked_albums', []))

    # If they didn't give an output filename, then prompt them. (They probably just double-clicked.)
    while not args.file:
        args.file = input('Enter a file name (e.g. playlists.txt): ')
        args.format = args.file.split('.')[-1]

    # If format wasn't set by interactive prompt (i.e. user provided file), derive from extension if possible
    if not hasattr(args, 'format'):
        args.format = args.file.split('.')[-1]


    # Write either a single file with all playlists (default) or one file per playlist.
    output_dir = os.path.dirname(args.file)
    if output_dir == '':
        output_dir = ''

    if args.per_playlist:
        written_files = []
        for playlist in playlists:
            pname = playlist.get('name', 'playlist')
            safe_name = urllib.parse.quote(pname.replace("/", "_"))
            filename = f"{safe_name}.{args.format}"
            path = os.path.join(output_dir, filename) if output_dir else filename
            with open(path, 'w', encoding='utf-8') as f:
                _write_playlist(f, playlist, '#')
            written_files.append(path)
        # make the final logging line reflect what was actually written
        args.file = ','.join(written_files)
    else:
        with open(args.file, 'w', encoding='utf-8') as f:
            for playlist in playlists:
                _write_playlist(f, playlist, '#')
        logging.info('Wrote file: ' + args.file)

if __name__ == '__main__':
    main()
