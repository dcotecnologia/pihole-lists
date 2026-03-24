# Pi-Hole Lists | Adlists

[![Tests](https://github.com/dcotecnologia/pihole-lists/actions/workflows/tests.yml/badge.svg)](https://github.com/dcotecnologia/pihole-lists/actions/workflows/tests.yml)

Simplified adlists to complete your local dns server. You will need a software like [Pi-Hole](https://github.com/pi-hole/pi-hole).

| basic (Recommended)      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/basic.txt)       | A starter list that contains malicious, spam, phishing, ads, malware, spam and tracking                        |

## Community

I strongly recommend that you import and keep these lists as an add-on. Don't worry, Pi-hole will merge all your imported lists.

```json
{
    "openphish": "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt",
    "Spam404": "https://raw.githubusercontent.com/Spam404/lists/refs/heads/master/main-blacklist.txt",
    "stevenblack": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "someonewhocares": "https://someonewhocares.org/hosts/hosts",
    "yoyo": "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&mimetype=plaintext&useip=0.0.0.0",
    "adaway": "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt",
    "nolovia": "https://raw.githubusercontent.com/parseword/nolovia/master/skel/hosts-windows-telemetry.txt"
}
```

## Ready-to-use list

| List        | Link                                                                                               | Description                                            |
| ----------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| adobe       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/adobe.txt)       | Adobe Telemetry                                        |
| amp         | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/amp.txt)         | Block AMP pages with this list                         |
| crypto      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/crypto.txt)      | Crypto / cryptojacking based sites                     |
| dating      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/dating.txt)      | Known sites about dating                               |
| drugs       | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/drugs.txt)       | RE sites that deal with illegal drugs                  |
| facebook    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/facebook.txt)    | Block FB and FB related / owned services               |
| fakenews    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/fakenews.txt)    | Known sites that promote fake news                     |
| intelbras   | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/intelbras.txt)   | Intelbras service & events tracking                    |
| gambling    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/gambling.txt)    | All gambling based site legit and illegal              |
| microsoft   | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/microsoft.txt)   | General Microsoft reladted hosts                       |
| piracy      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/piracy.txt)      | Knows sites that allow for illegal downloads           |
| porn        | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/porn.txt)        | Porn or sites that promote porn                        |
| redirect    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/redirect.txt)    | Sites that redirect your from your intended site       |
| smart-tv    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/smart-tv.txt)    | Smart TV call home and ads                             |
| social      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/social.txt)      | All the most popular social networks                   |
| tiktok      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/tiktok.txt)      | Copy and pasted into your device                       |
| torrent     | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/torrent.txt)     | Torrent directory                                      |
| vaping      | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/vaping.txt)      | User requested list that blocks sites promoting vaping |
| whatsapp    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/whatsapp.txt)    | User requested list that blocks only WhatsApp          |
| x           | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/x.txt)           | User requested list that blocks only X / Twitter       |
| youtube     | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/lists/youtube.txt)     | User requested list that blocks only Youtube           |

## External lists

| List                                                                                                                                     |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Adaway             | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/adaway_hosts.txt)              |
| Nolovia            | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/nolovia_hosts.txt)             |
| Openshift          | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/openphish_hosts.txt)           |
| Someonewhocares    | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/someonewhocares_hosts.txt)     |
| Spam404            | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/Spam404_hosts.txt)             |
| stevenblack        | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/stevenblack_hosts.txt)         |
| yoyo               | [Link](https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/imported/yoyo_hosts.txt)                |

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
