# giuseppe

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/NiceAesth/giuseppe/master.svg)](https://results.pre-commit.ci/latest/github/NiceAesth/giuseppe/master)

Discord bot for the Giuseppe osu! server (or anything bancho.py based)

## Installation

```bash
git clone https://github.com/NiceAesth/giuseppe.git
cd giuseppe
cd docker
cp config.sample.json config.json
# edit config.json
docker-compose up -d
```

Note: If building the image manually, you need to copy Pipfile and Pipfile.lock to the `src/` directory and use that as the build context.
Look at the [build workflow](.github/workflows/docker-image.yml) for more information.
