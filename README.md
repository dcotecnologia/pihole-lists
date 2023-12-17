# Pi-Hole Lists (a.k.a Adlists)

Adlists to complete your pi-hole server.
Create your own list in an uncomplicated way.

## Requirements

- Docker and docker-compose (optional)

## Add the list directly in your pi-hole server

<https://raw.githubusercontent.com/dcotecnologia/pi-hole-lists/master/src/out/ads_malware+fakenews+gambling+porn.txt>

That's the most recommended list. You can find all the lists already builded in the out/ folder.

## Download the latest build

<https://github.com/dcotecnologia/pi-hole-lists/releases>

## How to generate a compiled list

Create a docker image:

```sh
docker-compose build
```

Run the program with your preferred lists:

```sh
LISTS=porn,ads_malware docker-compose run app
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

**Please do not directly email any committers with questions or problems.**  A community is best served when discussions are held in public.

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

## Maintainers

Danilo Carolino, [@danilogco](https://github.com/danilogco)