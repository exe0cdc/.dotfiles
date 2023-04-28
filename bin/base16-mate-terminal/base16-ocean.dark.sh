#!/usr/bin/env bash
# Base16 Ocean - Mate Terminal color scheme install script
# Chris Kempson (http://chriskempson.com)

[[ -z "$PROFILE_NAME" ]] && PROFILE_NAME="Base 16 Ocean Dark"
[[ -z "$PROFILE_SLUG" ]] && PROFILE_SLUG="base-16-ocean-dark"
[[ -z "$DCONFTOOL" ]] && DCONFTOOL=dconf
[[ -z "$BASE_KEY" ]] && BASE_KEY=/org/mate/terminal/profiles

PROFILE_KEY="$BASE_KEY/$PROFILE_SLUG"

dset() {
  local key="$1"; shift
  local val="$1"; shift

  "$DCONFTOOL" write "$PROFILE_KEY/$key" "$val"
}

# Because gconftool doesn't have "append"
glist_append() {
  local key="$1"; shift
  local val="$1"; shift

  local entries="$(
    {
      "$DCONFTOOL" read "$key" | tr -d '[]' | tr , "\n" | fgrep -v "$val"
      echo "'$val'"
    } | head -c-1 | tr "\n" ,
  )"

  "$DCONFTOOL" write "$key" "[$entries]"
}

# Append the Base16 profile to the profile list
glist_append /org/mate/terminal/global/profile-list "$PROFILE_SLUG"

dset visible-name "'$PROFILE_NAME'"
dset palette "'#2B303B:#BF616A:#A3BE8C:#EBCB8B:#8FA1B3:#B48EAD:#96B5B4:#C0C5CE:#65737E:#BF616A:#A3BE8C:#EBCB8B:#8FA1B3:#B48EAD:#96B5B4:#EFF1F5'"
dset background-color "'#2B303B'"
dset foreground-color "'#C0C5CE'"
dset bold-color "'#C0C5CE'"
dset bold-color-same-as-fg "true"
dset use-theme-colors "false"
dset use-theme-background "false"
