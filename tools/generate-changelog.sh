#!/usr/bin/env bash

REL_SCRIPT_DIR="`dirname \"$0\"`"
SCRIPT_DIR="`( cd \"$REL_SCRIPT_DIR\" && pwd )`"

# based on https://gist.github.com/joelittlejohn/5937573
#

main()
{
    cd $SCRIPT_DIR/..

    if [ "$#" -ne 2 ]; then
      echo "Usage: ./generate-changelog.sh user/repo <github token>"
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

    for m in $(
        curl -s -H "Authorization: token $2" "https://api.github.com/repos/$1/milestones?state=closed&per_page=100" \
        | jq -c '.[] | [.title, .number]' \
        | sed 's/-/\!/' | sort -rV  | sed 's/\!/-/' # sed trick to put -alpha, -beta, etc earlier than GA release
      ); do

      echo "Processing milestone: $title..."
      echo $m | sed 's/\["\(.*\)",.*\]/\n## \1/' >> CHANGELOG.md
      mid=$(echo $m | sed 's/.*,\(.*\)]/\1/')

      for i in $(curl -s -H "Authorization: token $2" "https://api.github.com/repos/$1/issues?milestone=$mid&state=closed" | jq -r '.[] | [.html_url, .number, .title, (.labels[] | select(.name == "breaking") | .name)] | @tsv'); do
        if [ "$(echo "$i" | cut -f 4)" = "breaking" ]; then
            echo "* **$(echo "$i" | cut -f 3 | sed 's/_/\\_/g') ([#$(echo "$i" | cut -f 2)]($(echo "$i" | cut -f 1)))**"  >> CHANGELOG.md
        else
            echo "* $(echo "$i" | cut -f 3 | sed 's/_/\\_/g') ([#$(echo "$i" | cut -f 2)]($(echo "$i" | cut -f 1)))"  >> CHANGELOG.md
        fi
      done
    done

    git commit -am "Update Changelog"
}

(main $*)
