# Vars
$currentBranch = git symbolic-ref --short HEAD

if ($currentBranch -eq "master") {
    do {
    $pushtomaster = Read-Host -Prompt 'Looks like you are on master branch. Are you really sure you want to push to master?`nLike, absolutely sure? [Y/N]'
    } while ($pushtomaster -ne 'Y' -and $input -ne 'N')

    if ($pushtomaster -eq 'Y') {
        echo 'Okay then...'
    } else {
        Write-Host 'Push aborted.'
        exit
    }
}

git push origin $currentBranch
```