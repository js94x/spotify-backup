import argparse, json, logging, sys, urllib.parse

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')


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


    with open(args.file, 'w', encoding='utf-8') as f:

        f.write('# Spotify Dump\n\n')
        for playlist in data['playlists']:
            f.write('## ' + playlist['name'] + '\n\n')
            f.write('|Titel|Artist(s)|Album|\n')
            f.write('|---|---|---|\n')
            for track in playlist['tracks']:
                if track['track'] is None:
                    continue
                f.write('|{name}|{artists}|{album}|\n'.format(
                    name=track['track']['name'],
                    artists=', '.join(["["+artist['name']+"]"+"(./artists/"+urllib.parse.quote(artist['name'].replace("/", "_"))+".md)" for artist in track['track']['artists']]),
                    album=track['track']['album']['name']
                ))
            f.write('\n')
    
    logging.info('Wrote file: ' + args.file)

if __name__ == '__main__':
    main()
