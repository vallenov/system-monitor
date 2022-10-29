from services.deploy import Deploy


def test_self_deploy():
    try:
        Deploy.deploy_project('system-monitor', 'system_monitor')
    except Exception as e:
        assert False, f'Ошибка {e}'
    else:
        assert True
