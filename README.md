# Pi-Hole Lists (a.k.a Adlists)

Adlists to complete your pi-hole server.
Create your own list in an uncomplicated way.

## Requirements

- Docker and docker-compose (optional)

## Ready-to-use list

| List        | Link                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------- |
| abuse       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/abuse.txt)       |
| adobe       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/adobe.txt)       |
| ads         | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/ads.txt)         |
| ads_malware | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/ads_malware.txt) |
| amp         | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/amp.txt)         |
| basic       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/basic.txt)       |
| crypto      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/crypto.txt)      |
| dating      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/dating.txt)      |
| drugs       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/drugs.txt)       |
| facebook    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/facebook.txt)    |
| fakenews    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/fakenews.txt)    |
| fraud       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/fraud.txt)       |
| gambling    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/gambling.txt)    |
| phishing    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/phishing.txt)    |
| piracy      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/piracy.txt)      |
| porn        | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/porn.txt)        |
| ransonmware | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/ransonmware.txt) |
| redirect    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/redirect.txt)    |
| scam        | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/scam.txt)        |
| smart-tv    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/smart-tv.txt)    |
| social      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/social.txt)      |
| tiktok      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/tiktok.txt)      |
| torrent     | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/torrent.txt)     |
| tracking    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/tracking.txt)    |
| vaping      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/vaping.txt)      |
| whatsapp    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/whatsapp.txt)    |
| x           | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/x.txt)           |
| youtube     | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/youtube.txt)     |

## How to generate a compiled list

Create a docker image:

```sh
docker-compose build
```

Run the program with your preferred lists:

```sh
LISTS=porn,ads_malware docker-compose run build
```

Leave the variable `LISTS` to get all the hosts builded:

```sh
docker-compose run build
```

To cleanup the lists (removing duplicated entries, etc):

```sh
docker-compose run cleanup
```

## How to contribute to the project

Fork it. Open your own PR with the hosts added and some explanation about why are they being added for us to review. If you are not used to edit these files, just open an issue an we are gonna update ASAP.

**Please do not directly email any committers with questions or problems.** A community is best served when discussions are held in public.

Searching the [issues](https://github.com/dcotecnologia/pi-hole-lists/issues) for your problem is also a good idea.

## Contributing

- Check out the latest master to make sure the feature hasn"t been implemented or the bug hasn't been fixed yet;
- Check out the issue tracker to make sure someone already hasn"t requested it and/or contributed it;
- Fork the project;
- Start a feature/bugfix branch;
- Commit and push until you are happy with your contribution;
- Make sure to add tests for it. This is important so I don't break it in a future version unintentionally.;
- Please try not to mess with the Rakefile, version, or history. If you want to have your own version, or is otherwise necessary, that is fine, but please isolate to its own commit so I can cherry-pick around it.

## License

Please see [LICENSE](LICENSE) for licensing details.

## Sources

The main source is [Blocklist Project](https://github.com/blocklistproject/Lists), [License](https://github.com/blocklistproject/Lists/blob/master/LICENSE).

## Maintainers

Danilo Carolino, [@danilogco](https://github.com/danilogco)
