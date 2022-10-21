from services.deploy import Deploy


def test_self_deploy():
    try:
        Deploy.deploy_project('system-monitor', 'system_monitor')
    except Exception:
        assert False, 'Ошибка'
    else:
        assert True
