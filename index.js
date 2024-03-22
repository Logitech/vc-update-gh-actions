const core = require('@actions/core');
const github = require('@actions/github');





async function run() {
    const github_token = ''
    if ("github_token" in process.env) {
        github_token =  process.env.github_token;
    } else {
        github_token = core.getInput('github_token');
    }

    const config = {
        github_token: github_token,
        check_name: core.getInput('check_name'),
        ref: core.getInput('ref'),
        concurency: 5,
    };
    
    const { repository, pull_request } = github.context.payload;
    const repoInfo = {
        owner: repository.owner.login,
        repo: repository.name,
        ref: config.ref === '' ? pull_request.head.ref : config.ref,
    };
    
    const check_info = Object.assign({ status: 'completed' }, repoInfo);
    
    try {
        const octokit = github.getOctokit(config.github_token); //new github.GitHub(config.github_token);
        const checks = await octokit.rest.checks.listForRef(check_info);
        const check_runs = checks.data.check_runs;
        for (var i = 0; i < check_runs.length; i+=config.concurency) {
            await Promise.all(
                check_runs.slice(i, i+config.concurency)
                    .filter(check_run => check_run.name === config.check_name)
                    .map(async (check_run) => {
                        await octokit.rest.checks.update({
                            owner: repoInfo.owner,
                            repo: repoInfo.repo,
                            check_run_id: check_run.id,
                            conclusion: 'success',
                        })
                    })
            );
        }
    } catch (error) {
        core.setFailed(error.message);
    }
}

run();
