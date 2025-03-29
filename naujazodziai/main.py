import os, json, argparse, requests, atproto
import ekalba, repo, bluesky, preview

BLUESKY_LOGIN = os.environ.get('BLUESKY_LOGIN')
BLUESKY_PASSWORD = os.environ.get('BLUESKY_PASSWORD')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    generate_html_parser = subparsers.add_parser("html", help="Format posts into HTML for preview")
    generate_html_parser = subparsers.add_parser("update", help="Fetch and update posts in output dir")

    args = parser.parse_args()

    if args.command == "html":
        items = repo.load_json_dir('output')
        items.reverse()
        print(preview.html_posts([bluesky.format(item) for item in items]))
    elif args.command == "update":
        irasai = ekalba.fetch_irasai()['details']['list']
        client = None

        for irasas in irasai:
            contents = {
                'uuid': irasas['uuid'],
                'header': irasas['header'],
                'publishedDate': irasas['publishedDate']
            }

            filename = repo.get_filename(irasas)

            if os.path.exists(filename):
                print(f"File {filename} already exists")
                continue

            try:
                details = ekalba.fetch_details(irasas)
            except (ekalba.DetailsError, requests.RequestException) as e:
                print(f"Failed to fetch details for {irasas['header']}: {e}")
                continue

            contents['details'] = details

            try:
                text = bluesky.format(contents)
            except Exception as e:
                print(f"Failed to format {irasas['header']}: {e}")
                continue

            
            if BLUESKY_LOGIN and BLUESKY_PASSWORD:
                if not client:
                    client = atproto.Client()
                    client.login(BLUESKY_LOGIN, BLUESKY_PASSWORD)
                client.send_post(text)
                print(f'Posted {irasas['header']} to Bluesky')

            repo.save_to_file(contents, filename)


if __name__ == "__main__":
    main()