#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

# based on https://gist.github.com/joelittlejohn/5937573
#

main()
{
    cd $SCRIPT_DIR/..

    if [ "$#" -ne 1 ]; then
      echo "Usage: ./generate-changelog.sh user/repo"
      exit 1
    fi

    local JQ
    JQ=$(command -v jq) || {
      echo "Required tool 'jq' missing.  Failed."
      exit 1
    }

    local GSORT
    GSORT=$(command -v gsort || command -v sort) || {
      echo "Required tool 'GNU sort' missing.  Failed."
      exit 1
    }

    IFS=$'\n'
    echo "# Changelog" > CHANGELOG.md

    for m in $(curl -s "https://api.github.com/repos/$1/milestones?state=closed" | "$JQ" -c '.[] | [.title, .number, .description]' | "$GSORT" -r -V); do
        mid=$(echo $m | sed 's/\[".*",\(.*\),".*"\]/\1/')
        title=$(echo $m | sed 's/\["\(.*\)",.*,".*"\]/\1/')

        echo "Processing milestone: $title..."
        echo $m | sed 's/\["\(.*\)",.*\]/## \1/' >> CHANGELOG.md
        echo "" >> CHANGELOG.md
        echo '### Description' >> CHANGELOG.md
        echo $m | sed 's/\[".*",.*,"\(.*\)"\]/\1/' | sed -e 's/\\"/"/g' | sed -e 's/\\r\\n/\\n/g' | sed -e 's/\\n/\'$'\n/g' >> CHANGELOG.md
        echo "" >> CHANGELOG.md
        echo '### Closed Issues' >> CHANGELOG.md
        for i in $(curl -s "https://api.github.com/repos/$1/issues?milestone=$mid&state=closed" | "$JQ" -c '.[] | [.html_url, .number, .title]'); do
            echo $i | sed 's/\["\(.*\)",\(.*\),\"\(.*\)\"\]/* \3 ([#\2](\1))/' | sed 's/\\"/"/g' >> CHANGELOG.md
        done
        echo "" >> CHANGELOG.md
        echo "" >> CHANGELOG.md
    done
}

(main $*)
