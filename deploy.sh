#!/usr/bin/env bash
set -e

SYMLINK_NAME="latest"
CONTAINERS=(redis sphinx mysql uwsgi-pkg)

function deploy() {
    cd ${SOURCE_DIR}
    # Total cleanup
    # TODO: Use tags from incoming webhook
    git reset --hard
    git pull
    # Get app version
    local APP_VERSION=$(git describe --tags)
    # Cleanup
    vagga clean
    # Collect (and build) static
    # TODO: build static at this step
    vagga manage.py collectstatic --noinput
    # Build app
    vagga package
    # Clean unused containers
    vagga _clean --unused
    # Build and sync all containers
    declare -A VERSIONS
    for name in ${CONTAINERS[*]}
    do
        local full_name=${name}.$(vagga _version_hash --short ${name})
        local latest_name=${name}.${SYMLINK_NAME}

        if [ -d .vagga/.lnk ]; then
            root_dir=".vagga/.lnk/.roots/$full_name/root"
        else
            root_dir=".vagga/.roots/$full_name/root"
        fi

        vagga _build ${name}

        rsync \
            --archive \
            --hard-links \
            --delete-after \
            --stats \
            --omit-dir-times \
            --delay-updates \
            --link-dest ${IMAGE_DIR}/${latest_name} \
            ${root_dir}/ \
            ${IMAGE_DIR}/${full_name}

        local tmpdir=$(mktemp -d)
        ln -snf ${full_name} ${tmpdir}/${latest_name}
        rsync \
            --recursive \
            --links \
            --omit-dir-times \
            --verbose \
            ${tmpdir}/ \
            ${IMAGE_DIR}/
        rm -rf ${tmpdir}

        VERSIONS+=([$name]=${full_name})
    done
    # Create new config for lithos
    local NEW_CONFIG=${CONFIG_DIR}/${APP_VERSION}.yaml
    # Load templating helpers
    . /usr/local/bin/mo
    mo ${SOURCE_DIR}/config/prod/lithos/processes/trunk.yaml.template > ${NEW_CONFIG}
}

usage(){
cat <<'EOT'
Deploy stories

Пример использования:
    ./deploy.sh \
        --config-dir /opt/ponyFiction/config \
        --image-dir /opt/ponyFiction/image \
        --source-dir /opt/ponyFiction/source

Параметры:
   -h, --help           Справка по использованию
   -c, --config-dir     Путь к конфигурациям дерева процессов lithos
   -i, --image-dir      Путь к каталогу контейнеров
   -s, --source-dir     Путь к исходному коду
EOT
exit 0;
}

[ $# -eq 0 ] && usage

while [ $# -gt 0 ]
do
    case "$1" in
        -c|--config-dir) CONFIG_DIR=$2; shift;;
        -s|--source-dir) SOURCE_DIR=$2; shift;;
        -i|--image-dir) IMAGE_DIR=$2; shift;;
        -h|--help) usage;;
        *) break;;
    esac
    shift
done

if [ -z ${CONFIG_DIR+x} ] ||
   [ -z ${SOURCE_DIR+x} ] ||
   [ -z ${IMAGE_DIR+x} ];
then
    usage
else
    deploy
fi
