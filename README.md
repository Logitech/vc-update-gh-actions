# GitHub checks updater

This actionacts as a workround sets previously executed check run to successful state. https://github.community/t5/GitHub-Actions/duplicate-checks-on-pull-request-event/td-p/33157

## Inputs

### `github_token`

**Required** GitHub access token

### `check_name`

**Required** The name of the check run that should be updated.

### `ref`

**Optional** Git ref where check should be updated. Default is to check latest ref in the PR.

## Example usage

  uses: adoroshenko-logitech/update-previous-checks@v1.0.0
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    check_name: verify-pr-labels

