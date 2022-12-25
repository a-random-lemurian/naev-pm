import pygit2 as git
import datetime
from naevpm import plugin_registry
from naevpm.database import set_key


# Taken from <https://github.com/MichaelBoselowitz/pygit2-examples/blob/master/examples.py>
def git_repository_pull(repo, remote_name='origin', branch='main'):
    for remote in repo.remotes:
        if remote.name == remote_name:
            remote.fetch()
            remote_master_id = repo.lookup_reference('refs/remotes/origin/%s' % (branch)).target
            merge_result, _ = repo.merge_analysis(remote_master_id)
            # Up to date, do nothing
            if merge_result & git.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                return
            # We can just fastforward
            elif merge_result & git.GIT_MERGE_ANALYSIS_FASTFORWARD:
                repo.checkout_tree(repo.get(remote_master_id))
                try:
                    master_ref = repo.lookup_reference('refs/heads/%s' % (branch))
                    master_ref.set_target(remote_master_id)
                except KeyError:
                    repo.create_branch(branch, repo.get(remote_master_id))
                repo.head.set_target(remote_master_id)
            elif merge_result & git.GIT_MERGE_ANALYSIS_NORMAL:
                repo.merge(remote_master_id)

                if repo.index.conflicts is not None:
                    for conflict in repo.index.conflicts:
                        print('Fatal: conflicts found in:'+conflict[0].path)
                    raise AssertionError('Please resolve the conflict')

                user = repo.default_signature
                tree = repo.index.write_tree()
                commit = repo.create_commit('HEAD',
                                            user,
                                            user,
                                            'Merge!',
                                            tree,
                                            [repo.head.target, remote_master_id])
                # We need to do this or git CLI will think we are still merging.
                repo.state_cleanup()
            else:
                raise AssertionError('Unknown merge analysis result')


def update_one_registry(registry_dir: str):
    repo = git.Repository(registry_dir)
    print(f"Updating registry {registry_dir}")
    git_repository_pull(repo)


def update_registries():
    """
    Update the registries to receive updated information
    from the GitHub plugin registries.
    """

    # Set the last time the plugin registry was updated,
    # so the player can be reminded again in a week.
    now = datetime.datetime.now()
    set_key("last_registry_update_time", now.strftime("%Y-%m-%dT%H:%M:%S"))

    for registry in plugin_registry.get_registries_from_database():
        update_one_registry(registry[1])

