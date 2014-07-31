#!/bin/bash
#
# updates to the next version and adds the changes to the index

getversion(){
  # get the current version from the branch name
  branch_name="$(git symbolic-ref HEAD 2>/dev/null)" ||
  branch_name="(unnamed branch)"     # detached HEAD
  branch_name=${branch_name##refs/heads/}
  echo ${branch_name##release-}
}

getlongversion(){
  sed -e 's/^\([0-9]*\)\.\?\([0-9]*\)\?\.\?\([0-9]*\)\?\([a-z]*[0-9]*\)\?$/\1.\2.\3\4/' -e 's/^\./0./' -e 's/\.\([^0-9]\)/.0\1/g' -e 's/\.\([^0-9]\)/.0\1/g' -e 's/\.$/.0/' <<< $1
}

getlibversion(){
  sed -e 's/[^0-9.].*//' <<< $1
}

if [ $1 ]; then
  version="$1"
else
  version=`getversion`
fi

if grep 'devel' <<<$version &>/dev/null && $prompt; then
  read -e -p "which version? [$version](`getlongversion $version`) " newversion; [ $newversion ] && version="$newversion" && unset newversion
  echo
fi

longversion=`getlongversion $version`
libversion=`getlibversion $longversion`

echo "updating to version $version ($longversion)($libversion)"

if [ ! $version ] || [ ! $longversion ] || [ ! $libversion ]; then
  echo "one of the version strings is empty" >&2
  exit 1
fi

if ! grep '[0-9]\+.[0-9]\+.[0-9]\+' &>/dev/null <<< $libversion; then
  echo "error: libversion has wrong format" >&2
  exit 1
fi

# update the version information header entry
sed -i -e "/const char \\*version\\(\\[\\]\\)\?/ s/\"[^\"]\+\"/\"$version\"/" include/config.hpp

# update autoconf information
sed -i -e "/AC_INIT(/ s/\[[^]]*\]/[$version]/2" configure.ac

# update libversion
sed -i -e "s/\(-release\)\s\+[0-9:.]*/\1 $libversion/" Makefile.am

# confirm the changes
required="include/config.hpp configure.ac Makefile.am"
for file in $required; do
    if ! git ls-files -m 2>/dev/null | grep $file &>/dev/null; then
        echo "warning: file was not modified: $file" >&2
    fi
done

while true; do

  read -p "perform pre-release tasks (git-add and git-rm) [y/N]" remove
  case "$remove" in
    y|Y)
      echo "adding changed files"
      git add $required
      echo "removing pushversion.sh"
      git rm --cached $0
      rm $0
      break
      ;;
    n|N)
      break
      ;;
    "")
      break
      ;;
    *)
      echo "Please enter 'y' or 'n'" >&2
      ;;
  esac

done

echo "done"

