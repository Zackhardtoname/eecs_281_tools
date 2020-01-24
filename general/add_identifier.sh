if [ $# -eq 0 ]
  then
    read -e -p "Your identifier: " identifier
else
	identifier=$1
fi

for src in *.cpp *.h; do
	line=$(head -n 1 $src)
    if [[ "$line" != *"$identifier"* ]]; then
        { echo "// $identifier"; cat "$src"; } > "$src.tmp" && mv "$src.tmp" "$src"
        echo "added $src"
    else
        echo "skipped $src"
    fi
done

read -p "all set: press enter to continue"